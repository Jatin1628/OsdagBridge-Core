"""Simple registry for codes"""
_registry = {
    "IRC:6-2017": __import__("osdagbridge_core.core.utils.codes.irc6_2017", fromlist=["*"]),
}
def get_code(key):
    return _registry.get(key)
