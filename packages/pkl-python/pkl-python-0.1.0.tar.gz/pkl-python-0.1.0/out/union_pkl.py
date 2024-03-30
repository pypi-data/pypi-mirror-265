# Code generated from Pkl module `union`. DO NOT EDIT.
from typing import Dict, List, Literal, Optional, Union
from dataclasses import dataclass
import pkll

_NO_DEFAULT = object()

City = Literal["San Francisco", "London", "上海"]

County = Literal["San Francisco", "San Mateo", "Yolo"]

Noodles = Literal["拉面", "刀切面", "面线", "意大利面"]

AccountDisposition = Literal["", "icloud3", "prod", "shared"]

@dataclass
class union:
    # A city
    city: City

    # County
    county: County

    # Noodles
    noodle: Noodles

    # Account disposition
    disposition: AccountDisposition

    _registered_identifier: str = "union"

    @classmethod
    def load_pkl(cls, source: str):
        # Load the Pkl module at the given source and evaluate it into `union.Module`.
        # - Parameter source: The source of the Pkl module.
        config = pkll.load(source)
        return cls(**config._asdict())