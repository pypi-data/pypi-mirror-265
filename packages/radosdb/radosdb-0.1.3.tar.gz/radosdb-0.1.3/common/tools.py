from __future__ import annotations

import functools
import importlib
import inspect
import itertools
import json
import logging
import os
import re
import sys
import threading
import traceback
import typing
from logging.handlers import TimedRotatingFileHandler

import numpy as np
import requests
from requests import HTTPError

from .helper.env import EnvConst


def get_file_handler_to_logger(to_file, encoding=None):
    return TimedRotatingFileHandler(filename=f"log/{to_file}", when="D", backupCount=3, encoding=encoding)


def get_logger(name=None, to_file=None, encoding=None, level=(logging.INFO, logging.DEBUG)):
    if name is None or isinstance(name, str):
        logger = logging.getLogger(name=name)
        if len(logger.handlers) > 0:
            logger.handlers.clear()
    else:
        logger = name
    name = logger.name

    if level is None:
        level = (logging.INFO, logging.INFO)
    if isinstance(level, int):
        level = (level, level)
    if isinstance(level, tuple):
        if len(level) == 1:
            level = (level[0], level[0])

    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter("%(asctime)s\t%(levelname)s %(filename)s:%(lineno)s -- %(message)s")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level[0])
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if to_file is None:
        to_file = EnvConst.log_to_file.env

    if isinstance(to_file, bool):
        if to_file:
            to_file = f"{name}.log"
        else:
            to_file = None
    if to_file == "":
        to_file = None
    if to_file is not None:
        if not os.path.exists("log"):
            os.makedirs("log")
        fh = get_file_handler_to_logger(to_file, encoding)
        fh.setLevel(level[1])
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


logger = get_logger(os.path.basename(__file__))


class Result:
    def __init__(self, prop: str = None, handler=None):
        self.prop = prop
        self.handler = handler

    def handle_response(self, response):
        if response.ok:
            try:
                data = response.json()
            except (json.JSONDecodeError, requests.JSONDecodeError) as e:
                return response.text

            if self.prop is not None:
                data = data.get(self.prop, None)
            if self.handler is not None:
                data = self.handler(data)
            return data
        message = None
        try:
            error = response.json()
            message = error.get("message", error.get("error", {}).get("status"))

            if message is None or message == "":
                message = error.get("type")
        except Exception:
            pass
        if message is None:
            message = response.text
        raise HTTPError("%s, %s" % (response.status_code, str(message)), request=response.request, response=response)

    def __call__(self, fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            return self.handle_response(fun(*args, **kwargs))

        return wrapper


class Address:
    def __init__(self, host, port=None, db=None):
        if port is None:
            split = host.split(":")
            host = split[0]
            if len(split) < 2:
                port = "80"
            else:
                port = split[1]
            if len(split) > 3:
                db = split[2]

        self.host = str(host)
        self.port = port
        self.db = db

    def __str__(self):
        return f"{self.host}:{self.port}"

    def encode(self, *args, **kwargs):
        return str(self).encode(*args, **kwargs)


def load_module(module, path=None):
    if path is None:
        path = module.__path__[0]
    if not isinstance(module, str):
        module = module.__name__
    for f in os.listdir(path):
        if f.endswith(".py"):
            name, fix = os.path.splitext(f)
            if name.startswith("__"):
                continue
            try:
                inspect.getmembers(importlib.import_module(f"{module}.{name}"), inspect.isclass)
            except Exception as e:
                logger.warning("load module(%s) error: %s", name, e)


def find_all_subclasses(cls: type):
    result = []
    for c in cls.__subclasses__():
        result.append(c)
        result.extend(find_all_subclasses(c))
    return result


def get_cls(cls, module):
    return getattr(importlib.import_module(module), cls)


def find_match_sub_cls(name: str, cls: type):
    for c in cls.__subclasses__():
        if c.__name__ == name:
            return get_cls(name, c.__module__)
        sc = find_match_sub_cls(name, c)
        if sc is not None:
            return sc
    return None

class DFS:
    def __init__(
        self,
        iterable: typing.Iterable,
        tree_node_type: typing.Union[typing.Tuple, typing.Type] = (list, tuple),
        is_tree_node: typing.Callable[[typing.Any], bool] = None,
        tree_node_map_to_stack_elements: typing.Callable[[typing.Any], typing.Iterable] = None,
    ):
        self.iterable = iterable
        self.stack = None
        self.reset()
        self.node_type = tree_node_type

        if is_tree_node is None:
            is_tree_node = lambda x: isinstance(x, self.node_type)
        if tree_node_map_to_stack_elements is None:
            tree_node_map_to_stack_elements = lambda x: reversed(x)

        self.is_tree_node = is_tree_node
        self.tree_node_map_to_stack_elements = tree_node_map_to_stack_elements

    def reset(self):
        self.stack = list(reversed(list(self.iterable)))

    def __iter__(self):
        return self

    def __next__(self):
        while len(self.stack) > 0:
            item = self.stack.pop()
            if self.is_tree_node(item):
                self.stack.extend(self.tree_node_map_to_stack_elements(item))
                continue
            return item
        raise StopIteration


class ZipDFS(DFS):
    def __init__(self, *iterable: typing.Iterable):
        super().__init__(
            iterable,
            is_tree_node=self._is_tree_node,
            tree_node_map_to_stack_elements=lambda x: reversed(list(zip(x[0], [x[1]] * len(x[0])))),
        )

    def reset(self):
        self.stack = list(reversed(list(zip(*self.iterable))))

    def _is_tree_node(self, item):
        return isinstance(item[0], self.node_type)
