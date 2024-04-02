from ai_model_task.base.ParamsAwareBaseModel import ParamsAwareBaseModel


class ZeroShotClassificationPayload(ParamsAwareBaseModel):
    sequence: str
    labels: list
