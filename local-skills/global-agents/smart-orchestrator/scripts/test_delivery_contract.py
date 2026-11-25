"""Shared acceptance oracle: same requirements, temporary real Git repos."""
import copy, importlib, json, subprocess, sys, tempfile, unittest
from pathlib import Path
from datetime import datetime, timedelta, timezone
PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT/'scripts'))
snapshot=importlib.import_module('delivery_snapshot')
evidence=importlib.import_module('delivery_evidence')

class Acceptance(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name).resolve()
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        (self.root/'.gitignore').write_text('.local/\n.super-qa/\n',encoding='utf-8')
        (self.root/'.local').mkdir()
        (self.root/'file.bin').write_bytes(b'\x00\xff\x01')
        (self.root/'test.py').write_text('assert True\n',encoding='utf-8')
        self.before=(datetime.now(timezone.utc)-timedelta(seconds=1)).isoformat()
    def report(self):
        now=datetime.now(timezone.utc).isoformat()
        return dict(status='PASS',runId='fixture-run',project=str(self.root),configHash='abc',sourceFingerprint='def',startedAt=now,finishedAt=now,unregistered=[],results=[dict(id='unit',status='PASS',passed=3,failed=0,skipped=0,todo=0,members=1,memberPaths=['test.py'],reporter='jest')])
    def qualify(self,r=None,required=None):
        return evidence.qualify(self.report() if r is None else r,self.root,['unit'] if required is None else required,self.before)
    def test_snapshot_equivalent(self):
        s=snapshot.capture(self.root);self.assertEqual(s['version'],1)
        self.assertEqual(snapshot.changed(self.root,s),[]);self.assertEqual(len(s['files']['file.bin']),64)
    def test_binary_change(self):
        s=snapshot.capture(self.root);(self.root/'file.bin').write_bytes(b'\x00\xff\x02')
        self.assertIn('file.bin',snapshot.changed(self.root,s))
    def test_new_file(self):
        s=snapshot.capture(self.root);(self.root/'new.py').write_text('x=1')
        self.assertIn('new.py',snapshot.changed(self.root,s))
    def test_deleted_file(self):
        s=snapshot.capture(self.root);(self.root/'file.bin').unlink()
        self.assertIn('file.bin',snapshot.changed(self.root,s))
    def test_ignored_output(self):
        s=snapshot.capture(self.root);(self.root/'.local/result').write_text('output')
        self.assertEqual(snapshot.changed(self.root,s),[])
    def test_subdirectory_rejected(self):
        with self.assertRaises(ValueError):snapshot.capture(self.root/'.local')
    def test_wrong_project_rejected(self):
        s=snapshot.capture(self.root);s['project']=str(self.root.parent)
        with self.assertRaises(ValueError):snapshot.changed(self.root,s)
    def test_bad_snapshot_rejected(self):
        for value in [None,{}, {'version':2}, {'version':1,'files':[]}]:
            with self.subTest(value=value),self.assertRaises(ValueError):snapshot.changed(self.root,value)
    def test_valid_report(self):self.assertTrue(self.qualify())
    def test_bad_report_status(self):
        for status in ['FAIL','BLOCKED','RUNNING','CURRENT',None]:
            r=self.report();r['status']=status
            with self.subTest(status=status),self.assertRaises(ValueError):self.qualify(r)
    def test_skip_failure_flaky_todo(self):
        for field in ['failed','skipped','todo','flaky']:
            r=self.report();r['results'][0][field]=1
            with self.subTest(field=field),self.assertRaises(ValueError):self.qualify(r)
    def test_bad_count(self):
        for n in [True,0,-1,'3',2.5]:
            r=self.report();r['results'][0]['passed']=n
            with self.subTest(n=n),self.assertRaises(ValueError):self.qualify(r)
    def test_missing_duplicate_suites(self):
        for required in [['missing'],[],['unit','unit']]:
            with self.subTest(required=required),self.assertRaises(ValueError):self.qualify(required=required)
        r=self.report();r['results']*=2
        with self.assertRaises(ValueError):self.qualify(r)
    def test_unchosen_failure(self):
        r=self.report();extra=copy.deepcopy(r['results'][0]);extra.update(id='other',status='FAIL');r['results'].append(extra)
        with self.assertRaises(ValueError):self.qualify(r)
    def test_unregistered_and_source_drift(self):
        for field,value in [('unregistered',['test_missing.py']),('sourceChanged',True)]:
            r=self.report();r[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.qualify(r)
    def test_wrong_report_project(self):
        r=self.report();r['project']=str(self.root.parent)
        with self.assertRaises(ValueError):self.qualify(r)
    def test_stale_or_bad_time(self):
        for stamp in ['2001-01-01T00:00:00+00:00','not-a-date','2026-01-01T00:00:00']:
            r=self.report();r['startedAt']=stamp
            with self.subTest(stamp=stamp),self.assertRaises(ValueError):self.qualify(r)
    def test_member_integrity(self):
        for paths in [[],['missing.py'],['../escape.py'],[str(self.root/'test.py')],['test.py','test.py']]:
            r=self.report();r['results'][0]['memberPaths']=paths
            with self.subTest(paths=paths),self.assertRaises(ValueError):self.qualify(r)
    def test_exit_only_report(self):
        r=self.report();r['results'][0]['reporter']='exit'
        with self.assertRaises(ValueError):self.qualify(r)
    def cli(self,*args):
        return subprocess.run([sys.executable,'-B',str(PROJECT/'scripts/delivery.py'),*map(str,args)],capture_output=True,text=True,cwd=self.root)
    def prepare_packet(self):
        candidate=self.root/'.local/candidate.json';packet=self.root/'.local/packet.json';report=self.root/'.local/report.json'
        c=self.cli('capture','--project',self.root,'--out',candidate);self.assertEqual(c.returncode,0,c.stdout+c.stderr)
        report.write_text(json.dumps(self.report()),encoding='utf-8')
        c=self.cli('seal','--project',self.root,'--candidate',candidate,'--report',report,'--suite','unit','--out',packet)
        self.assertEqual(c.returncode,0,c.stdout+c.stderr);return candidate,report,packet
    def test_cli_valid_not_acceptance(self):
        _,_,packet=self.prepare_packet();r=self.cli('check','--project',self.root,'--packet',packet)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr);body=json.loads(r.stdout)
        self.assertEqual(body['status'],'CURRENT');self.assertEqual(body['acceptance'],'MANUAL_REVIEW_REQUIRED')
    def test_cli_code_drift(self):
        _,_,packet=self.prepare_packet();(self.root/'test.py').write_text('assert False\n')
        r=self.cli('check','--project',self.root,'--packet',packet);self.assertEqual(r.returncode,2,r.stdout+r.stderr)
    def test_cli_report_drift(self):
        _,report,packet=self.prepare_packet();report.write_text('{}')
        r=self.cli('check','--project',self.root,'--packet',packet);self.assertEqual(r.returncode,2,r.stdout+r.stderr)
    def test_cli_preserves_output(self):
        out=self.root/'.local/out.json';out.write_text('preserve')
        r=self.cli('capture','--project',self.root,'--out',out)
        self.assertEqual(r.returncode,2,r.stdout+r.stderr);self.assertEqual(out.read_text(),'preserve')
    def test_cli_output_source_rejected(self):
        r=self.cli('capture','--project',self.root,'--out',self.root/'candidate.json')
        self.assertEqual(r.returncode,2,r.stdout+r.stderr);self.assertFalse((self.root/'candidate.json').exists())

if __name__=='__main__':unittest.main()
