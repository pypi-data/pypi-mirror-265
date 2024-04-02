from ai_model_task.base.ParamsAwareBaseModel import ParamsAwareBaseModel


class IndexPayload(ParamsAwareBaseModel):
    name: str
    data: list
