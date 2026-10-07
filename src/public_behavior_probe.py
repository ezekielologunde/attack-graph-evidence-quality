import argparse,json,time,resource,hashlib,ssl,zipfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('case');args=p.parse_args();start=time.perf_counter()
if args.case=='scrapy':
 import scrapy
 from scrapy.http import Request,Response,HtmlResponse
 from scrapy.settings import Settings
 from scrapy.downloadermiddlewares.redirect import RedirectMiddleware,MetaRefreshMiddleware
 settings=Settings();spider=scrapy.Spider('offline-probe');rows=[]
 for kind,cls in [('location',RedirectMiddleware),('meta',MetaRefreshMiddleware)]:
  mw=cls(settings)
  for target in ['https://example.invalid/next','file:///tmp/nonexistent-probe-fixture']:
   req=Request('https://example.invalid/start')
   response=Response(req.url,status=302,headers={'Location':target}) if kind=='location' else HtmlResponse(req.url,body=('<html><head><meta http-equiv="refresh" content="0;url='+target+'"></head></html>').encode(),encoding='utf-8')
   result=mw.process_response(req,response,spider)
   rows.append(dict(kind=kind,target=target,returned_request=isinstance(result,Request),result_url=result.url))
 result=dict(version=scrapy.__version__,observations=rows)
else:
 target='9a296a5182d1d451a2e37f439b74daafa267523329f90f9a0d2007c334e23c9a';rows=[]
 blank=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT);empty=len(blank.get_ca_certs(binary_form=True))==0
 for wheel in sorted(Path('/wheels').glob('certifi*.whl')):
  with zipfile.ZipFile(wheel) as z:bundle=z.read('certifi/cacert.pem').decode('ascii')
  ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT);ctx.load_verify_locations(cadata=bundle)
  fingerprints=sorted(hashlib.sha256(c).hexdigest() for c in ctx.get_ca_certs(binary_form=True))
  rows.append(dict(wheel=wheel.name,sha256=hashlib.sha256(wheel.read_bytes()).hexdigest(),target_present=target in fingerprints,fingerprints=fingerprints))
 result=dict(observations=rows,empty_context_control=empty,common_non_target_control=bool((set(rows[0]['fingerprints'])&set(rows[1]['fingerprints']))-{target}))
result.update(probe_seconds=time.perf_counter()-start,peak_process_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,cpu_seconds=resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime)
print(json.dumps(result))
