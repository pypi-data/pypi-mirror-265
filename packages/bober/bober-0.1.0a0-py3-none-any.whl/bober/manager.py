from __future__ import annotations

import json
from pathlib import Path
from bober.utils import merge_configs, read_yaml

FOREST = {}


class Bober:
    def __init__(
            self,
            *,
            cfg_common: str | Path | dict = None,
            cfg_embedded: str | Path | dict = None,
            cfg_external: str | Path | dict = None,
            output_path: str | Path = None,
    ):
        self._cfg_common = Bober._load_config(cfg_common)
        self._cfg_embedded = Bober._load_config(cfg_embedded)
        self._cfg_external = Bober._load_config(cfg_external)

        self._config = merge_configs([
            self._cfg_common,
            self._cfg_embedded,
            self._cfg_external,
        ])
        self._output_path = output_path

    def go(self, name: str):
        func = FOREST.get(name)
        if not func:
            raise ValueError(f'There is no wood with name {name} in the forest!')

        result = func(self._config) if self._config else func()

        if result and self._output_path:
            self._save_result(result)

        return result

    @property
    def config(self) -> dict:
        return self._config

    def __call__(self, *args, **kwargs):
        return self.go(*args, **kwargs)

    def _save_result(self, result) -> None:

        if str(self._output_path).startswith('/'):
            with Path(self._output_path).open('w') as file:
                json.dump(result, file)
        elif str(self._output_path).startswith('s3://'):
            raise NotImplementedError('S3 is not supported yet!')
        else:
            raise ValueError(f'Arg `output_path` must be `local` or `S3` path: `{self._output_path}`!')

    @staticmethod
    def _load_config(config: str | Path | dict) -> dict:
        if isinstance(config, Path):
            config = str(config)

        if config is None:
            return {}
        elif type(config) is dict:
            return config
        elif type(config) is str:
            if config.startswith('/'):
                return read_yaml(Path(config))
            elif config.startswith('s3://'):
                raise NotImplementedError('S3 is not supported yet!')
            else:
                return json.loads(config)
        else:
            raise ValueError(f'Arg `config` has unsupported type `{type(config)}`!')
