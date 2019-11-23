import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ratonGato.settings')
django.setup()

from django.contrib.auth.models import User
from datamodel.models import Game, Move

#crear usuario de id = 10
try:
    user10 = User.objects.get(id=10)
except User.DoesNotExist:
    user10 = User.objects.create_user(id=10, username="user_id_10")

#crear usuario de id = 11
try:
    user11 = User.objects.get(id=11)
except User.DoesNotExist:
    user11 = User.objects.create_user(id=11, username="user_id_11")

#crear juego y asignarlo al usuario con id = 10
game = Game(cat_user=user10)
game.save()

#Buscar juegos con un solo usuario e imprimirlos
lista_games = []
lista_ids = []

GamesList = Game.objects.all()
for game in GamesList:
    if game.mouse_user is None:
        lista_games.append(game)
        lista_ids.append(game.id)

print(lista_games)

#Buscar e imprimir el juego con menor id
minimo = min(lista_ids)
game_min_id = Game.objects.filter(id=minimo)[0]
game_min_id.mouse_user = user11
game_min_id.save()
print("Juego con el menor id: "+str(game_min_id))

#mover el gato2 de la casilla 2 a la 11
mover11 = Move.objects.create(game=game_min_id, player=user10, origin=2, target=11)
print("Movimiento cat2 a la casilla 11"+str(game_min_id))

#mover el raton de la casilla 59 a la 52
mover = Move.objects.create(game=game_min_id, player=user11, origin=59, target=52)
print("Movimiento mouse a la casilla 52"+str(game_min_id))



















