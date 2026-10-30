from pydantic import BaseModel


class ActionCreate(BaseModel):
    module: str
    action_type: str
    title: str
    payload: dict
    expected_impact: float | None = None


class ActionDecision(BaseModel):
    approved: bool
    actor: str = 'user'
