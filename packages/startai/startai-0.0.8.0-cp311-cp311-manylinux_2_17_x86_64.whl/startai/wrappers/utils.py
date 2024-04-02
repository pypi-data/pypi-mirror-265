import os
import logging
import json
from urllib import request
import importlib
import startai

folder_path = os.sep.join(__file__.split(os.sep)[:-3])
wrappers_path = os.path.join(folder_path, "wrappers.json")
if os.path.exists(wrappers_path):
    wrappers = json.loads(open(wrappers_path).read())
wrapers_dir = os.path.join(folder_path, "startai/wrappers")


def download_cython_wrapper(func_name: str):
    """Get the wrapper for the given function name."""
    if func_name + ".so" not in wrappers["startai"]["functional"]:
        logging.warning(f"Wrapper for {func_name} not found.")
        return False
    try:
        response = request.urlopen(
            "https://raw.githubusercontent.com/khulnasoft"
            + "/binaries/cython_wrappers/wrappers/"
            + func_name
            + ".so"
        )
        os.makedirs(wrapers_dir, exist_ok=True)
        with open(os.path.join(wrapers_dir, func_name + ".so"), "wb") as f:
            f.write(response.read())
        print("Downloaded wrapper for " + func_name)
        return True
    except request.HTTPError:
        logging.warning(f"Unable to download wrapper for {func_name}.")
        return False


def wrapper_exists(func_name: str):
    """Check if the wrapper for the given function name exists."""
    return func_name + ".so" in wrappers["startai"]["functional"]


def load_one_wrapper(func_name: str):
    """Load the wrapper for the given function name."""
    module_name = func_name
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # check if file exists
    if os.path.isfile(os.path.join(dir_path, module_name + ".so")):
        startai.wrappers.__dict__[module_name] = importlib.import_module(module_name)
        startai.wrappers.__dict__[module_name + "_wrapper"] = getattr(
            startai.wrappers.__dict__[module_name], module_name + "_wrapper"
        )
        startai.wrappers.__all__.append(module_name + "_wrapper")
        return True
    else:
        return False
