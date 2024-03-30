# Code generated from Pkl module `com.example.ExtendedSimple`. DO NOT EDIT.
from enum import Enum
from typing import Dict, List, Literal, Optional, Union
from dataclasses import dataclass
import pkll
from . import com_example_Simple_pkl

_NO_DEFAULT = object()

@dataclass
class ExtendedSimple(com_example_Simple_pkl.Person):
    eyeColor: str = _NO_DEFAULT

    _registered_identifier: str = "com.example.ExtendedSimple#ExtendedSimple"

    def __post_init__(self):
        no_default_list = [("eyeColor", self.eyeColor)]
        for n, x in no_default_list:
            if x is _NO_DEFAULT:
                raise TypeError(f"__init__ missing 1 required argument: '{n}'")

@dataclass
class com_example_ExtendedSimple:
    _registered_identifier: str = "com.example.ExtendedSimple"

    @classmethod
    def load_pkl(cls, source: str):
        # Load the Pkl module at the given source and evaluate it into `com_example_ExtendedSimple.Module`.
        # - Parameter source: The source of the Pkl module.
        config = pkll.load(source)
        return cls(**config._asdict())

breakpoint()
