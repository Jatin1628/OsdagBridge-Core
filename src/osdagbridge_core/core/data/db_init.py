"""
Database initialization and self-healing utilities for OsdagBridge Core.

Ensures that required SQLite databases (both for OsdagBridge Core and its
dependency osdag_core) exist and are populated with tables from the bundled
SQL files upon startup using standard Python package resource resolution.
"""

from importlib.resources import files, as_file
from pathlib import Path
import sqlite3
import logging

logger = logging.getLogger("osdagbridge_core.db_init")


def _has_tables(sqlitepath: Path) -> bool:
    """Check if the SQLite database contains at least one table."""
    try:
        conn = sqlite3.connect(str(sqlitepath))
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM sqlite_master WHERE type='table' LIMIT 1")
        row = cur.fetchone()
        conn.close()
        return row is not None
    except Exception:
        return False


def ensure_osdagbridge_db() -> bool:
    """Build the OsdagBridge Core Intg_osdag.sqlite database if missing or empty.

    Uses importlib.resources to locate the bundled SQL script from the installed package.
    Returns True if the database is available and valid, False otherwise.
    """
    try:
        # Resolve assets from the package environment using importlib.resources
        data_pkg = files("osdagbridge_core.core.data").joinpath("ResourceFiles")
        sql_resource = data_pkg.joinpath("Intg_osdag.sql")
        sqlite_resource = data_pkg.joinpath("Intg_osdag.sqlite")

        if not sql_resource.is_file():
            logger.warning("OsdagBridge Intg_osdag.sql not found in package resources.")
            return False

        with as_file(sqlite_resource) as sqlitepath:
            # If the database already exists and has tables, nothing to do
            if sqlitepath.exists() and sqlitepath.stat().st_size > 0 and _has_tables(sqlitepath):
                return True

            sql_content = sql_resource.read_text(encoding="utf-8")
            conn = sqlite3.connect(str(sqlitepath))
            conn.executescript(sql_content)
            conn.close()
            logger.info(f"Initialized OsdagBridge SQLite database at {sqlitepath}")
            return True
    except Exception as e:
        logger.warning(f"Could not initialize OsdagBridge database: {e}")
        return False


def ensure_osdag_core_db() -> bool:
    """Build the upstream osdag_core SQLite database if missing or 0 bytes.

    The installed `osdag` conda package ships a 0-byte placeholder
    `Intg_osdag.sqlite`. When queried via osdag_core.Common, lookups fail
    with "no such table: Beams/Angles". Populating the database prevents
    these warnings and runtime errors.
    """
    try:
        db_dir = files("osdag_core.data.ResourceFiles.Database")
        sql_resource = db_dir.joinpath("Intg_osdag.sql")
        sqlite_resource = db_dir.joinpath("Intg_osdag.sqlite")

        if not sql_resource.is_file():
            return False

        with as_file(sqlite_resource) as sqlitepath:
            if sqlitepath.exists() and sqlitepath.stat().st_size > 0 and _has_tables(sqlitepath):
                return True

            sql_content = sql_resource.read_text(encoding="utf-8")
            conn = sqlite3.connect(str(sqlitepath))
            conn.executescript(sql_content)
            conn.close()
            logger.info(f"Initialized osdag_core SQLite database at {sqlitepath}")
            return True
    except Exception as e:
        # Non-fatal if osdag_core is not installed or installed in a read-only path
        logger.debug(f"osdag_core DB setup skipped: {e}")
        return False


def ensure_all_databases() -> None:
    """Ensure both osdag_core and OsdagBridge Core databases are initialized."""
    # Initialize osdag_core first so subsequent imports of osdag_core do not warn
    ensure_osdag_core_db()
    ensure_osdagbridge_db()
