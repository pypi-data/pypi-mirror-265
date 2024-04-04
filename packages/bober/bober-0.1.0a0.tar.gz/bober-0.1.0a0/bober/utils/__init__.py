from __future__ import annotations

import yaml
from pathlib import Path
from functools import reduce


def read_yaml(path: Path):
    with path.open(mode='r', encoding='utf-8') as yaml_file:
        data = yaml.safe_load(yaml_file.read())
        return data if data else dict()


def merge_configs(configs: list[dict]) -> dict:
    return reduce(lambda left, right: deepmerge(left, right), configs)


def deepmerge(left: dict, right: dict, path=None):
    path = [] if path is None else path

    for key in right:
        if key in left:
            if isinstance(left[key], dict) and isinstance(right[key], dict):  # go deeper
                deepmerge(left[key], right[key], path + [str(key)])
            elif isinstance(left[key], type(right[key])):  # replace
                left[key] = right[key]
            else:
                raise Exception(f'Conflict at path: `{".".join(path + [str(key)])}`, '
                                f'incompatible types `{type(left[key])}` and `{type(right[key])}`')
        else:
            left[key] = right[key]  # merge

    return left
