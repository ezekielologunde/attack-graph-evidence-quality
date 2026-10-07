"""Original disposable-fixture check of installed pretalx export function."""
import importlib.metadata, json, os, resource, tempfile, time
from pathlib import Path
start=time.perf_counter()
config=Path('/tmp/pretalx-probe.cfg')
config.write_text('[filesystem]\nbase=/tmp/pretalx-app\n[database]\nbackend=sqlite3\nname=:memory:\n')
os.environ['PRETALX_CONFIG_FILE']=str(config)
os.environ['DJANGO_SETTINGS_MODULE']='pretalx.settings'
import django
django.setup()
from pretalx.agenda.management.commands.export_schedule_html import dump_content
from django.core.management.base import CommandError

root=Path(tempfile.mkdtemp(prefix='export-fixture-'))
destination=root/'export';destination.mkdir()
observations=[]
for label,path,target in [('benign','/page.html',destination/'page.html'),('traversal','/../outside.html',root/'outside.html')]:
    error=None
    try: dump_content(destination,path,lambda _: b'public synthetic fixture')
    except CommandError as e: error=str(e)
    observations.append(dict(label=label,error=error,file_exists=target.exists(),expected_content=target.exists() and target.read_bytes()==b'public synthetic fixture'))
usage=resource.getrusage(resource.RUSAGE_SELF)
print(json.dumps(dict(version=importlib.metadata.version('pretalx'),observations=observations,probe_seconds=time.perf_counter()-start,peak_process_rss_kib=usage.ru_maxrss,cpu_seconds=usage.ru_utime+usage.ru_stime)))
