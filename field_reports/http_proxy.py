#!/usr/bin/env python

from urllib import request, parse, error
from field_reports.proxy import *

class HttpProxy(Proxy):
    def __init__(self, base_address: str):
        self.base_address = base_address

    def version(self) -> str:
        try:
            req = request.Request(parse.urljoin(self.base_address, "version"))
            with request.urlopen(req) as res:
                return res.read().decode().rstrip()
        except error.HTTPError as exn:
            raise ReportsError(self._http_exn_message(exn)) from exn
        except Exception as exn:
            raise ReportsError(self._exn_message(exn)) from exn

    def render(self, param: ReportsParam) -> bytes:
        try:
            req = request.Request(
                parse.urljoin(self.base_address, "render"),
                headers = {'content-type': 'application/json'},
                data = self.to_jbytes(param))
            with request.urlopen(req) as res:
                return res.read()
        except error.HTTPError as exn:
            raise ReportsError(self._http_exn_message(exn)) from exn
        except Exception as exn:
            raise ReportsError(self._exn_message(exn)) from exn

    def parse(self, pdf: bytes) -> dict:
        import json
        try:
            req = request.Request(
                parse.urljoin(self.base_address, "parse"),
                headers = {'content-type': 'application/pdf'},
                data = pdf)
            with request.urlopen(req) as res:
                return json.loads(res.read().decode('utf-8'))
        except error.HTTPError as exn:
            raise ReportsError(self._http_exn_message(exn)) from exn
        except Exception as exn:
            raise ReportsError(self._exn_message(exn)) from exn

    def _exn_message(self, exn):
        return "Fail to HTTP comunication: {0}.".format(str(exn))

    def _http_exn_message(self, exn):
        return "Fail to HTTP comunication: Status Code = {0}, Reason = {1}, Response = {2}.".format(exn.code, exn.reason, exn.read().decode('utf-8'))