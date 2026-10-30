from datetime import date


class ReportingService:
    def weekly_summary(self, highlights: list[str], next_steps: list[str]) -> str:
        lines = [f'Weekly SEO & Ads report - {date.today().isoformat()}', '', "What's changed:"]
        lines.extend([f'- {item}' for item in highlights] or ['- No major changes this week.'])
        lines.append('')
        lines.append("What's next:")
        lines.extend([f'- {item}' for item in next_steps] or ['- Continue monitoring trends.'])
        return '\n'.join(lines)
