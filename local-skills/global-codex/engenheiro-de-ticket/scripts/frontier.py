"""Read-only GitHub frontier; does not reserve, close, or dispatch tasks."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import re
import subprocess


def select_frontier(issues, dependencies):
    result = []
    for item in sorted(issues, key=lambda x: x['number']):
        if item['state'] != 'open':
            continue
        blockers = dependencies[item['number']]
        if all(b['state'] == 'closed' and b.get('state_reason') == 'completed'
               for b in blockers):
            result.append({'number': item['number'], 'url': item['html_url'],
                           'blockers': [b['number'] for b in blockers]})
    return result


def api(endpoint):
    output = subprocess.run(['rtk', 'proxy', 'gh', 'api', endpoint,
                             '--paginate', '--slurp'], check=True,
                            capture_output=True, encoding='utf-8').stdout
    return [item for page in json.loads(output) for item in page]


def fetch_frontier(repo, parent):
    if not re.fullmatch(r'[\w.-]+/[\w.-]+', repo) or parent < 1:
        raise ValueError('Invalid repository or parent issue')
    url = f'https://github.com/{repo}/issues/{parent}'
    pattern = re.compile(r'^\*\*Parent:\*\*\s*' + re.escape(url) + r'\s*$', re.M)
    issues = [i for i in api(f'repos/{repo}/issues?state=all&per_page=100')
              if not i.get('pull_request') and pattern.search(i.get('body') or '')]
    opened = [i for i in issues if i['state'] == 'open']
    def blockers(i):
        return i['number'], api(f'repos/{repo}/issues/{i["number"]}/dependencies/blocked_by')
    with ThreadPoolExecutor(max_workers=6) as pool:
        dependencies = dict(pool.map(blockers, opened))
    return {'repo': repo, 'parent': parent, 'scanned': len(issues),
            'eligible': select_frontier(issues, dependencies),
            'note': 'Reconcile active tasks and atomic reservations before dispatching ALL eligible tickets.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo')
    parser.add_argument('parent', type=int)
    args = parser.parse_args()
    print(json.dumps(fetch_frontier(args.repo, args.parent), ensure_ascii=False))
