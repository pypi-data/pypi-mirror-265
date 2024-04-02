from typing import Optional

from ai_model_task.base.ParamsAwareBaseModel import ParamsAwareBaseModel


class ChatPayload(ParamsAwareBaseModel):
    input: str
    history: Optional[list] = []
