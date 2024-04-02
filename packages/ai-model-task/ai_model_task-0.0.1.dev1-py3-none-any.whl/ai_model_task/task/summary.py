from typing import Optional

from ai_model_task.base.ParamsAwareBaseModel import ParamsAwareBaseModel


class SummaryPayload(ParamsAwareBaseModel):
    input: str
    params: Optional[dict] = {}
