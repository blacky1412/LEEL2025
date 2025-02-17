from otree.api import *

doc = """
... (docstring unchanged) ...
"""

class Constants(BaseConstants):
    name_in_url = 'cazadores'
    players_per_group = 2
    num_rounds = 1

    pago_ambos_emboscar = 5
    pago_ambos_esperar = 15
    pago_emboscar_vs_esperar = 30

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    def set_payoffs(self):
        jugadores = self.get_players()
        decision_1 = jugadores[0].decision
        decision_2 = jugadores[1].decision

        if decision_1 == 'EMBOSCAR' and decision_2 == 'EMBOSCAR':
            jugadores[0].payoff = Constants.pago_ambos_emboscar
            jugadores[1].payoff = Constants.pago_ambos_emboscar
        elif decision_1 == 'EMBOSCAR' and decision_2 == 'ESPERAR':
            jugadores[0].payoff = Constants.pago_emboscar_vs_esperar
            jugadores[1].payoff = 0
        elif decision_1 == 'ESPERAR' and decision_2 == 'EMBOSCAR':
            jugadores[0].payoff = 0
            jugadores[1].payoff = Constants.pago_emboscar_vs_esperar
        else:
            # Ambos ESPERAR
            jugadores[0].payoff = Constants.pago_ambos_esperar
            jugadores[1].payoff = Constants.pago_ambos_esperar

class Player(BasePlayer):
    sexo = models.StringField(
        label="Selecciona tu sexo:",
        choices=['Masculino', 'Femenino'],
        widget=widgets.RadioSelect
    )
    decision = models.StringField(
        label="Elige tu acción:",
        choices=['EMBOSCAR', 'ESPERAR'],
        widget=widgets.RadioSelect
    )
    # Note: Label is empty to avoid duplication
    porcentaje_predicho = models.IntegerField(
        label="",
        min=0,
        max=100
    )

    @staticmethod
    def custom_export(players):
        yield ['Sexo', 'Decisión', 'Porcentaje ESPERAR', 'Porcentaje EMBOSCAR']
        for p in players:
            porcentaje_esperar = p.porcentaje_predicho
            porcentaje_emboscar = 100 - p.porcentaje_predicho
            yield [p.sexo, p.decision, porcentaje_esperar, porcentaje_emboscar]

class Sexo(Page):
    form_model = 'player'
    form_fields = ['sexo']

class EsperaSexo(WaitPage):
    pass

class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

    @staticmethod
    def vars_for_template(player: Player):
        otros = player.get_others_in_group()
        sexo_oponente = otros[0].sexo if otros else 'No disponible'
        return dict(sexo_oponente=sexo_oponente)

class Porcentaje(Page):
    form_model = 'player'
    form_fields = ['porcentaje_predicho']

class EsperaResultados(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_payoffs()

class Resultados(Page):
    @staticmethod
    def vars_for_template(player: Player):
        otro = player.get_others_in_group()[0]
        porcentaje_esperar = player.porcentaje_predicho
        porcentaje_emboscar = 100 - player.porcentaje_predicho
        return dict(
            mi_sexo=player.sexo,
            mi_decision=player.decision,
            mi_pago=player.payoff,
            otro_decision=otro.decision,
            otro_pago=otro.payoff,
            porcentaje_esperar=porcentaje_esperar,
            porcentaje_emboscar=porcentaje_emboscar,
        )

page_sequence = [
    Sexo,
    EsperaSexo,
    Decision,
    Porcentaje,
    EsperaResultados,
    Resultados
]
