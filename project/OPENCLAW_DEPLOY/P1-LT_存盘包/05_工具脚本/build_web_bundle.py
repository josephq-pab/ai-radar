from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE = Path('/home/admin/.openclaw/workspace-ai-radar/project/OPENCLAW_DEPLOY')
PROCESSED = BASE / 'data' / 'processed'
REPORTS = BASE / 'reports'
WEB_DATA = BASE / 'apps' / 'web' / 'data'


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def main() -> None:
    WEB_DATA.mkdir(parents=True, exist_ok=True)
    payload = {
        'dashboard': load_json(PROCESSED / 'dashboard.json'),
        'quality': load_json(PROCESSED / 'quality_report.json'),
        'deposit': load_json(PROCESSED / 'deposit_benchmark.json'),
        'loan': load_json(PROCESSED / 'loan_benchmark.json'),
        'rate': load_json(PROCESSED / 'loan_rate.json'),
        'summary': load_json(PROCESSED / 'summary.json'),
        'preferenceProfile': load_json(PROCESSED / 'preference_profile.json') if (PROCESSED / 'preference_profile.json').exists() else {'guidance': [], 'topThemes': [], 'totalReviews': 0},
        'sectionPreferences': load_json(PROCESSED / 'section_preferences.json') if (PROCESSED / 'section_preferences.json').exists() else {'sections': {}},
        'domainTemplates': load_json(PROCESSED / 'domain_templates.json') if (PROCESSED / 'domain_templates.json').exists() else {'domains': {}},
        'interpretationRules': load_json(PROCESSED / 'interpretation_rules.json') if (PROCESSED / 'interpretation_rules.json').exists() else {'rules': {}},
        'recommendationRules': load_json(PROCESSED / 'recommendation_rules.json') if (PROCESSED / 'recommendation_rules.json').exists() else {'rules': {}},
        'trackingStatusRules': load_json(PROCESSED / 'tracking_status_rules.json') if (PROCESSED / 'tracking_status_rules.json').exists() else {'reviewToTracking': {}},
        'weeklyReportMarkdown': (REPORTS / 'weekly-report-draft.md').read_text(encoding='utf-8') if (REPORTS / 'weekly-report-draft.md').exists() else '',
        'reviewQueue': load_json(REPORTS / 'review-queue.json') if (REPORTS / 'review-queue.json').exists() else {'items': []},
        'reviewStatus': load_json(REPORTS / 'review-status.json') if (REPORTS / 'review-status.json').exists() else {'items': [], 'pending': 0, 'approved': 0, 'modified': 0, 'rejected': 0},
        'trackingItems': load_json(REPORTS / 'tracking-items.json') if (REPORTS / 'tracking-items.json').exists() else {'items': [], 'pending': 0, 'approved': 0, 'modified': 0, 'rejected': 0},
    }
    content = 'window.AIRadarData = ' + json.dumps(payload, ensure_ascii=False, indent=2) + ';\n'
    (WEB_DATA / 'app-data.js').write_text(content, encoding='utf-8')
    print(WEB_DATA / 'app-data.js')


if __name__ == '__main__':
    main()
