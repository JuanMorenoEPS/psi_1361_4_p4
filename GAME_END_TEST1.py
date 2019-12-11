import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ratonGato.settings')
django.setup()

from django.contrib.auth.models import User
from datamodel.models import Game, Move, GameStatus, WinStatus

#creamos un usuario para el juego (gatos)
try:
    user1 = User.objects.get(id=100)
except User.DoesNotExist:
    user1 = User.objects.create_user(id=100, username="username1")

#creamos el segundo usuario para el juego (raton)
try:
    user2 = User.objects.get(id=200)
except User.DoesNotExist:
    user2 = User.objects.create_user(id=200, username="username2")

#creamos un juego y añadimos a los dos jugadores
game = Game(id=100, cat_user=user1, mouse_user=user2)
game.save()

#mover segundo gato de la posicion 2 a la 11
move1 = Move.objects.create(game=game, player=user1, origin=2, target=11)

#mover raton de la posicion 59 a la 50
move2 = Move.objects.create(game=game, player=user2, origin=59, target=50)

#mover segundo gato de la posicion 11 a la 20
move3 = Move.objects.create(game=game, player=user1, origin=11, target=20)

#mover raton de la posicion 50 a la 43
move4 = Move.objects.create(game=game, player=user2, origin=50, target=43)

#mover segundo gato de la posicion 20 a la 27
move5 = Move.objects.create(game=game, player=user1, origin=20, target=27)

#mover raton de la posicion 43 a la 36
move6 = Move.objects.create(game=game, player=user2, origin=43, target=36)

#mover segundo gato de la posicion 27 a la 36 (EL GATO SE COME AL RATON)
move7 = Move.objects.create(game=game, player=user1, origin=27, target=36)

#Comprobamos que se ha acabado el juego y está a FINISHED
if game.status == GameStatus.FINISHED:
    print("EL JUEGO ACABA CORRECTAMENTE")

if game.win == WinStatus.CATS:
    print("EL JUEGO MUESTRA CORRECTAMENTE QUE HAN GANADO LOS GATOS")



