from packaging import version

from ._version import __version__

from .metrics import *

min_torch = '2.0'
assert version.parse(min_torch) <= version.parse(torch.__version__), \
    f'PyTorch=={torch.__version__} is used but incompatible. ' \
    f'Please install torch>={min_torch}.'