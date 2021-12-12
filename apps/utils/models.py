from model_utils.models import SoftDeletableModel


class BaseModel(SoftDeletableModel):
    class Meta:
        abstract = True
