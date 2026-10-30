from dataclasses import dataclass
from urllib.parse import urljoin
import xml.etree.ElementTree as ET


@dataclass
class PageAudit:
    url: str
    status_code: int
    title: str | None
    has_alt_issues: bool
    has_schema: bool
    load_ms: int


class SitemapAnalyzer:
    def generate_sitemap_xml(self, base_url: str, paths: list[str]) -> str:
        root = ET.Element('urlset', attrib={'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'})
        for path in sorted(set(paths)):
            node = ET.SubElement(root, 'url')
            ET.SubElement(node, 'loc').text = urljoin(base_url.rstrip('/') + '/', path.lstrip('/'))
        return ET.tostring(root, encoding='unicode')

    def validate_robots_txt(self, robots_txt: str) -> dict[str, bool]:
        lowered = robots_txt.lower()
        return {
            'has_user_agent': 'user-agent:' in lowered,
            'has_disallow': 'disallow:' in lowered,
            'has_sitemap': 'sitemap:' in lowered,
        }

    def analyze_pages(self, pages: list[PageAudit]) -> dict[str, list[dict]]:
        broken_links = [{'url': p.url, 'status_code': p.status_code} for p in pages if p.status_code >= 400]
        missing_alt = [{'url': p.url} for p in pages if p.has_alt_issues]
        duplicate_titles = []
        seen_titles: dict[str, str] = {}
        for page in pages:
            if page.title and page.title in seen_titles:
                duplicate_titles.append({'url': page.url, 'duplicate_of': seen_titles[page.title]})
            elif page.title:
                seen_titles[page.title] = page.url
        missing_schema = [{'url': p.url} for p in pages if not p.has_schema]
        slow_pages = [{'url': p.url, 'load_ms': p.load_ms} for p in pages if p.load_ms > 2500]

        return {
            'broken_links': broken_links,
            'missing_alt_text': missing_alt,
            'duplicate_titles': duplicate_titles,
            'missing_schema': missing_schema,
            'slow_pages': slow_pages,
        }

    def generate_schema_markup(self, schema_type: str, payload: dict) -> dict:
        return {'@context': 'https://schema.org', '@type': schema_type, **payload}
