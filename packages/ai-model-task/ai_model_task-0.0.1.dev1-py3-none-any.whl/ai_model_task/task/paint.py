from typing import Optional

from ai_model_task.base.ParamsAwareBaseModel import ParamsAwareBaseModel


class PaintPayload(ParamsAwareBaseModel):
    prompt: str
    output_dir: Optional[str]
    output_filename: Optional[str] = "demo.png"
