"""Original offline function-level probe; no model, vector DB or external calls."""
import importlib.metadata, json, resource, time
start = time.perf_counter()
from langroid.mytypes import Document, DocMetaData
from langroid.vector_store.base import VectorStore

docs = [Document(content='alpha', metadata=DocMetaData()), Document(content='beta', metadata=DocMetaData())]
observations = []
for label, expr in [('benign', "df['content'].count()"), ('restricted_builtin', 'len(df)'), ('invalid_control', '(')]:
    value = VectorStore.compute_from_docs(None, docs, expr)
    observations.append(dict(label=label, expression=expr, result=str(value).strip()))
usage = resource.getrusage(resource.RUSAGE_SELF)
print(json.dumps(dict(version=importlib.metadata.version('langroid'), observations=observations, probe_seconds=time.perf_counter()-start, peak_process_rss_kib=usage.ru_maxrss, cpu_seconds=usage.ru_utime+usage.ru_stime)))
