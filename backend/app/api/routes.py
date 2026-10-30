from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import Base, engine, get_db
from app.models.seo import ApprovalAction, AutomationMode
from app.modules.approval_queue.service import ApprovalQueueService
from app.modules.planner.brain import PlannerBrain
from app.modules.search_console.service import SearchConsoleService
from app.modules.sitemap.service import SitemapService
from app.schemas.actions import ActionCreate, ActionDecision

router = APIRouter()
planner = PlannerBrain()
search_service = SearchConsoleService()
sitemap_service = SitemapService()


@router.on_event('startup')
def init_db():
    Base.metadata.create_all(bind=engine)


@router.get('/health')
def health():
    return {'status': 'ok'}


@router.get('/overview')
def overview():
    search_findings = search_service.analyze()
    sitemap_findings = sitemap_service.analyzer.analyze_pages(sitemap_service.crawl_demo_pages())
    return {
        'search_console': search_findings,
        'sitemap': sitemap_findings,
        'priorities': planner.weekly_plan()['priorities'],
    }


@router.get('/issues')
def issues():
    weekly = planner.weekly_plan()
    return weekly['findings']


@router.post('/actions', response_model=dict)
def create_action(payload: ActionCreate, db: Session = Depends(get_db)):
    queue = ApprovalQueueService(db)
    action = queue.enqueue_action(
        module=payload.module,
        action_type=payload.action_type,
        title=payload.title,
        payload=payload.payload,
        expected_impact=payload.expected_impact,
        mode=AutomationMode.manual,
    )
    db.commit()
    return {'id': action.id, 'approved': action.approved, 'executed': action.executed}


@router.post('/actions/{action_id}/decision')
def decide_action(action_id: int, payload: ActionDecision, db: Session = Depends(get_db)):
    action = db.get(ApprovalAction, action_id)
    if not action:
        raise HTTPException(status_code=404, detail='Action not found')
    queue = ApprovalQueueService(db)
    queue.decide(action, payload.approved, payload.actor)
    executed = queue.execute_if_allowed(action)
    db.commit()
    return {'id': action.id, 'approved': action.approved, 'executed': executed}


@router.get('/action-queue')
def action_queue(db: Session = Depends(get_db)):
    rows = db.query(ApprovalAction).order_by(ApprovalAction.created_at.desc()).all()
    return [
        {
            'id': row.id,
            'module': row.module,
            'title': row.title,
            'mode': row.mode.value,
            'approved': row.approved,
            'executed': row.executed,
        }
        for row in rows
    ]


@router.get('/content')
def content():
    return {'briefs': [], 'drafts': [], 'internal_linking_suggestions': []}


@router.get('/reviews')
def reviews():
    return {'queue': [], 'weekly_post_suggestions': [], 'nap_issues': []}


@router.get('/ads')
def ads():
    return {'campaigns': [], 'optimization_suggestions': []}


@router.get('/auth/google/url')
def auth_google_url():
    return {'url': 'https://accounts.google.com/o/oauth2/v2/auth?mock=true'}


@router.post('/auth/google/callback')
def auth_google_callback():
    return {'connected': True, 'message': 'Mock Google account connection completed.'}


@router.get('/accounts')
def connected_accounts():
    return {'businesses': [], 'sites': [], 'mode': 'mock'}


@router.get('/reports/weekly')
def weekly_report():
    return {
        'summary': 'Demo weekly report generated in mock mode.',
        'email_ready': True,
        'pdf_ready': False,
    }
