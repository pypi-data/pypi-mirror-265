from typing import Any, Sequence, Optional, Iterable
from wsgiref.types import WSGIApplication, WSGIEnvironment, StartResponse

class CGIRootFix:
    app: Any
    app_root: Any
    def __init__(self, app, app_root: str = ...): ...
    def __call__(self, environ, start_response): ...

LighttpdCGIRootFix: Any

class PathInfoFromRequestUriFix:
    app: Any
    def __init__(self, app): ...
    def __call__(self, environ, start_response): ...

class ProxyFix(object):
    app: WSGIApplication
    num_proxies: int
    def __init__(self, app: WSGIApplication, num_proxies: int = ...) -> None: ...
    def get_remote_addr(self, forwarded_for: Sequence[str]) -> Optional[str]: ...
    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]: ...

class HeaderRewriterFix:
    app: Any
    remove_headers: Any
    add_headers: Any
    def __init__(self, app, remove_headers: Optional[Any] = ..., add_headers: Optional[Any] = ...): ...
    def __call__(self, environ, start_response): ...

class InternetExplorerFix:
    app: Any
    fix_vary: Any
    fix_attach: Any
    def __init__(self, app, fix_vary: bool = ..., fix_attach: bool = ...): ...
    def fix_headers(self, environ, headers, status: Optional[Any] = ...): ...
    def run_fixed(self, environ, start_response): ...
    def __call__(self, environ, start_response): ...
