from ai_model_task.base.ParamsAwareBaseModel import ParamsAwareBaseModel


class CodeGenerationPayload(ParamsAwareBaseModel):
    input: str
    lang: str | None
