from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    PLAYERS_PER_GROUP = 3  # 3 jugadores por grupo
    NUM_ROUNDS = 4  # 4 rondas del juego
    ENDOWMENT = cu(100)  # Dotación inicial de cada jugador
    MULTIPLIER = 2  # Factor de multiplicación del fondo común

class Subsession(BaseSubsession):
    def creating_session(self):
        """Aleatoriza los grupos en cada ronda."""
        if self.round_number == 1:
            self.session.vars['group_matrix'] = self.get_group_matrix()
        else:
            new_matrix = self.get_group_matrix()
            import random
            random.shuffle(new_matrix)  # Mezcla los jugadores
            self.set_group_matrix(new_matrix)

class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    
    def set_payoffs(self):
        """Calcula las contribuciones y pagos individuales."""
        players = self.get_players()
        self.total_contribution = sum([p.contribution for p in players])
        self.individual_share = (self.total_contribution * C.MULTIPLIER) / C.PLAYERS_PER_GROUP
        
        for p in players:
            p.payoff = C.ENDOWMENT - p.contribution + self.individual_share

class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=C.ENDOWMENT, label="¿Cuánto deseas contribuir?"
    )

    def total_payoff(self):
        """Calcula el pago total del jugador en todas las rondas."""
        return sum([p.payoff for p in self.in_all_rounds()])

# FUNCTIONS
def set_payoffs(group: Group):
    """Asigna pagos después de que todos contribuyan."""
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = (group.total_contribution * C.MULTIPLIER) / C.PLAYERS_PER_GROUP
    for p in players:
        p.payoff = C.ENDOWMENT - p.contribution + group.individual_share

# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class Results(Page):
    def vars_for_template(self):
        return {
            "total_contribution": self.group.total_contribution,
            "individual_share": self.group.individual_share,
            "payoff": self.payoff  # ✅ Corregido: Se usa `self.payoff`, no `self.player.payoff`
        }

# class FinalResults(Page):
#     """Muestra el pago total acumulado al final del experimento"""
#     def is_displayed(self):
#         """Solo se muestra en la última ronda"""
#         return self.round_number == C.NUM_ROUNDS

#     def vars_for_template(self):
#         """Calcula el pago total final del jugador"""
#         return {
#             "total_payoff": self.total_payoff()  # ✅ Corregido: Se usa `self.payoff`, no `self.player.payoff`
#         }

page_sequence = [Contribute, ResultsWaitPage, Results]





# from otree.api import *

# class C(BaseConstants):
#     NAME_IN_URL = 'public_goods_simple'
#     PLAYERS_PER_GROUP = 3  # 3 jugadores por grupo
#     NUM_ROUNDS = 4  # 4 rondas del juego
#     ENDOWMENT = cu(100)  # Dotación inicial de cada jugador
#     MULTIPLIER = 2.4  # Factor de multiplicación del fondo común

# class Subsession(BaseSubsession):
#     def creating_session(self):
#         """Aleatoriza los grupos en cada ronda."""
#         if self.round_number == 1:
#             self.session.vars['group_matrix'] = self.get_group_matrix()
#         else:
#             new_matrix = self.get_group_matrix()
#             import random
#             random.shuffle(new_matrix)  # Mezcla los jugadores
#             self.set_group_matrix(new_matrix)

# class Group(BaseGroup):
#     total_contribution = models.CurrencyField()
#     individual_share = models.CurrencyField()
    
#     def set_payoffs(self):
#         """Calcula las contribuciones y pagos individuales."""
#         players = self.get_players()
#         self.total_contribution = sum([p.contribution for p in players])
#         self.individual_share = (self.total_contribution * C.MULTIPLIER) / C.PLAYERS_PER_GROUP
        
#         for p in players:
#             p.payoff = C.ENDOWMENT - p.contribution + self.individual_share

# class Player(BasePlayer):
#     contribution = models.CurrencyField(
#         min=0, max=C.ENDOWMENT, label="¿Cuánto deseas contribuir?"
#     )

#     def total_payoff(self):
#         """Calcula el pago total del jugador en todas las rondas."""
#         return sum([p.payoff for p in self.in_all_rounds()])

# # FUNCTIONS
# def set_payoffs(group: Group):
#     """Asigna pagos después de que todos contribuyan."""
#     players = group.get_players()
#     contributions = [p.contribution for p in players]
#     group.total_contribution = sum(contributions)
#     group.individual_share = (group.total_contribution * C.MULTIPLIER) / C.PLAYERS_PER_GROUP
#     for p in players:
#         p.payoff = C.ENDOWMENT - p.contribution + group.individual_share

# # PAGES
# class Contribute(Page):
#     form_model = 'player'
#     form_fields = ['contribution']

# class ResultsWaitPage(WaitPage):
#     after_all_players_arrive = set_payoffs

# class Results(Page):
#     def vars_for_template(self):
#         return {
#             "total_contribution": self.group.total_contribution,
#             "individual_share": self.group.individual_share,
#             "payoff": self.payoff  # ✅ Corregido: Se usa `self.payoff`, no `self.player.payoff`
#         }

# class FinalResults(Page):
#     """Muestra el pago total acumulado al final del experimento"""
#     def is_displayed(self):
#         """Solo se muestra en la última ronda"""
#         return self.round_number == C.NUM_ROUNDS

#     def vars_for_template(self):
#         """Calcula el pago total final del jugador"""
#         return {
#             "total_payoff": self.payoff  # ✅ Corregido: Se usa `self.payoff`, no `self.player.payoff`
#         }

# page_sequence = [Contribute, ResultsWaitPage, Results, FinalResults]

