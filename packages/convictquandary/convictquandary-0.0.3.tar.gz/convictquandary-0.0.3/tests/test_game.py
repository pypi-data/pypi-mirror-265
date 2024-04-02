from convictquandary import Game, Player
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
