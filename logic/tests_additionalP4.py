from datamodel.models import Game, GameStatus, Move, WinStatus
from django.contrib.auth.models import User


from . import forms
from . import tests_services


class GameEndTests(tests_services.PlayGameBaseServiceTests):
    def setUp(self):
        super().setUp()
        # PARTE PARA EL CASO EN EL QUE GANAN LOS GATOS
        # creamos un usuario para el juego (gatos)
        try:
            self.user1 = User.objects.get(id=100)
        except User.DoesNotExist:
            self.user1 = User.objects.create_user(id=100, username="username1")

        # creamos el segundo usuario para el juego (raton)
        try:
            self.user2 = User.objects.get(id=200)
        except User.DoesNotExist:
            self.user2 = User.objects.create_user(id=200, username="username2")

        # creamos un juego y añadimos a los dos jugadores
        self.game = Game(id=100, cat_user=self.user1, mouse_user=self.user2)
        self.game.save()

        # mover segundo gato de la posicion 2 a la 11
        move1 = Move.objects.create(game=self.game, player=self.user1, origin=2, target=11)

        # mover raton de la posicion 59 a la 50
        move2 = Move.objects.create(game=self.game, player=self.user2, origin=59, target=50)

        # mover segundo gato de la posicion 11 a la 20
        move3 = Move.objects.create(game=self.game, player=self.user1, origin=11, target=20)

        # mover raton de la posicion 50 a la 43
        move4 = Move.objects.create(game=self.game, player=self.user2, origin=50, target=43)

        # mover segundo gato de la posicion 20 a la 27
        move5 = Move.objects.create(game=self.game, player=self.user1, origin=20, target=27)

        # mover raton de la posicion 43 a la 36
        move6 = Move.objects.create(game=self.game, player=self.user2, origin=43, target=36)

        # mover segundo gato de la posicion 27 a la 36 (EL GATO SE COME AL RATON)
        move7 = Move.objects.create(game=self.game, player=self.user1, origin=27, target=36)


        #-----------------------------------------------------------------------------
        #PARTE PARA EL CASO EN EL QUE GANA EL RATON
        # creamos un usuario para el juego (gatos)
        try:
            self.user3 = User.objects.get(id=300)
        except User.DoesNotExist:
            self.user3 = User.objects.create_user(id=300, username="username3")

        # creamos el segundo usuario para el juego (raton)
        try:
            self.user4 = User.objects.get(id=400)
        except User.DoesNotExist:
            self.user4 = User.objects.create_user(id=400, username="username4")

        # creamos un juego y añadimos a los dos jugadores
        self.game2 = Game(id=89, cat_user=self.user3, mouse_user=self.user4)
        self.game2.save()

        # mover segundo gato de la posicion 2 a la 11
        move1 = Move.objects.create(game=self.game2, player=self.user3, origin=2, target=11)

        # mover raton de la posicion 59 a la 50
        move2 = Move.objects.create(game=self.game2, player=self.user4, origin=59, target=50)

        # mover segundo gato de la posicion 11 a la 18
        move3 = Move.objects.create(game=self.game2, player=self.user3, origin=11, target=18)

        # mover raton de la posicion 50 a la 43
        move4 = Move.objects.create(game=self.game2, player=self.user4, origin=50, target=43)

        # mover segundo gato de la posicion 18 a la 25
        move5 = Move.objects.create(game=self.game2, player=self.user3, origin=18, target=25)

        # mover raton de la posicion 43 a la 36
        move6 = Move.objects.create(game=self.game2, player=self.user4, origin=43, target=36)

        # mover segundo gato de la posicion 25 a la 32
        move7 = Move.objects.create(game=self.game2, player=self.user3, origin=25, target=32)

        # mover raton de la posicion 36 a la 27
        move8 = Move.objects.create(game=self.game2, player=self.user4, origin=36, target=27)

        # mover segundo gato de la posicion 32 a la 41
        move9 = Move.objects.create(game=self.game2, player=self.user3, origin=32, target=41)

        # mover raton de la posicion 27 a la 20
        move10 = Move.objects.create(game=self.game2, player=self.user4, origin=27, target=20)

        # mover segundo gato de la posicion 41 a la 50
        move11 = Move.objects.create(game=self.game2, player=self.user3, origin=41, target=50)

        # mover raton de la posicion 20 a la 11
        move12 = Move.objects.create(game=self.game2, player=self.user4, origin=20, target=11)

        # mover segundo gato de la posicion 50 a la 59
        move13 = Move.objects.create(game=self.game2, player=self.user3, origin=50, target=59)

        # mover raton de la posicion 11 a la 2
        move14 = Move.objects.create(game=self.game2, player=self.user4, origin=11, target=2)

    def tearDown(self):
        super().tearDown()

    def test1(self):
        self.assertEqual(self.game.status, GameStatus.FINISHED)
        self.assertEqual(self.game.win, WinStatus.CATS)

    def test2(self):
        self.assertEqual(self.game2.status, GameStatus.FINISHED)
        self.assertEqual(self.game2.win, WinStatus.MOUSE)

