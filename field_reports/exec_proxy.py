# -*- coding: utf-8 -*-
from six import raise_from
import subprocess
from field_reports.proxy import *

class ExecProxy(Proxy):
    def __init__(self, exe_path, cwd, loglevel, logout):
        self.exe_path = exe_path
        self.cwd = cwd
        self.loglevel = loglevel
        self.logout = logout

    def version(self):
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
            return out.decode().rstrip()
        except Exception as exn:
            raise_from(ReportsError(self._exn_message(exn)), exn)

    def render(self, param):
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
            raise_from(ReportsError(self._exn_message(exn)), exn)

    def parse(self, pdf):
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
            raise_from(ReportsError(self._exn_message(exn)), exn)
    
    def _exn_message(self, exn):
        return "Process terminated abnormally: {0}.".format(exn)