from ai_model_task.base.ParamsAwareBaseModel import ParamsAwareBaseModel


class TextToSpeechPayload(ParamsAwareBaseModel):
    input: str
