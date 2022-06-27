import logging

from gym.envs.registration import register

logger = logging.getLogger("yawning_titan")

register(id="five-node-def-v0", entry_point="yawning_titan.envs.specific:FiveNodeDef")

register(id="four-node-def-v0", entry_point="yawning_titan.envs.specific:FourNodeDef")

register(
    id="network-graph-explore-v0",
    entry_point="yawning_titan.envs.specific:GraphExplore",
)

register(id="18-node-env-v0", entry_point="yawning_titan.envs.specific:NodeEnv")
