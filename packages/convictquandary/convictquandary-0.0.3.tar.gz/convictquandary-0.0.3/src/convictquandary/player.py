from .constants import Action, Persuasion
from .player_logic import PlayerLogic


class Player:

    def __init__(self, player_logic: PlayerLogic) -> None:
        self.player_logic = player_logic()
        self.actions = list()
        self.persuasions = list()
        self.beliefs = list()
        self.opponent_actions = list()
        self.opponent_persuasions = list()
        self.score = 0

    def get_persuasion(self) -> Persuasion:
        player_persuasion = self.player_logic.get_persuasion(
            self.actions,
            self.persuasions,
            self.beliefs,
            self.opponent_actions,
            self.opponent_persuasions,
        )
        self.persuasions.append(player_persuasion)
        return player_persuasion

    def play_move(self, opponent_persuasion: Persuasion) -> Action:
        self.opponent_persuasions.append(opponent_persuasion)
        player_belief = self.player_logic.get_belief(
            self.actions,
            self.persuasions,
            self.beliefs,
            self.opponent_actions,
            self.opponent_persuasions,
        )
        player_action = self.player_logic.get_action(
            self.actions,
            self.persuasions,
            self.beliefs,
            self.opponent_actions,
            self.opponent_persuasions,
        )
        self.beliefs.append(player_belief)
        self.actions.append(player_action)
        return player_action

    def save_outcome(self, opponent_move: Action, score: int) -> None:
        self.opponent_actions.append(opponent_move)
        self.score += score
