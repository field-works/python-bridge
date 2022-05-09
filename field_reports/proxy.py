# -*- coding: utf-8 -*-

"""
Field Reportsの機能を呼び出すためのProxyインターフェースです。
"""
class Proxy:

    def version(self):
        """バージョン番号を取得します。

        Returns:
            str: バージョン番号

        Raised:
            ReportsError: Field Reportsとの連携に失敗した場合に発生
        """
        raise NotImplementedError()


    def render(self, param):
        """レンダリング・パラメータを元にレンダリングを実行します。

        Args:
            param (str|bytes|dict): JSON文字列または辞書形式レンダリング・パラメータ

        Returns:
            bytes: PDFデータ

        Raised:
            ReportsError: Field Reportsとの連携に失敗した場合に発生
        
        Note:
            ユーザーズ・マニュアル「第5章 レンダリングパラメータ」参照
        """
        raise NotImplementedError()

    def parse(self, pdf):
        """PDFデータを解析し，フィールドや注釈の情報を取得します。

        Args:
            pdf (bytes): PDFデータ

        Returns:
            dict: 解析結果

        Raised:
            ReportsError: Field Reportsとの連携に失敗した場合に発生
        """
        raise NotImplementedError()

    def to_jbytes(self, param):
        import json
        if isinstance(param, str):
            return param.encode('utf-8')
        elif isinstance(param, dict):
            return json.dumps(param, ensure_ascii=False).encode('utf-8')
        else:
            return param

class ReportsError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
