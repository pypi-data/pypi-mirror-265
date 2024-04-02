from typing import Optional

from ai_model_task.base.ParamsAwareBaseModel import ParamsAwareBaseModel


class ReadingComprehensionPayload(ParamsAwareBaseModel):
    context: str
    question: str
    params: Optional[dict] = {}
