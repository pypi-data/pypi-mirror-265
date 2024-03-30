# Code generated from Pkl module `com.example.Simple`. DO NOT EDIT.
from enum import Enum
from typing import Dict, List, Literal, Optional, Union
from dataclasses import dataclass
import pkll

_NO_DEFAULT = object()

@dataclass
class Person:
    # The name of the person
    the_name: str

    # Some name that matches a keyword
    enum: str

    _registered_identifier: str = "com.example.Simple#Person"

@dataclass
class ThePerson(Person):
    the: str = _NO_DEFAULT

    _registered_identifier: str = "com.example.Simple#ThePerson"

    def __post_init__(self):
        no_default_list = [("the", self.the)]
        for n, x in no_default_list:
            if x is _NO_DEFAULT:
                raise TypeError(f"__init__ missing 1 required argument: '{n}'")

@dataclass
class OpenClassExtendingOpenClass:
    someOtherProp: Optional[bool]

    _registered_identifier: str = "com.example.Simple#OpenClassExtendingOpenClass"

@dataclass
class ClassWithReallyLongConstructor:
    theProperty1: str

    theProperty2: str

    theProperty3: str

    theProperty4: str

    theProperty5: str

    theProperty6: str

    _registered_identifier: str = "com.example.Simple#ClassWithReallyLongConstructor"

@dataclass
class com_example_Simple:
    # This is truly a person.
    person: Person

    _registered_identifier: str = "com.example.Simple"

    @classmethod
    def load_pkl(cls, source: str):
        # Load the Pkl module at the given source and evaluate it into `com_example_Simple.Module`.
        # - Parameter source: The source of the Pkl module.
        config = pkll.load(source)
        return cls(**config._asdict())