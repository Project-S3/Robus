import sys
import pathlib
import importlib
import os

PROJECT_BASE_PATH = pathlib.Path(r"D:/robus")
# Needed to use import in blender
sys.path.append(str(PROJECT_BASE_PATH))
sys.path.append(str(os.path.join(PROJECT_BASE_PATH, pathlib.Path("venv/lib/site-packages"))))

import robus


def is_reloadable_module(module):
    if not hasattr(module, "__file__"): return False
    if module.__file__ is None: return False
    file_path = pathlib.Path(module.__file__)
    return file_path.is_relative_to(PROJECT_BASE_PATH) \
           and not file_path.is_relative_to(PROJECT_BASE_PATH.joinpath("venv")) \
           and module.__name__ != "__main__"


def reload_module():
    modules_to_reload = list(filter(is_reloadable_module, sys.modules.values()))
    for i in range(len(modules_to_reload)):
        m = modules_to_reload[i]
        importlib.reload(m)
        print(f"RELOAD MODULE: {m.__name__}")


if __name__ == '__main__':
    reload_module()
    robus.main()



