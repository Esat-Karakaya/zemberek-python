from threading import Lock
from typing import Dict, Set, Union

from zemberek.core.turkish.phonetic_attribute import PhoneticAttribute


class AttributeToSurfaceCache:

    def __init__(self):
        self.attribute_map: Dict[int, str] = {}
        self.lock = Lock()

    def add_surface(self, attributes: Set[PhoneticAttribute], surface: str):
        """
        Uses a frozenset of attributes as the key for better performance.
        """
        key = frozenset(attributes)
        with self.lock:
            self.attribute_map[key] = surface

    def get_surface(self, attributes: Set[PhoneticAttribute]) -> Union[str, None]:
        """
        Uses a frozenset of attributes as the key for better performance.
        """
        return self.attribute_map.get(frozenset(attributes))
