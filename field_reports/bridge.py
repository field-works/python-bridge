# -*- coding: utf-8 -*-
import sys
import os
from field_reports.http_proxy import HttpProxy
from field_reports.exec_proxy import ExecProxy

"""
Field Reportsと連携するためのProxyオブジェクトを生成します。
"""
class Bridge:
    @staticmethod
    def create_proxy(uri = None):
        """引数で与えられるURIに応じたField Reports Proxyオブジェクトを返却します。

        Example:
            >>> # コマンド連携時
            >>> from field_reports import Bridge
            >>> reports = Bridge.create_proxy("exec:/usr/local/bin/reports?cwd=/usr/share&amp;logleve=3");

        Example:
            >>> # HTTP連携時
            >>> from field_reports import Bridge
            >>> reports = Bridge.create_proxy("http://localhost:50080/");
        
        Args:
            uri (str, optional): Field Reportsとの接続方法を示すURI．
            省略した場合，環境変数'REPORTS_PROXY'よりURIを取得します.   
            環境変数'REPORTS_PROXY'も未設定の場合のURIは，"exec:reports"とします。

            コマンド連携時:

                "exec:{exePath}?cwd={cwd}&loglevel={logLevel}"

            - cwd, loglevelは省略可能です。
            - loglevelが0より大きい場合，標準エラー出力にログを出力します。

            HTTP連携時:

                "http://{hostName}:{portNumber}/"

        Returns:
            Proxy: Field Reports Proxyオブジェクト

        """
        from six.moves.urllib import parse
        uri = os.environ.get('REPORTS_PROXY', "exec:reports") if not uri else uri
        u = parse.urlparse(uri);
        if u.scheme == 'exec':
            q = parse.parse_qs(u.query)
            exe_path = u.path
            cwd = q['cwd'] if 'cwd' in q else "."
            loglevel = int(q['loglevel']) if 'loglevel' in q else 0
            return Bridge.create_exec_proxy(exe_path, cwd, loglevel, sys.stderr)
        else:
            return Bridge.create_http_proxy(uri)

    @staticmethod
    def create_exec_proxy(
        exe_path="reports", cwd=".",
        loglevel=0, logout=sys.stderr):
        """コマンド呼び出しによりField Reportsと連携するProxyオブジェクトを生成します。

        Args:
            exe_path (str, optional): Field Reportsコマンドのパス
            cwd (str, optional): Field Reportsプロセス実行時のカレントディレクトリ
            loglevel (int, optional): ログ出力レベル
            logout (TextIO, optional): ログ出力先Stream

        Returns:
            Proxy: Field Reports Proxyオブジェクト
        """
        return ExecProxy(exe_path, cwd, loglevel, logout)

    @staticmethod
    def create_http_proxy(base_address="http://localhost:50080/"):
        """HTTP通信によりField Reportsと連携するProxyオブジェクトを生成します。

        Args:
            base_address (str, optional): ベースUri

        Returns:
            Proxy: Field Reports Proxyオブジェクト

        Note:
            reportsコマンドがサーバーモードで起動していることが前提となります。

            $ reports server -l3
        """
        return HttpProxy(base_address)
