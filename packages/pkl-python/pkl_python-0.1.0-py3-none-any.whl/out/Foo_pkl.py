# Code generated from Pkl module `Foo`. DO NOT EDIT.
from typing import Dict, List, Literal, Optional, Union
from dataclasses import dataclass
import pkll

_NO_DEFAULT = object()

@dataclass
class Animal(Being):
    name: str = _NO_DEFAULT

    _registered_identifier: str = "Foo#Animal"

    def __post_init__(self):
        no_default_list = [("name", self.name)]
        for n, x in no_default_list:
            if x is _NO_DEFAULT:
                raise TypeError(f"__init__ missing 1 required argument: '{n}'")

@dataclass
class Being:
    exists: bool

    _registered_identifier: str = "Foo#Being"

@dataclass
class Bird(Animal):
    flies: bool = _NO_DEFAULT

    _registered_identifier: str = "Foo#Bird"

    def __post_init__(self):
        no_default_list = [("flies", self.flies)]
        for n, x in no_default_list:
            if x is _NO_DEFAULT:
                raise TypeError(f"__init__ missing 1 required argument: '{n}'")

@dataclass
class Dog(Animal):
    barks: bool = _NO_DEFAULT

    _registered_identifier: str = "Foo#Dog"

    def __post_init__(self):
        no_default_list = [("barks", self.barks)]
        for n, x in no_default_list:
            if x is _NO_DEFAULT:
                raise TypeError(f"__init__ missing 1 required argument: '{n}'")

@dataclass
class Foo:
    animals: List[Animal]

    _registered_identifier: str = "Foo"

    @classmethod
    def load_pkl(cls, source: str):
        # Load the Pkl module at the given source and evaluate it into `Foo.Module`.
        # - Parameter source: The source of the Pkl module.
        config = pkll.load(source)
        return cls(**config._asdict())