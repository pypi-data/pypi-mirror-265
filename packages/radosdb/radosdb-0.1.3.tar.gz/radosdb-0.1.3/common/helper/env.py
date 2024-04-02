import os


class EnvMeta(type):
    def __new__(cls, n, b, a):
        return super().__new__(cls, n, b, a)

    @classmethod
    def get(cls, name, default=None):
        return os.getenv(name, default)

    @classmethod
    def get_int(cls, name, default=None):
        value = cls.get(name, default)
        if value is None:
            return None
        return int(value)

    @classmethod
    def set(cls, name, value):
        if name is None:
            raise ValueError(f"key {name} is not defined")
        if not isinstance(value, str):
            value = str(value)

        if value is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = value

    @classmethod
    def delete(cls, name):
        os.environ.pop(name, None)

    def __getitem__(self, item) -> str:
        return self.get(item)

    def __setitem__(self, name, value):
        self.set(name, value)

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, name, value):
        self.set(name, value)

    def __delattr__(self, name):
        self.delete(name)


class Env(metaclass=EnvMeta):
    def __init__(self, name):
        self.name = name

    def value(self) -> str:
        return Env[self.name]

    def set_value(self, value):
        Env[self.name] = value


class EnvItem(str):
    def __new__(cls, name):
        return super().__new__(cls, name)

    def get(self, default=None):
        return Env.get(self, default)

    def get_int(self, default=None):
        return Env.get_int(self, default)

    @property
    def env(self) -> str:
        return Env[self]

    @env.setter
    def env(self, value):
        Env[self] = value


class EnvConstMeta(type):
    def __new__(cls, n, b, a):
        return super().__new__(cls, n, b, a)

    def __getattribute__(self, item):
        if item.startswith("__"):
            return super().__getattribute__(item)
        if item in EnvConst.__dict__:
            return EnvItem(super().__getattribute__(item))
        return EnvItem(item)


class EnvConst(metaclass=EnvConstMeta):
    system_name = "radosdb"

    config_path = system_name + "config_path"

    compute_platform_env = f"{system_name}_env"

    computing_platform_address = f"{system_name}_address"
    server_address = f"{system_name}_cplat_address"

    horizon_server_address = "horizon_server_address"

    compute_platform_user = f"{system_name}_user"
    compute_platform_password = f"{system_name}_password"

    log_to_file = "LOG_TO_FILE"
