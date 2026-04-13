from typing import TypeVar, Generic

from pydantic import BaseModel

from app.core.interface.normalization_interface import NormalizationInterface
from app.core.interface.operator_interface import OperatorInterface

T = TypeVar("T")


class StrategyInterface(BaseModel, Generic[T]):
    config: T
    normalization: NormalizationInterface
    operator: OperatorInterface

    class Config:
        arbitrary_types_allowed = True
