from ..constants import Action, Belief, Persuasion
from ..player_logic import PlayerLogic


class LogicAlwaysDefectBelieveTruth(PlayerLogic):

    def get_persuasion(
        self,
        player_actions: list[Action],
        player_persuasions: list[Persuasion],
        player_beliefs: list[Belief],
        opponent_actions: list[Action],
        opponent_persuasions: list[Persuasion],
    ) -> Persuasion:
        return Persuasion.TRUTH

    def get_belief(
        self,
        player_actions: list[Action],
        player_persuasions: list[Persuasion],
        player_beliefs: list[Belief],
        opponent_actions: list[Action],
        opponent_persuasions: list[Persuasion],
    ) -> Belief:
        return Belief.BELIEVE

    def get_action(
        self,
        player_actions: list[Action],
        player_persuasions: list[Persuasion],
        player_beliefs: list[Belief],
        opponent_actions: list[Action],
        opponent_persuasions: list[Persuasion],
    ) -> Action:
        return Action.DEFECT
