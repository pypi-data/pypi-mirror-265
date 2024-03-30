# Code generated from Pkl module `Imports`. DO NOT EDIT.
from typing import Dict, List, Literal, Optional, Union
from dataclasses import dataclass
import pkll
from . import Foo_pkl

_NO_DEFAULT = object()

@dataclass
class Imports:
    foo: Foo_pkl.Foo

    _registered_identifier: str = "Imports"

    @classmethod
    def load_pkl(cls, source: str):
        # Load the Pkl module at the given source and evaluate it into `Imports.Module`.
        # - Parameter source: The source of the Pkl module.
        config = pkll.load(source)
        return cls(**config._asdict())