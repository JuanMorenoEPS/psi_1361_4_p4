from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datamodel import constants

from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse

from logic.forms import SignupForm, MoveForm, LogInForm
from datamodel.models import Game, Move, Counter, GameStatus


def anonymous_required(f):
    def wrapped(request):
        if request.user.is_authenticated:
            return HttpResponseForbidden(
                errorHTTP(request, exception="Action restricted to anonymous users"))
        else:
            return f(request)

    return wrapped


def errorHTTP(request, exception=None):
    context_dict = {}
    context_dict[constants.ERROR_MESSAGE_ID] = exception
    return render(request, "mouse_cat/error.html", context_dict)


def index(request):
    return render(request, "mouse_cat/index.html")


@login_required
def select_game_service(request, game_id=-1):
    user = request.user
    if game_id == -1:
        dict = {}
        user = request.user
        as_cat = Game.objects.filter(cat_user=user, status=GameStatus.ACTIVE)
        if as_cat:
            dict['as_cat'] = as_cat

        as_mouse = Game.objects.filter(mouse_user=user, status=GameStatus.ACTIVE)
        if as_mouse:
            dict['as_mouse'] = as_mouse

        return render(request, "mouse_cat/select_game.html", dict)

    else:
        game = Game.objects.filter(id=game_id).first()
        if not game or game.status != GameStatus.ACTIVE:
            return HttpResponse(constants.ERROR_NOT_FOUND, status=404)
        else:
            if game.cat_user == user or game.mouse_user == user:
                request.session['game_id'] = game.id
                return redirect(reverse('show_game'))
            else:
                return HttpResponse(constants.ERROR_NOT_FOUND, status=404)

@anonymous_required
def login_service(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['counter'] = 0
                request.session['username'] = User.objects.get(username=username).id
                return render(request, 'mouse_cat/index.html')
        else:
            user_form = LogInForm(request.POST or None)
            user_form.is_valid()
            user_form.add_error("username", "Username/password is not valid|Usuario/clave no válidos")
            return render(request, 'mouse_cat/login.html', {'user_form': user_form})
    else:
        user_form = LogInForm
        return render(request, 'mouse_cat/login.html', {'user_form': user_form})


def logout_service(request):
    user = request.user
    logout(request)
    request.session['counter'] = 0
    dictUser = {'user': user}
    return render(request, 'mouse_cat/logout.html', dictUser)


def counter_service(request):
    if 'counter' in request.session:
        request.session['counter'] += 1

    else:
        request.session['counter'] = 1

    counter_global = Counter.objects.inc()
    dict = {'counter_session': request.session['counter'], 'counter_global': counter_global}
    return render(request, 'mouse_cat/counter.html', dict)

@anonymous_required
def signup_service(request):
    user_form = SignupForm(data=request.POST)
    if request.method == 'POST':
        user_form = SignupForm(data=request.POST)
        if user_form.is_valid():
            if user_form.cleaned_data.get('password') != user_form.cleaned_data.get('password2'):
                user_form.add_error("password",
                                    "Password and Repeat password are not the same|La clave y su repetición no coinciden")
                return render(request, 'mouse_cat/signup.html', {'user_form': user_form})
            user = user_form.save()
            user.set_password(user.password)
            request.session['counter'] = 0
            user.save()
            return render(request, 'mouse_cat/signup.html', {'user_form': user_form})
        else:
            user_form.add_error("username", "A user with that username already exists|Usuario duplicado")
            user_form.add_error("password", "(?=.too short)(?=.at least 6 characters)(?=.*too common)")

            return render(request, 'mouse_cat/signup.html', {'user_form': user_form})
    else:
        return render(request, 'mouse_cat/signup.html', {'user_form': user_form})


@login_required
def create_game_service(request):
    game = Game(cat_user=request.user)
    request.session[constants.GAME_SELECTED_SESSION_ID] = game.id
    game.save()
    dict = {'game': game}
    return render(request, "mouse_cat/new_game.html", dict)


@login_required
def join_game_service(request):
    GamesList = Game.objects.all()
    lista_games = []
    lista_ids = []
    for game in GamesList:
        if game.mouse_user is None:
            lista_games.append(game)
            lista_ids.append(game.id)

    if not lista_ids:
        dict = {}
        dict[constants.ERROR_MESSAGE_ID] = "There is no available games|No hay juegos disponibles"
        return render(request, 'mouse_cat/join_game.html', dict)
    else:
        game.mouse_user = request.user
        game.save()
        dict = {'game': game}
        return render(request, 'mouse_cat/join_game.html', dict)


@login_required
def show_game_service(request):
    game_id = request.session['game_id']
    game = Game.objects.get(id=game_id)
    mouse = game.mouse
    cats = [game.cat1, game.cat2, game.cat3, game.cat4]
    board = []

    for i in range(0, 64):
        if i == mouse:
            board.append(-1)
        elif i == game.cat1:
            board.append(1)
        elif i == game.cat2:
            board.append(2)
        elif i == game.cat3:
            board.append(3)
        elif i == game.cat4:
            board.append(4)
        else:
            board.append(0)

    print(game.status)
    if game.status == GameStatus.FINISHED:
        print("acabaaaaaaaaa")
        dictF = {}
        dictF['board'] = board
        dictF['game'] = game
        dictF['finished'] = "Finished Game!"

        return render(request, "mouse_cat/game.html", dictF)

    dict = {}
    dict['game'] = game
    dict['board'] = board
    dict['move_form'] = MoveForm()

    return render(request, "mouse_cat/game.html", dict)


@login_required
def move_service(request):
    player = request.user
    if 'game_id' in request.session.keys():
        game_id = request.session['game_id']
        game = Game.objects.get(id=game_id)

        if request.method == 'POST':
            if not player:
                redirect(reverse('login'))

            move_form = MoveForm(data=request.POST)

            if move_form.is_valid():
                move = Move(game=Game.objects.get(id=game_id), player=player, origin=move_form.data['origin'], target=move_form.data['target'])
                move.save()

            return redirect(reverse('show_game'))

    return HttpResponseNotFound('<h1>Page Not Found</h1>')


