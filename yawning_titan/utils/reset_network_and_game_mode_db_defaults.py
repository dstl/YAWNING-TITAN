def run(rebuild: bool = False):
    """
    Force a reset of the default entries in the NetworkDB and GameModeDB.

    :param rebuild: If True, completely rebuild the DB, removing all custom
        Networks and GameModes. Default value is False.
    """

    from yawning_titan.game_modes.game_mode_db import GameModeDB

    """Forces a reset of the default entries in the NetworkDB and GameModeDB."""
    from yawning_titan.networks.network_db import NetworkDB

    network_db = NetworkDB()
    game_mode_db = GameModeDB()

    if rebuild:
        network_db.rebuild_db()
        game_mode_db.rebuild_db()
    else:
        network_db.reset_default_networks_in_db(force=True)
        game_mode_db.reset_default_game_modes_in_db(force=True)


if __name__ == "__main__":
    run(True)
