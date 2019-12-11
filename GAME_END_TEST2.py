import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ratonGato.settings')
django.setup()

from django.contrib.auth.models import User
from datamodel.models import Game, Move, GameStatus, WinStatus

#creamos un usuario para el juego (gatos)
try:
    user3 = User.objects.get(id=300)
except User.DoesNotExist:
    user3 = User.objects.create_user(id=300, username="username3")

#creamos el segundo usuario para el juego (raton)
try:
    user4 = User.objects.get(id=300)
except User.DoesNotExist:
    user4 = User.objects.create_user(id=400, username="username4")

#creamos un juego y añadimos a los dos jugadores
game = Game(id=89, cat_user=user3, mouse_user=user4)
game.save()

#mover segundo gato de la posicion 2 a la 11
move1 = Move.objects.create(game=game, player=user3, origin=2, target=11)

#mover raton de la posicion 59 a la 50
move2 = Move.objects.create(game=game, player=user4, origin=59, target=50)

#mover segundo gato de la posicion 11 a la 18
move3 = Move.objects.create(game=game, player=user3, origin=11, target=18)

#mover raton de la posicion 50 a la 43
move4 = Move.objects.create(game=game, player=user4, origin=50, target=43)

#mover segundo gato de la posicion 18 a la 25
move5 = Move.objects.create(game=game, player=user3, origin=18, target=25)

#mover raton de la posicion 43 a la 36
move6 = Move.objects.create(game=game, player=user4, origin=43, target=36)

#mover segundo gato de la posicion 25 a la 32
move7 = Move.objects.create(game=game, player=user3, origin=25, target=32)

#mover raton de la posicion 36 a la 27
move8 = Move.objects.create(game=game, player=user4, origin=36, target=27)

#mover segundo gato de la posicion 32 a la 41
move9 = Move.objects.create(game=game, player=user3, origin=32, target=41)

#mover raton de la posicion 27 a la 20
move10 = Move.objects.create(game=game, player=user4, origin=27, target=20)

#mover segundo gato de la posicion 41 a la 50
move11 = Move.objects.create(game=game, player=user3, origin=41, target=50)

#mover raton de la posicion 20 a la 11
move12 = Move.objects.create(game=game, player=user4, origin=20, target=11)

#mover segundo gato de la posicion 50 a la 59
move13 = Move.objects.create(game=game, player=user3, origin=50, target=59)

#mover raton de la posicion 11 a la 2
move14 = Move.objects.create(game=game, player=user4, origin=11, target=2)

#Comprobamos que se ha acabado el juego y está a FINISHED
if game.status == GameStatus.FINISHED:
    print("EL JUEGO ACABA CORRECTAMENTE")

if game.win != WinStatus.CATS:
    print("EL JUEGO MUESTRA CORRECTAMENTE QUE HA GANADO EL RATON")