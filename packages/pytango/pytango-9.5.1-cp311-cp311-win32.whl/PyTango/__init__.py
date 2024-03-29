"""Provides PyTango as a module for backward compatibility."""


# start delvewheel patch
def _delvewheel_patch_1_5_4():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pytango.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_5_4()
del _delvewheel_patch_1_5_4
# end delvewheel patch

# Imports
import sys
import tango
import pkgutil


def alias_package(package, alias, extra_modules={}):
    """Alias a python package properly.

    It ensures that modules are not duplicated by trying
    to import and alias all the submodules recursively.
    """
    path = package.__path__
    alias_prefix = alias + "."
    prefix = package.__name__ + "."
    # Alias all importable modules recursively
    for _, name, _ in pkgutil.walk_packages(path, prefix):
        # Skip databaseds backends
        if name.startswith("tango.databaseds.db_access."):
            continue
        try:
            if name not in sys.modules:
                __import__(name)
        except ImportError:
            continue
        alias_name = name.replace(prefix, alias_prefix)
        sys.modules[alias_name] = sys.modules[name]
    # Alias extra modules
    for key, value in extra_modules.items():
        name = prefix + value
        if name not in sys.modules:
            __import__(name)
        if not hasattr(package, key):
            setattr(package, key, sys.modules[name])
        sys.modules[alias_prefix + key] = sys.modules[name]
    # Alias root module
    sys.modules[alias] = sys.modules[package.__name__]


# Do not flood pytango users console with warnings yet
# warnings.warn('PyTango module is deprecated, import tango instead.')

# Alias tango package
alias_package(
    package=tango,
    alias=__name__,
    extra_modules={"_PyTango": "_tango", "constants": "constants"},
)