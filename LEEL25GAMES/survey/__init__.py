from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='¿Qué edad tienes?', min=13, max=125)
    gender = models.StringField(
        choices=[['Male', 'Hombre'], ['Female', 'Mujer']],
        label='Cuál es tu género',
        widget=widgets.RadioSelect,
    )
    


# FUNCTIONS
# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']


# class CognitiveReflectionTest(Page):
#     form_model = 'player'
#     form_fields = ['crt_bat', 'crt_widget', 'crt_lake']


page_sequence = [Demographics]
