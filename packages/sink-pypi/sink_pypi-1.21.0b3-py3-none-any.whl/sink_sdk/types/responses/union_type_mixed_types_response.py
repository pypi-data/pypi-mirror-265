# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional

from ..shared import SimpleObject
from ..._models import BaseModel

__all__ = ["UnionTypeMixedTypesResponse", "BasicObject"]


class BasicObject(BaseModel):
    item: Optional[str] = None


UnionTypeMixedTypesResponse = Union[SimpleObject, BasicObject, bool]
