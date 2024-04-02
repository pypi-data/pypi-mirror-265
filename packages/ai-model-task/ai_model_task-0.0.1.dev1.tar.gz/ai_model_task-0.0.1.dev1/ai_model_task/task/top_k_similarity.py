from ai_model_task.base.ParamsAwareBaseModel import ParamsAwareBaseModel


class TopKSimilarityIndexPayload(ParamsAwareBaseModel):
    index_name: str
    index_data: list
    transforms: list[str]


class TopKSimilarityQueryPayload(ParamsAwareBaseModel):
    index_name: str
    query_data: list
    k: int = 10
    transforms: list[str]
