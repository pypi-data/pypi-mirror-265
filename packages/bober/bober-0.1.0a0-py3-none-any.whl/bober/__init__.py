from __future__ import annotations

from pathlib import Path
from bober.manager import Bober
from bober.integration.decorators import wood

__version__ = "0.1.0.alpha"


def setup(
        *,
        cfg_common: str | Path | dict = None,
        cfg_embedded: str | Path | dict = None,
        cfg_external: str | Path | dict = None,
        output_path: str | Path = None
) -> Bober:
    return Bober(
        cfg_common=cfg_common,
        cfg_embedded=cfg_embedded,
        cfg_external=cfg_external,
        output_path=output_path
    )


__all__ = [
    'Bober',
    'wood'
]
