from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models

from django.contrib import admin

from datamodel import constants
from . import tests


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


class GameStatus:
    CREATED = 0
    ACTIVE = 1
    FINISHED = 2

    @classmethod
    def getStatus(cls):
        return (cls.CREATED, "Created"), (cls.ACTIVE, "Active"), (cls.FINISHED, "Created")

    def __str__(self): \
            return "Status: " + self.status


class Game(models.Model):
    MIN_CELL = 0
    MAX_CELL = 63
    celdas_validas = []

    cat_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='games_as_cat')
    mouse_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='games_as_mouse')

    cat1 = models.IntegerField(default=0, null=False, blank=False)
    cat2 = models.IntegerField(default=2, null=False, blank=False)
    cat3 = models.IntegerField(default=4, null=False, blank=False)
    cat4 = models.IntegerField(default=6, null=False, blank=False)
    mouse = models.IntegerField(default=59, null=False, blank=False)
    cat_turn = models.BooleanField(default=True, null=False, blank=False)
    status = models.IntegerField(default=GameStatus.CREATED)

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        if len(self.celdas_validas) == 0:
            self.posiciones_validas()

        if self.cat1 not in self.celdas_validas:
            raise ValidationError("Invalid cell for a cat or the mouse|Gato o ratón en posición no válida")

        if self.cat2 not in self.celdas_validas:
            raise ValidationError("Invalid cell for a cat or the mouse|Gato o ratón en posición no válida")

        if self.cat3 not in self.celdas_validas:
            raise ValidationError("Invalid cell for a cat or the mouse|Gato o ratón en posición no válida")

        if self.cat4 not in self.celdas_validas:
            raise ValidationError("Invalid cell for a cat or the mouse|Gato o ratón en posición no válida")

        if self.mouse not in self.celdas_validas:
            raise ValidationError("Invalid cell for a cat or the mouse|Gato o ratón en posición no válida")

    def save(self, *args, **kwargs):
        if self.cat1 is None:
            raise ValidationError("No hay usuario gato...")

        if self.mouse_user and self.status == GameStatus.CREATED:
            self.status = GameStatus.ACTIVE

        if not (
                self.MAX_CELL >= self.cat1 >= self.MIN_CELL and self.MAX_CELL >= self.cat2 >= self.MIN_CELL and self.MAX_CELL >= self.cat3 >= self.MIN_CELL and self.MAX_CELL >= self.cat4 >= self.MIN_CELL and self.MAX_CELL >= self.mouse >= self.MIN_CELL):
            raise ValidationError(tests.MSG_ERROR_MOVE)

        if len(self.celdas_validas) == 0:
            self.posiciones_validas()

        if self.cat1 not in self.celdas_validas:
            raise ValidationError(tests.MSG_ERROR_INVALID_CELL)

        if self.cat2 not in self.celdas_validas:
            raise ValidationError(tests.MSG_ERROR_INVALID_CELL)

        if self.cat3 not in self.celdas_validas:
            raise ValidationError(tests.MSG_ERROR_INVALID_CELL)

        if self.cat4 not in self.celdas_validas:
            raise ValidationError(tests.MSG_ERROR_INVALID_CELL)

        if self.mouse not in self.celdas_validas:
            raise ValidationError(tests.MSG_ERROR_INVALID_CELL)

        super(Game, self).save(*args, **kwargs)

    def posiciones_validas(self):
        for i in range(8):
            for j in range(8):
                celda = i * 8 + j

                if i % 2 == 0:
                    if j % 2 == 0:
                        self.celdas_validas.append(celda)

                else:
                    if j % 2 != 0:
                        self.celdas_validas.append(celda)

    def __str__(self):
        string = "(" + str(self.id) + ", "
        if self.status == GameStatus.ACTIVE:
            string += "Active)\t"
        elif self.status == GameStatus.CREATED:
            string += "Created)\t"
        elif self.status == GameStatus.FINISHED:
            string += "Finished)\t"

        if self.cat_turn:
            string += "Cat [X] "
        else:
            string += "Cat [ ] "

        string += str(self.cat_user) + "(" + str(self.cat1) + ", " + str(self.cat2) + ", " + str(
            self.cat3) + ", " + str(self.cat4) + ")"

        if self.mouse_user:
            string += " --- Mouse "
            string += "[X] " if not self.cat_turn else "[ ] "
            string += str(self.mouse_user) + "(" + str(self.mouse) + ")"

        return string


class Move(models.Model):
    origin = models.IntegerField(blank=False, null=False)
    target = models.IntegerField(blank=False, null=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="moves")
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, blank=False, null=False)

    def __str__(self): \
        return self.origin, self.target

    def movimientos_validos(self):
        origin = int(self.origin)
        target = int(self.target)

        if self.game.cat_turn:
            if origin % 8 == 0:
                targetcalc = origin + 9
                if target != targetcalc:
                    return False
            elif origin % 8 == 7:
                targetcalc = origin + 7
                if target != targetcalc:
                    return False
            else:
                targetcalc1 = origin + 7
                targetcalc2 = origin + 9
                if target != targetcalc1 and target != targetcalc2:
                    return False
            if target == self.game.cat1 or target == self.game.cat2 or target == self.game.cat3 or target == self.game.cat4 or target == self.game.mouse:
                return False

            return True

        else:
            if origin % 8 == 0:
                targetcalc1 = origin + 9
                targetcalc2 = origin - 7
                if target != targetcalc1 and target != targetcalc2:
                    return False
            elif origin % 8 == 7:
                targetcalc1 = origin + 7
                targetcalc2 = origin - 9
                if target != targetcalc1 and target != targetcalc2:
                    return False
            else:
                targetcalc1 = origin + 7
                targetcalc2 = origin + 9
                targetcalc3 = origin - 7
                targetcalc4 = origin - 9
                if target != targetcalc1 and target != targetcalc2 and target != targetcalc3 and target != targetcalc4:
                    return False
            if target == self.game.cat1 or target == self.game.cat2 or target == self.game.cat3 or target == self.game.cat4 or target == self.game.mouse:
                return False
            return True

    def finish_game(self):
        gatos = [self.game.cat1, self.game.cat2, self.game.cat3, self.game.cat4]
        if self.game.mouse == 0 or self.game.mouse == 2 or self.game.mouse == 4 or self.game.mouse == 6:
            return True

        for gato in gatos:
            if gato == self.game.mouse or gato == self.game.mouse or gato == self.game.mouse or gato == self.game.mouse:
                return True

        return False

    def save(self, *args, **kwargs):
        origin = int(self.origin)
        target = int(self.target)
        if self.game.status == GameStatus.CREATED or self.game.status == GameStatus.FINISHED:
            raise ValidationError(constants.MSG_ERROR_MOVE)

        if self.finish_game() is True:
            raise ValidationError(constants.FINISHED_GAME)

        if self.game.status == GameStatus.FINISHED:
            raise ValidationError(constants.FINISHED_GAME)

        if self.movimientos_validos() is False:
            raise ValidationError(constants.MSG_ERROR_MOVE)

        if self.player == self.game.mouse_user and not self.game.cat_turn:
            self.game.mouse = target
            self.game.cat_turn = True
            self.game.save()

        elif self.player == self.game.cat_user and self.game.cat_turn:
            if origin == self.game.cat1:
                self.game.cat1 = target
                self.game.cat_turn = False
                self.game.save()

            elif origin == self.game.cat2:
                self.game.cat2 = target
                self.game.cat_turn = False
                self.game.save()

            elif origin == self.game.cat3:
                self.game.cat3 = target
                self.game.cat_turn = False
                self.game.save()

            elif origin == self.game.cat4:
                self.game.cat4 = target
                self.game.cat_turn = False
                self.game.save()

            else:
                raise ValidationError(tests.MSG_ERROR_INVALID_CELL)

        elif not(self.player == self.game.cat_user and self.game.cat_turn and self.player == self.game.mouse_user and not self.game.cat_turn):
            raise ValidationError(constants.MSG_ERROR_MOVE)

        super(Move, self).save(*args, **kwargs)


class CounterManager(models.Manager):
    def create(self, *args, **kwargs):
        raise ValidationError(tests.MSG_ERROR_NEW_COUNTER)

    @classmethod
    def createCounter(cls, valor):
        counter = Counter(value=valor)
        super(Counter, counter).save()
        return counter



    def inc(self):
        try:
            counter = Counter.objects.get()
            counter.value += 1
            Counter.objects.all().filter().update(value=counter.value)
            return counter.value

        except ObjectDoesNotExist:
            counter = CounterManager.createCounter(1)
            return counter.value

    def get_current_value(self):
        try:
            Counter.objects.get()
            value = Counter.objects.filter().values('value').first()
            return value['value']
        except ObjectDoesNotExist:
            counter = CounterManager.createCounter(0)
            return counter.value


class Counter(models.Model):
    value = models.IntegerField(default=0)
    objects = CounterManager()

    def __str__(self): \
            return "Value: {}".format(self.value)

    def save(self, *args, **kwargs):
        raise ValidationError(tests.MSG_ERROR_NEW_COUNTER)
        super(Counter, self).save(*args, **kwargs)
