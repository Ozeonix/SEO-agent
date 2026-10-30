from dataclasses import dataclass


@dataclass
class SearchRow:
    page: str
    query: str
    clicks: int
    impressions: int
    ctr: float
    position: float
    previous_position: float | None = None


class SearchConsoleAnalyzer:
    def find_opportunities(self, rows: list[SearchRow]) -> dict[str, list[dict]]:
        low_ctr = [
            {'page': r.page, 'query': r.query, 'impressions': r.impressions, 'ctr': r.ctr}
            for r in rows
            if r.impressions >= 100 and r.ctr < 0.02
        ]
        quick_wins = [
            {'page': r.page, 'query': r.query, 'position': r.position}
            for r in rows
            if 5 <= r.position <= 20
        ]
        dropping_pages = [
            {
                'page': r.page,
                'query': r.query,
                'previous_position': r.previous_position,
                'position': r.position,
            }
            for r in rows
            if r.previous_position is not None and r.position - r.previous_position >= 2
        ]
        return {
            'low_ctr_pages': low_ctr,
            'quick_win_keywords': quick_wins,
            'dropping_pages': dropping_pages,
            'indexing_errors': [],
            'crawl_issues': [],
        }

    def suggest_metadata(self, page: str, primary_keyword: str) -> dict[str, str]:
        title = f"{primary_keyword.title()} | Improve Results with Proven Tips"
        description = (
            f"Learn how {primary_keyword} can boost results for {page}. "
            'Actionable guidance with clear next steps.'
        )
        return {'title': title[:60], 'meta_description': description[:155]}
