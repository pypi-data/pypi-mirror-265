# Code generated from Pkl module `ExtendModule`. DO NOT EDIT.
from enum import Enum
from typing import Dict, List, Literal, Optional, Union
from dataclasses import dataclass
import pkll
from . import MyModule_pkl

_NO_DEFAULT = object()

@dataclass
class ExtendModule(MyModule_pkl.MyModule):
    bar: str = _NO_DEFAULT

    _registered_identifier: str = "ExtendModule"

    def __post_init__(self):
        no_default_list = [("bar", self.bar)]
        for n, x in no_default_list:
            if x is _NO_DEFAULT:
                raise TypeError(f"__init__ missing 1 required argument: '{n}'")

    @classmethod
    def load_pkl(cls, source: str):
        # Load the Pkl module at the given source and evaluate it into `ExtendModule.Module`.
        # - Parameter source: The source of the Pkl module.
        config = pkll.load(source)
        return cls(**config._asdict())

breakpoint()
