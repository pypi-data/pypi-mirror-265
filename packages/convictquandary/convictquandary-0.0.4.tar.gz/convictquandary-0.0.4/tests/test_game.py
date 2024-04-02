import pytest

from convictquandary import Game, Player, utils
from convictquandary.player_logics import (
    LogicAlwaysCooperateBelieveTruth,
    LogicAlwaysDefectBelieveTruth,
)


def test_1v1_game_always_defect_win():
    player1 = Player(LogicAlwaysCooperateBelieveTruth)
    player2 = Player(LogicAlwaysDefectBelieveTruth)
    game = Game(player1, player2, 200)
    game.play_game()
    assert game.get_game_result() == (
        0,
        1000,
    ), "Always defect not winning against always cooperate"


def test_1v1_game_always_defect_against_itself():
    player1 = Player(LogicAlwaysDefectBelieveTruth)
    player2 = Player(LogicAlwaysDefectBelieveTruth)
    game = Game(player1, player2, 200)
    game.play_game()
    assert game.get_game_result() == (0, 0), "Always defect against itself not 0"


def test_1v1_game_always_cooperate_against_itself():
    player1 = Player(LogicAlwaysCooperateBelieveTruth)
    player2 = Player(LogicAlwaysCooperateBelieveTruth)
    game = Game(player1, player2, 200)
    game.play_game()
    assert game.get_game_result() == (600, 600), "Always cooperate not score 600"


def test_1v1_game_get_players():
    player1 = Player(LogicAlwaysCooperateBelieveTruth)
    player2 = Player(LogicAlwaysCooperateBelieveTruth)
    game = Game(player1, player2, 200)
    p1, p2 = game.get_players()
    assert (p1, p2) == (player1, player2), "Game returns correct players"


def test_1v1_game_already_played():
    player1 = Player(LogicAlwaysCooperateBelieveTruth)
    player2 = Player(LogicAlwaysCooperateBelieveTruth)
    game = Game(player1, player2, 200)
    game.play_game()
    with pytest.raises(ValueError, match="Game already finished"):
        game.play_game()


def test_utils_exception_factory():
    with pytest.raises(ValueError, match="Test message"):
        raise utils.exception_factory(ValueError, "Test message")
