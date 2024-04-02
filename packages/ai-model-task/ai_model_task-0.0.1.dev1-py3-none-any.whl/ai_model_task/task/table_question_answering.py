from ai_model_task.base.ParamsAwareBaseModel import ParamsAwareBaseModel


class TableQuestionAnsweringPayload(ParamsAwareBaseModel):
    table: dict
    query: str
