#!/usr/bin/env python

import subprocess
from typing import IO
from field_reports.proxy import *

class ExecProxy(Proxy):
    def __init__(self, exe_path: str, cwd: str,
        loglevel: int, logout: IO):
        self.exe_path = exe_path
        self.cwd = cwd
        self.loglevel = loglevel
        self.logout = logout

    def version(self) -> str:
        try:
            proc = subprocess.Popen(
                [self.exe_path, 'version'],
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            out, err = proc.communicate()
            self.logout.write(err.decode('utf-8'))
            if proc.returncode != 0:
                raise RuntimeError("Exit Code = {0}".format(proc.returncode))
            return out.decode()
        except Exception as exn:
            raise ReportsError(self._exn_message(exn)) from exn

    def render(self, param: ReportsParam) -> bytes:
        try:
            proc = subprocess.Popen(
                [self.exe_path, 'render', '-l' + str(self.loglevel), '-', '-'],
                cwd=self.cwd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            out, err = proc.communicate(self.to_jbytes(param))
            self.logout.write(err.decode('utf-8'))
            if proc.returncode != 0:
                raise RuntimeError("Exit Code = {0}".format(proc.returncode))
            return out
        except Exception as exn:
            raise ReportsError(self._exn_message(exn)) from exn

    def parse(self, pdf: bytes) -> dict:
        import json
        try:
            proc = subprocess.Popen(
                [self.exe_path, 'parse', '-'],
                cwd=self.cwd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            out, err = proc.communicate(pdf)
            self.logout.write(err.decode('utf-8'))
            if proc.returncode != 0:
                raise RuntimeError("Exit Code = {0}".format(proc.returncode))
            return json.loads(out.decode('utf-8'))
        except Exception as exn:
            raise ReportsError(self._exn_message(exn)) from exn
    
    def _exn_message(self, exn):
        return "Process terminated abnormally: {0}.".format(exn)