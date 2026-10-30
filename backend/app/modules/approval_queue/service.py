from sqlalchemy.orm import Session

from app.models.seo import ApprovalAction, AuditLog, AutomationMode


class ApprovalQueueService:
    def __init__(self, db: Session):
        self.db = db

    def enqueue_action(
        self,
        module: str,
        action_type: str,
        title: str,
        payload: dict,
        expected_impact: float | None,
        mode: AutomationMode,
    ) -> ApprovalAction:
        action = ApprovalAction(
            module=module,
            action_type=action_type,
            title=title,
            payload=payload,
            expected_impact=expected_impact,
            mode=mode,
            approved=mode == AutomationMode.full_auto,
        )
        self.db.add(action)
        self.db.flush()
        self._log(action.id, 'action_enqueued', f'Action queued for {module}:{action_type}')
        return action

    def decide(self, action: ApprovalAction, approved: bool, actor: str) -> ApprovalAction:
        action.approved = approved
        self._log(action.id, 'action_decision', f'Approved={approved} by {actor}', {'actor': actor})
        return action

    def execute_if_allowed(self, action: ApprovalAction) -> bool:
        if action.mode != AutomationMode.full_auto and not action.approved:
            self._log(action.id, 'execution_blocked', 'Execution requires approval')
            return False
        if action.action_type in {'increase_budget', 'raise_bid'} and action.mode != AutomationMode.full_auto:
            self._log(action.id, 'execution_blocked', 'Spend-increasing change blocked without full-auto')
            return False

        action.executed = True
        self._log(action.id, 'action_executed', 'Action executed successfully')
        return True

    def _log(self, action_id: int | None, event_type: str, message: str, metadata: dict | None = None):
        self.db.add(AuditLog(action_id=action_id, event_type=event_type, message=message, details=metadata))
