# -*- coding: utf-8 -*-

"""
Copyright (c) 2021 Keijack Wu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import os
import sys
from naja_atra import Response
from naja_atra.utils.logger import get_logger
from jinja2 import Environment, FileSystemLoader
from typing import Dict

name = "naja-atra-jinja"
version = "1.0.2"

_logger = get_logger(name)

DEFAULT_TAG = "default"
ENVS: Dict[str, Environment] = {}


def set_env(env: Environment, tag: str = DEFAULT_TAG):
    ENVS[tag] = env


def get_main_module_dir() -> str:
    mpath = os.path.dirname(sys.modules['__main__'].__file__)
    _logger.debug(f"Path of module[main] is {mpath}")
    return mpath


def get_template_dir() -> str:
    template_path = os.path.join(get_main_module_dir(), "templates")
    if os.path.exists(template_path):
        return template_path
    template_path = os.path.join(os.getcwd(), "templates")
    if os.path.exists(template_path):
        return template_path
    raise FileNotFoundError(
        f"Cannot find templates directory, please create a directory named 'templates' in your project root directory")


def get_env(tag: str = DEFAULT_TAG) -> Environment:
    if tag not in ENVS:
        searchpath = get_template_dir()
        _logger.info(
            f"Cannot find env in tag[#{tag}], create a default one which templates should in {searchpath}")
        ENVS[tag] = Environment(loader=FileSystemLoader(searchpath))
    return ENVS[tag]


def render(name, variables: dict = {}, env_tag: str = DEFAULT_TAG) -> str:
    env = get_env(env_tag)
    tpl = env.get_template(name)
    return tpl.render(variables)


class JinjaView(Response):

    def __init__(self, name, variables: dict = {},
                 env_tag: str = DEFAULT_TAG,
                 status_code: int = 200,
                 headers: Dict[str, str] = None):
        super().__init__(status_code, headers, body=render(
            name, variables=variables, env_tag=env_tag))
