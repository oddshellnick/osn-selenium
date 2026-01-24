from osn_selenium.javascript.fingerprint.registry.models import RegistryItem
from osn_selenium.javascript.fingerprint.registry._functions import create_registry


__all__ = ["FINGERPRINT_REGISTRY", "RegistryItem"]

FINGERPRINT_REGISTRY = create_registry()
