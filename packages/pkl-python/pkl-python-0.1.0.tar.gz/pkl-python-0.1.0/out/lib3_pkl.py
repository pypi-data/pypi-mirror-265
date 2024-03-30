# Code generated from Pkl module `lib3`. DO NOT EDIT.
from enum import Enum
from typing import Dict, List, Literal, Optional, Union
from dataclasses import dataclass
import pkll

_NO_DEFAULT = object()

@dataclass
class GoGoGo:
    duck: Literal["quack"] = "quack"

    _registered_identifier: str = "lib3#GoGoGo"

@dataclass
class lib3:
    _registered_identifier: str = "lib3"

    @classmethod
    def load_pkl(cls, source: str):
        # Load the Pkl module at the given source and evaluate it into `lib3.Module`.
        # - Parameter source: The source of the Pkl module.
        config = pkll.load(source)
        return cls(**config._asdict())