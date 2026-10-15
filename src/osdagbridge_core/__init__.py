"""
OsdagBridge Core
Computational, analysis and design engine for steel bridges.
"""

import importlib
import os
import sys

__version__ = "1.0.0"

# Extend package search path to include the 'core' directory.
# This allows direct submodule imports without the redundant '.core.':
#   e.g. `from osdagbridge_core.boq import calculate_material_quantities`
#   or   `from osdagbridge_core.reports import generate_report`
# while preserving backward compatibility for `from osdagbridge_core.core...`
_core_dir = os.path.join(os.path.dirname(__file__), "core")
if _core_dir not in __path__:
    __path__.append(_core_dir)

# Ensure databases are initialized (prevents missing table warnings and LookupErrors)
try:
    from osdagbridge_core.core.data.db_init import ensure_all_databases
    ensure_all_databases()
except Exception:
    pass

# Safe top-level exception export
from osdagbridge_core.core.exceptions import OsdagError

_SUBMODULES = {
    "boq",
    "bridge_components",
    "bridge_types",
    "exceptions",
    "ifc_export_bridge",
    "loads",
    "reports",
    "solvers",
    "utils",
}

__all__ = [
    "__version__",
    "OsdagError",
    "boq",
    "bridge_components",
    "bridge_types",
    "exceptions",
    "ifc_export_bridge",
    "loads",
    "reports",
    "solvers",
    "utils",
]


def __getattr__(name: str):
    """Lazy-load submodules when accessed as attributes on the root package.

    Enables `from osdagbridge_core import bridge_types, boq, reports`
    without eagerly loading heavy optional dependencies (e.g. OCC or OpenSees)
    at root package import time.
    """
    if name in _SUBMODULES:
        core_mod = importlib.import_module(f".core.{name}", package=__name__)
        sys.modules[f"{__name__}.{name}"] = core_mod
        globals()[name] = core_mod
        return core_mod
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__():
    return sorted(list(globals().keys()) + list(_SUBMODULES))
