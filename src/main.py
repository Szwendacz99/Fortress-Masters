from Game import Game

if __name__ == "__main__":
    game: Game = Game()
    game.curr_menu.display_menu()
    game.game_loop()