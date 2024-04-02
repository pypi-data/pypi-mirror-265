import sys


import startai.functional.frontends.torch as torch
import startai
from startai.functional.frontends import set_frontend_to_specific_version


from . import ops


tensor = _frontend_array = torch.tensor


# setting to specific version #
# --------------------------- #

if startai.is_local():
    module = startai.utils._importlib.import_cache[__name__]
else:
    module = sys.modules[__name__]

set_frontend_to_specific_version(module)
