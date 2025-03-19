from pydantic import BaseModel


class ConfigMixin(BaseModel):
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        from_attributes = True
