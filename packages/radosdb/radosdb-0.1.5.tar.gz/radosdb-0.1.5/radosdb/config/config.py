import os
import types

import yaml

from ..common.helper.env import Env, EnvConst
from ..common.tools import get_logger

logger = get_logger(os.path.basename(__file__))

_config_cache = {}

def parse_config(name=None, path=None, env=None, file_name=None):
    if isinstance(path, types.ModuleType):
        path = os.path.dirname(os.path.abspath(path.__file__))
    if path is None:
        path = Env[EnvConst.config_path]
        if path is None:
            path = os.path.dirname(os.path.abspath(__file__))
    if file_name is None:
        if env is None:
            env = Env[EnvConst.compute_platform_env]
            if env is None:
                env_config_path = os.path.join(path, "config.yaml")
                if os.path.exists(env_config_path):
                    with open(env_config_path) as file:
                        env_config = yaml.safe_load(file)
                        env = env_config.get("env", "dev")
                else:
                    env = "dev"
        file_name = f"config.{env}.yaml"

    path = os.path.abspath(os.path.join(path, file_name))
    config = _config_cache.get(path)
    if config is None:
        logger.info(f"read config: %s", path)
        with open(path) as file:
            config = yaml.safe_load(file)
            _config_cache[path] = config
    if name is None:
        return config
    return config.get(name, {})


