from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models.seo import AutomationMode
from app.modules.approval_queue.service import ApprovalQueueService


def _session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def test_budget_increase_blocked_without_full_auto():
    db = _session()
    service = ApprovalQueueService(db)

    action = service.enqueue_action(
        module='ads',
        action_type='increase_budget',
        title='Increase budget by 10%',
        payload={'campaign_id': '123'},
        expected_impact=15.0,
        mode=AutomationMode.semi_auto,
    )
    service.decide(action, approved=True, actor='user')

    assert service.execute_if_allowed(action) is False


def test_non_spend_action_executes_after_approval():
    db = _session()
    service = ApprovalQueueService(db)

    action = service.enqueue_action(
        module='search_console',
        action_type='update_meta',
        title='Improve title',
        payload={'page': '/a'},
        expected_impact=7.5,
        mode=AutomationMode.manual,
    )
    service.decide(action, approved=True, actor='user')

    assert service.execute_if_allowed(action) is True
