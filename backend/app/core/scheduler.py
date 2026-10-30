from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.config import get_settings
from app.modules.planner.brain import PlannerBrain

scheduler = BackgroundScheduler()


def schedule_jobs() -> None:
    settings = get_settings()
    planner = PlannerBrain()

    daily = CronTrigger.from_crontab(settings.scheduler_daily_cron)
    weekly = CronTrigger.from_crontab(settings.scheduler_weekly_cron)

    scheduler.add_job(lambda: planner.search.analyze(), trigger=daily, id='daily-search-console', replace_existing=True)
    scheduler.add_job(planner.weekly_plan, trigger=weekly, id='weekly-planner', replace_existing=True)
    if not scheduler.running:
        scheduler.start()
