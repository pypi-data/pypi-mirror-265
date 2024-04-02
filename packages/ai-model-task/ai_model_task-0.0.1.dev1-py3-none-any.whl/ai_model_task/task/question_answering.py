from ai_model_task.base.ParamsAwareBaseModel import ParamsAwareBaseModel


class QuestionAnsweringPayload(ParamsAwareBaseModel):
    question: str
