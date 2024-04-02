from typing import Optional

from ai_model_task.base.ParamsAwareBaseModel import ParamsAwareBaseModel


class TranslationPayload(ParamsAwareBaseModel):
    input: str
    src_lang: Optional[str] = "中文"
    tar_lang: Optional[str] = "英语"
    params: Optional[dict] = {}
