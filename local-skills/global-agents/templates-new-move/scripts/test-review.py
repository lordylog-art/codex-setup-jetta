import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from types import SimpleNamespace
import urllib.error
import urllib.request

spec = importlib.util.spec_from_file_location('review', Path(__file__).with_name('serve-review.py'))
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
MANIFEST = {'grooming': 'nota#decisao', 'surfaces': [{'id': 'a', 'template': 'ModalCenario'}]}
FEEDBACK = {'items': [{'id': 'a', 'decision': 'disagree', 'text': 'Não mudar a cor; ampliar o conteúdo.'}]}


class FakeMCP:
    answer = {'changes': [{'id': 'a', 'request': 'Ampliar o conteúdo.'}], 'summary': 'Revisão pronta.'}
    def __init__(self, **_): pass
    def __enter__(self): return self
    def __exit__(self, *_): pass
    def create_chat(self, prompt, **options):
        assert options['sandbox'] == 'read-only'
        assert 'Não mudar a cor' in prompt
        return {'agentId': 'a', 'threadId': 'thread-test'}
    def wait(self, *_):
        return {'ready': [{'status': 'completed', 'message': json.dumps(self.answer)}]}


class ReviewTests(unittest.TestCase):
    def test_memory_preserves_history_and_latest_decision(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'decisions.md'
            feedback = copy.deepcopy(FEEDBACK)
            feedback['items'][0]['configuration'] = {'sucesso.posicao': 'direita', 'erro.posicao': 'esquerda'}
            save = lambda: review.memory.record_decisions(path, MANIFEST, feedback, 'origin')
            self.assertEqual(save()['added'], 1)
            self.assertEqual(save()['added'], 0)
            feedback['items'][0]['decision'] = 'agree'
            self.assertEqual(save()['added'], 1)
            feedback['items'][0]['decision'] = 'disagree'
            self.assertEqual(save()['added'], 1)
            text = path.read_text(encoding='utf-8')
            self.assertEqual(text.count('<!-- context:'), 3)
            self.assertIn('sucesso.posicao', text)
            self.assertIn('erro.posicao', text)
            with patch.object(review.memory.os, 'replace', side_effect=OSError('disk')):
                feedback['items'][0]['decision'] = 'change'
                with self.assertRaises(OSError): save()
            self.assertEqual(path.read_text(encoding='utf-8'), text)
            self.assertFalse(path.with_suffix('.lock').exists())

    def test_total_acceptance_ends_studio(self):
        manifest = {'surfaces': [{'id': 'a'}, {'id': 'b'}]}
        feedback = {'items': [{'id': name, 'decision': 'agree', 'text': 'Ajuste aprovado.'} for name in ('a', 'b')]}
        self.assertEqual(review.studio_stage(manifest, feedback), 'implementation')
        for decision in ('pending', 'disagree', 'change'):
            feedback['items'][1]['decision'] = decision
            self.assertEqual(review.studio_stage(manifest, feedback), 'review')
        with self.assertRaises(ValueError): review.studio_stage(manifest, {'items': feedback['items'][:1]})
        self.assertEqual(review.studio_stage({'surfaces': []}, {'items': []}), 'review')

    def test_delivery_preserves_full_json_and_target(self):
        with tempfile.TemporaryDirectory() as directory:
            sender = Path(directory) / 'direcionar_chat.py'
            sender.write_text('# test')
            result = {'stage': 'implementation', 'feedback': [{'text': 'Comentário longo ' * 5000}]}
            ack = SimpleNamespace(returncode=0, stdout=json.dumps({'threadId': 'origin', 'result': {'isError': False}}))
            with patch.object(review.subprocess, 'run', return_value=ack) as run:
                self.assertEqual(review.send_to_chat(sender, 'origin', result), {'status': 'sent', 'threadId': 'origin'})
                payload = json.loads(run.call_args.kwargs['input'])
                self.assertEqual(payload['thread'], 'origin')
                self.assertIn('Siga diretamente à implementação', payload['message'])
                self.assertIn(result['feedback'][0]['text'], payload['message'])
            with patch.object(review.subprocess, 'run', return_value=SimpleNamespace(returncode=1, stdout='')):
                with self.assertRaises(RuntimeError): review.send_to_chat(sender, 'origin', result)
    def test_feedback_integrity_and_validation(self):
        result = review.ask_codex(FakeMCP, Path.cwd(), MANIFEST, FEEDBACK)
        self.assertEqual(result['feedback'], FEEDBACK['items'])
        self.assertEqual(result['grooming'], MANIFEST['grooming'])
        for value in ({'items': []}, {'items': FEEDBACK['items'] * 2}, {'items': [{'id': 'other', 'decision': 'agree', 'text': ''}]}, {'items': [{'id': 'a', 'decision': 'invented', 'text': ''}]}):
            with self.assertRaises(ValueError): review.validate_feedback(value, MANIFEST)
        self.assertEqual(review.validate_feedback(FEEDBACK, MANIFEST), FEEDBACK)
        configured = copy.deepcopy(FEEDBACK)
        configured['items'][0]['configuration'] = {'tamanho': 'compacto', 'apresentacao': 'conteudo', 'sucesso.posicao': 'direita', 'sucesso.apresentacao': 'ilustrado', 'erro.posicao': 'esquerda', 'erro.apresentacao': 'conteudo'}
        self.assertEqual(review.validate_feedback(configured, MANIFEST), configured)
        self.assertEqual(review.ask_codex(FakeMCP, Path.cwd(), MANIFEST, configured)['feedback'], configured['items'])
        configured['items'][0]['configuration']['tamanho'] = []
        with self.assertRaises(ValueError): review.validate_feedback(configured, MANIFEST)

    def test_unknown_ai_reference_rejected(self):
        with patch.object(FakeMCP, 'answer', {'changes': [{'id': 'invented', 'request': 'x'}], 'summary': 'x'}):
            with self.assertRaises(ValueError): review.ask_codex(FakeMCP, Path.cwd(), MANIFEST, FEEDBACK)

    def test_http_origin_traversal_and_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'review.json').write_text(json.dumps(MANIFEST))
            (root / 'index.html').write_text('<h1>Review</h1>')
            mcp = root / 'mcp.py'
            mcp.write_text('class CodexMCP: pass')
            server = review.make_server(root, Path('D:/newmove'), mcp, 0, memory_path=root / 'decisions.md')
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            base = f'http://127.0.0.1:{server.server_port}'
            def request(path, value=None, origin=base):
                req = urllib.request.Request(base + path, data=None if value is None else json.dumps(value).encode(), headers={'Origin': origin, 'X-Review-Voice': '1', 'Content-Type': 'application/json'})
                try:
                    with urllib.request.urlopen(req) as response: return response.status, response.read()
                except urllib.error.HTTPError as error: return error.code, error.read()
            try:
                self.assertEqual(request('/')[0], 200)
                self.assertEqual(request('/%2e%2e/settings.json')[0], 404)
                self.assertEqual(request('/review', FEEDBACK, 'https://evil.test')[0], 403)
                self.assertEqual(request('/review', {'items': []})[0], 400)
                with patch.object(review, 'ask_codex', return_value={'feedback': FEEDBACK['items']}) as ask, patch.object(review, 'send_to_chat', return_value={'status': 'sent', 'threadId': 'origin'}):
                    status, body = request('/review', FEEDBACK)
                    self.assertEqual(status, 200)
                    self.assertEqual(json.loads(body)['feedback'], FEEDBACK['items'])
                    self.assertEqual(json.loads(body)['delivery']['status'], 'sent')
                    self.assertEqual(ask.call_count, 1)
                    self.assertEqual(json.loads(body)['memory']['status'], 'saved')
                    saved_memory = (root / 'decisions.md').read_text(encoding='utf-8')
                with patch.object(review, 'ask_codex', return_value={'feedback': FEEDBACK['items']}), patch.object(review, 'send_to_chat', side_effect=RuntimeError('offline')):
                    status, body = request('/review', FEEDBACK)
                    self.assertEqual(status, 200)
                    self.assertEqual(json.loads(body)['feedback'], FEEDBACK['items'])
                    self.assertEqual(json.loads(body)['delivery']['status'], 'failed')
                    self.assertEqual((root / 'decisions.md').read_text(encoding='utf-8'), saved_memory)
                with patch.object(review, 'speech', return_value=b'mp3'):
                    self.assertEqual(request('/speech', {'text': 'Resumo'})[1], b'mp3')
                self.assertEqual(request('/speech', {'text': ''})[0], 400)
            finally:
                server.shutdown()
                server.server_close()
                thread.join()


if __name__ == '__main__': unittest.main()
