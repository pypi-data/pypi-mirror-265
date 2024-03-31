from ...types import KeplerianState
import numpy as np
from pathlib import Path

def load_keplerian_elements():
    
    current_dir = Path(__file__).resolve().parent
    data = np.load(current_dir.parent / "data/kepler_elements.npy").T
    time = data[0]
    kstate = KeplerianState(data[1], data[2], data[3],
                            data[5], data[4], data[6])
    
    return time, kstate


def test_subtraction() -> None:

    assert False
   
    return None