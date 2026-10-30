from app.core.config import get_settings
from app.modules.search_console.analyzer import SearchConsoleAnalyzer, SearchRow


class SearchConsoleService:
    def __init__(self):
        self.settings = get_settings()
        self.analyzer = SearchConsoleAnalyzer()

    def fetch_rows(self) -> list[SearchRow]:
        if self.settings.demo_mode:
            return [
                SearchRow(
                    page='/services/local-seo',
                    query='local seo services',
                    clicks=12,
                    impressions=1400,
                    ctr=0.0085,
                    position=8.2,
                    previous_position=6.1,
                )
            ]
        return []

    def analyze(self) -> dict[str, list[dict]]:
        return self.analyzer.find_opportunities(self.fetch_rows())
