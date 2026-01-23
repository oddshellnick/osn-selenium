from osn_selenium.javascript.fingerprint.registry.types import RegistryItem
from osn_selenium.javascript.fingerprint.registry._functions import create_registry


__all__ = ["FINGERPRINT_REGISTRY"]

FINGERPRINT_REGISTRY = create_registry()
