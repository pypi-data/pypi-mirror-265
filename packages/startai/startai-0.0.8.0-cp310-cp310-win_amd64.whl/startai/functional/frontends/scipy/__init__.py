# global
import sys
import startai

# local
from startai.functional.frontends import set_frontend_to_specific_version
from . import cluster
from . import constants
from . import fft
from . import fftpack
from . import integrate
from . import interpolate
from . import linalg
from . import ndimage
from . import odr
from . import optimize
from . import signal
from . import sparse
from . import spatial
from . import special
from . import stats

import startai.functional.frontends.numpy as np


array = _frontend_array = np.array

# setting to specific version #
# --------------------------- #

if startai.is_local():
    module = startai.utils._importlib.import_cache[__name__]
else:
    module = sys.modules[__name__]

set_frontend_to_specific_version(module)
