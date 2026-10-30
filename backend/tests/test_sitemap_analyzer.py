from app.modules.sitemap.analyzer import PageAudit, SitemapAnalyzer


def test_sitemap_generation_and_robots_validation():
    analyzer = SitemapAnalyzer()
    xml = analyzer.generate_sitemap_xml('https://example.com', ['/a', '/b', '/a'])
    assert xml.count('<url>') == 2

    robots = analyzer.validate_robots_txt('User-agent: *\nDisallow:\nSitemap: https://example.com/sitemap.xml')
    assert all(robots.values())


def test_page_issue_analysis():
    analyzer = SitemapAnalyzer()
    issues = analyzer.analyze_pages(
        [
            PageAudit(url='https://x/a', status_code=404, title='Home', has_alt_issues=True, has_schema=False, load_ms=3100),
            PageAudit(url='https://x/b', status_code=200, title='Home', has_alt_issues=False, has_schema=True, load_ms=1200),
        ]
    )

    assert issues['broken_links']
    assert issues['missing_alt_text']
    assert issues['duplicate_titles']
    assert issues['missing_schema']
    assert issues['slow_pages']
