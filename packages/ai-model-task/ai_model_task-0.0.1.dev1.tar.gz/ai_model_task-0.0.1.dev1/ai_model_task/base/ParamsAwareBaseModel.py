from typing import Optional

from pydantic import BaseModel


class ParamsAwareBaseModel(BaseModel):
    params: Optional[dict] = {}
