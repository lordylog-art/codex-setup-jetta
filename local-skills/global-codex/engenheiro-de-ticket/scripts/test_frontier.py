import unittest
from frontier import select_frontier

def issue(n, state='open', reason=None):
    return {'number': n, 'state': state, 'state_reason': reason,
            'html_url': f'https://github.com/o/r/issues/{n}'}

class FrontierTests(unittest.TestCase):
    def test_fanout_and_earlier_ready_ticket(self):
        done = issue(31, 'closed', 'completed')
        nodes = [issue(n) for n in [32,33,34,35,36]]
        dependencies = {32:[done],33:[done],34:[done],
                        35:[issue(30,'closed','completed')],36:[issue(32),issue(33)]}
        self.assertEqual([r['number'] for r in select_frontier(nodes,dependencies)],
                         [32,33,34,35])

    def test_join_waits_for_every_blocker(self):
        nodes = [issue(36)]
        deps = {36:[issue(32,'closed','completed'),issue(33)]}
        self.assertEqual(select_frontier(nodes,deps), [])
        deps[36][1] = issue(33,'closed','completed')
        self.assertEqual(select_frontier(nodes,deps)[0]['number'],36)

    def test_abandoned_and_unknown_dependencies_do_not_release(self):
        self.assertEqual(select_frontier([issue(2)], {2:[issue(1,'closed','not_planned')]}),[])
        with self.assertRaises(KeyError): select_frontier([issue(2)], {})

    def test_closed_ticket_is_not_restarted(self):
        self.assertEqual(select_frontier([issue(1,'closed','completed')], {}), [])

if __name__ == '__main__': unittest.main()
