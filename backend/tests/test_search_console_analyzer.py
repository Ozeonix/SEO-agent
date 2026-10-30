from app.modules.search_console.analyzer import SearchConsoleAnalyzer, SearchRow


def test_search_console_detects_opportunities():
    analyzer = SearchConsoleAnalyzer()
    results = analyzer.find_opportunities(
        [
            SearchRow('/a', 'alpha', clicks=10, impressions=1200, ctr=0.008, position=10.0, previous_position=7.0),
            SearchRow('/b', 'beta', clicks=60, impressions=500, ctr=0.12, position=2.0, previous_position=2.1),
        ]
    )

    assert len(results['low_ctr_pages']) == 1
    assert results['low_ctr_pages'][0]['page'] == '/a'
    assert len(results['quick_win_keywords']) == 1
    assert len(results['dropping_pages']) == 1


def test_metadata_suggestion_respects_lengths():
    analyzer = SearchConsoleAnalyzer()
    suggested = analyzer.suggest_metadata('/x', 'best local seo agency near me')
    assert len(suggested['title']) <= 60
    assert len(suggested['meta_description']) <= 155
