"""Offline API-level header check; synthetic credentials; no request is sent."""
import argparse
import hashlib
import json
import socket
import sys
import time
from pathlib import Path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--wheels',required=True)
    parser.add_argument('--version',required=True)
    args=parser.parse_args()
    wheels=sorted(Path(args.wheels).glob('*.whl'))
    sys.path[:0]=[str(p) for p in wheels]
    def guard(event,args):
        if event in ('socket.connect','socket.getaddrinfo','socket.bind','socket.sendto'):
            raise RuntimeError('Network access forbidden during behavior check')
    sys.addaudithook(guard)
    import requests
    assert requests.__version__==args.version
    results=[]
    for scheme in ('http','https'):
        for credentials in (False,True):
            for preexisting in (False,True):
                session=requests.Session()
                session.trust_env=False
                request=requests.Request('GET',f'{scheme}://destination.invalid/resource',
                                         headers={'Proxy-Authorization':'synthetic-old'} if preexisting else {})
                prepared=request.prepare()
                authority='synthetic-user:synthetic-password@' if credentials else ''
                proxies={scheme:f'http://{authority}proxy.invalid:8080'}
                start=time.perf_counter()
                session.rebuild_proxies(prepared,proxies)
                elapsed=time.perf_counter()-start
                results.append(dict(scheme=scheme,credentials=credentials,preexisting=preexisting,
                                    header_present='Proxy-Authorization' in prepared.headers,
                                    api_call_seconds=elapsed))
                session.close()
    print(json.dumps(dict(version=requests.__version__,module_path=requests.__file__,
                         network_guard=True,results=results,
                         wheels={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in wheels}),indent=2))


if __name__=='__main__':main()
