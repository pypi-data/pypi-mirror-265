from abc import ABC, abstractmethod

from .constants import Action, Belief, Persuasion


class PlayerLogic(ABC):

    @abstractmethod
    def get_persuasion(
        self,
        player_actions: list[Action],
        player_persuasions: list[Persuasion],
        player_beliefs: list[Belief],
        opponent_actions: list[Action],
        opponent_persuasions: list[Persuasion],
    ) -> Persuasion:
        pass  # pragma: no cover

    @abstractmethod
    def get_belief(
        self,
        player_actions: list[Action],
        player_persuasions: list[Persuasion],
        player_beliefs: list[Belief],
        opponent_actions: list[Action],
        opponent_persuasions: list[Persuasion],
    ) -> Belief:
        pass  # pragma: no cover

    @abstractmethod
    def get_action(
        self,
        player_actions: list[Action],
        player_persuasions: list[Persuasion],
        player_beliefs: list[Belief],
        opponent_actions: list[Action],
        opponent_persuasions: list[Persuasion],
    ) -> Action:
        pass  # pragma: no cover
