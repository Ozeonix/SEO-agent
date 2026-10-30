from app.modules.sitemap.analyzer import PageAudit, SitemapAnalyzer


class SitemapService:
    def __init__(self):
        self.analyzer = SitemapAnalyzer()

    def crawl_demo_pages(self) -> list[PageAudit]:
        return [
            PageAudit(
                url='https://demo.local/',
                status_code=200,
                title='Home - Demo Local Business',
                has_alt_issues=False,
                has_schema=True,
                load_ms=1500,
            ),
            PageAudit(
                url='https://demo.local/services',
                status_code=404,
                title='Services - Demo Local Business',
                has_alt_issues=True,
                has_schema=False,
                load_ms=2900,
            ),
        ]
