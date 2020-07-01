from ave import AVE, config


def run():
    ave = AVE()
    ave.load_games(config.games_folder)
    ave.start()
