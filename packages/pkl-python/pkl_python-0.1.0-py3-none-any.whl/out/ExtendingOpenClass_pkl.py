# Code generated from Pkl module `ExtendingOpenClass`. DO NOT EDIT.
from enum import Enum
from typing import Dict, List, Literal, Optional, Union
from dataclasses import dataclass
import pkll
from . import lib3_pkl

_NO_DEFAULT = object()

@dataclass
class MyClass(MyOpenClass):
    myBoolean: bool = _NO_DEFAULT

    myStr: str = "mystr"

    _registered_identifier: str = "ExtendingOpenClass#MyClass"

    def __post_init__(self):
        no_default_list = [("myBoolean", self.myBoolean)]
        for n, x in no_default_list:
            if x is _NO_DEFAULT:
                raise TypeError(f"__init__ missing 1 required argument: '{n}'")

@dataclass
class MyOpenClass:
    myStr: str

    _registered_identifier: str = "ExtendingOpenClass#MyOpenClass"

@dataclass
class MyClass2(lib3_pkl.GoGoGo):
    myBoolean: bool = _NO_DEFAULT

    duck: Literal["quack"] = "quack"

    _registered_identifier: str = "ExtendingOpenClass#MyClass2"

    def __post_init__(self):
        no_default_list = [("myBoolean", self.myBoolean)]
        for n, x in no_default_list:
            if x is _NO_DEFAULT:
                raise TypeError(f"__init__ missing 1 required argument: '{n}'")

@dataclass
class ExtendingOpenClass:
    res1: MyClass

    res2: MyClass2

    _registered_identifier: str = "ExtendingOpenClass"

    @classmethod
    def load_pkl(cls, source: str):
        # Load the Pkl module at the given source and evaluate it into `ExtendingOpenClass.Module`.
        # - Parameter source: The source of the Pkl module.
        config = pkll.load(source)
        return cls(**config._asdict())