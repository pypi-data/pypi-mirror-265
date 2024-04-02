from ai_model_task.base.ParamsAwareBaseModel import ParamsAwareBaseModel


class TextGenerationPayload(ParamsAwareBaseModel):
    input: str
