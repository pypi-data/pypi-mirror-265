from __future__ import annotations

import os
from typing import TypeVar, Self, Callable, Generic, Union
from inspect import get_annotations


C = TypeVar("C")


class Context(Generic[C]):

    instances: dict[str, C] = None

    def env(self, key):
        key = f"{self.context_name}_{key}" if self.context_name else key
        return os.getenv(key)

    def __init__(self, context_name: str) -> None:
        super().__init__()
        self.context_name = context_name
        cls = self.__class__
        for key, annotation in get_annotations(cls).items():
            value = getattr(cls, key)
            if isinstance(value, Auto):
                value.get_instance(context_name)

    @classmethod
    def factory(cls, context_name: str) -> C:
        return cls(context_name)

    @classmethod
    def instance(cls, context_name: str = None) -> C:
        if cls.instances is None:
            cls.instances = {}
        return cls.instances.setdefault(
            context_name, cls.factory(context_name))


A = TypeVar("A", bound=Context)

class Auto(Generic[A, C]):

    def __init__(
        self,
        context_type: A,
        context_name: str = None,
        instance_type: type[C] = None,
        instance_factory: Callable[[str], C] = None
    ) -> None:
        self.context_type = context_type
        self.context_name = context_name
        self.instance_type = instance_type
        self.instance_factory = instance_factory

    def get_instance(self, parent_context_name: str) -> C:
        context_name = self.context_name or parent_context_name

        if self.instance_factory:
            return self.instance_factory(context_name)

        return self.context_type.instance(context_name)
