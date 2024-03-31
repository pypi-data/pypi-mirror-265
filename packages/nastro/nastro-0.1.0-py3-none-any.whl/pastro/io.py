from .types import CartesianState, KeplerianState, Vector
import numpy as np
from typing import overload
from pathlib import Path


def save(state: CartesianState | KeplerianState, path: Path | str) -> None:
    """Save state to file

    :param state: State to save
    :param path: Path to save the state
    """

    np.save(path, state.asarray())

    return None


@overload
def load(path: Path | str, type: type[CartesianState]) -> CartesianState: ...


@overload
def load(
    path: Path | str, type: type[KeplerianState], deg: bool = False
) -> KeplerianState: ...


@overload
def load(path: Path | str, type: type[Vector]) -> Vector: ...


def load(path, type, deg=False):

    data = np.load(path)
    if type == CartesianState:
        return CartesianState(*data)
    elif type == KeplerianState:
        return KeplerianState(*data, deg=deg)
    elif type == Vector:
        return np.array(data, dtype=np.float64)
    else:
        raise ValueError("Invalid type")
