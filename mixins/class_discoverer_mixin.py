import importlib
from pathlib import Path
from typing import TypeVar, Dict, Type

from packages.extensions.string_extensions import StringExtensions

T = TypeVar("T")


class ClassDiscovererMixin:
    def __init__(self, generic_constraint: Type[T], root_dir: str, files_pattern: str, class_suffix: str):
        self._entity_base_class = generic_constraint
        self._files_pattern = files_pattern
        self._root_dir = root_dir
        self._class_suffix = class_suffix
        self._types: Dict[str, Type[T]] = {}
        self._discover_types()

    def get_class(self, name: str) -> Type[T]:
        return self._types.get(name.lower())

    def _discover_types(self):
        """Discover all subclasses using reflection."""
        if self._types:
            return

        self._preload_types()
        for subclass in self._entity_base_class.__subclasses__():
            class_name = subclass.__name__
            if class_name.endswith(self._class_suffix):
                entity_name = StringExtensions.to_snake_case(class_name[:-len(self._class_suffix)]).lower()
                self._types[entity_name] = subclass

    def _preload_types(self):
        root_resolved_path = Path(self._root_dir).resolve()
        for py_file in root_resolved_path.rglob(self._files_pattern):
            try:
                rel_path = py_file.relative_to(root_resolved_path)
                module_name = ".".join(rel_path.with_suffix("").parts)
                importlib.import_module(module_name)
            except (ImportError, ValueError):
                pass
