from otree.api import *

doc = """
Página de consentimiento para el experimento.
"""

class C(BaseConstants):
    NAME_IN_URL = 'consentimiento'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    acepta = models.BooleanField(
        choices=[
            [True, 'Sí, acepto participar en el estudio.']
            # ,[False, 'No, no deseo participar.']
        ],
        widget=widgets.RadioSelect,
        label="¿Aceptas participar en este experimento?"
    )

class Consentimiento(Page):
    form_model = 'player'
    form_fields = ['acepta']

    # def before_next_page(self, timeout_happened=False):
    #     """Si el jugador no acepta, se le excluye del experimento y no pasa a public_goods."""
    #     if not self.player.acepta:  # Si el jugador NO acepta
    #         self.participant.vars['exp_exit'] = True  # Se marca como excluido

page_sequence = [Consentimiento]

