from app.modules.search_console.service import SearchConsoleService
from app.modules.sitemap.service import SitemapService


class PlannerBrain:
    def __init__(self):
        self.search = SearchConsoleService()
        self.sitemap = SitemapService()

    def weekly_plan(self) -> dict:
        search_findings = self.search.analyze()
        technical_findings = self.sitemap.analyzer.analyze_pages(self.sitemap.crawl_demo_pages())
        priorities = []
        if search_findings['low_ctr_pages']:
            priorities.append({'task': 'Improve meta titles/descriptions', 'impact': 'high', 'effort': 'low'})
        if technical_findings['broken_links']:
            priorities.append({'task': 'Fix broken links and missing schema', 'impact': 'medium', 'effort': 'medium'})
        return {
            'findings': {'search_console': search_findings, 'sitemap': technical_findings},
            'priorities': priorities,
        }
