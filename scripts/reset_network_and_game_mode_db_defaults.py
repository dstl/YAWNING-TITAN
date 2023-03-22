"""Forces a reset of the default entries in the NetworkDB and GameModeDB."""

from yawning_titan.game_modes.game_mode_db import GameModeDB
from yawning_titan.networks.network_db import NetworkDB

network_db = NetworkDB()
network_db.reset_default_networks_in_db(force=True)

game_mode_db = GameModeDB()
game_mode_db.reset_default_game_modes_in_db(force=True)
