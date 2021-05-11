import os
import sys
import numpy as np
from typing import Union, Any

if sys.version_info[:2] >= (3, 8):
    from typing import Final, Literal  # noqa: F401
else:
    from typing_extensions import Final, Literal  # noqa: F401

# os.PathLike only becomes subscriptable from Python 3.9 onwards
if sys.version_info[:2] < (3, 9):
    PathLike = Union[str, os.PathLike]
elif sys.version_info[:2] >= (3, 9):
    PathLike = Union[str, os.PathLike[str]]

TBD = Any

try:
    floatArray = np.ndarray[float]  # type: ignore
except Exception:
    floatArray = np.ndarray         # type: ignore
