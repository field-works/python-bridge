#!/usr/bin/env python
# coding: utf-8

import unittest
import sys
import os

from field_reports import Bridge, ReportsError

class TestReports(unittest.TestCase):
    def setUp(self):
        self.reports = Bridge.create_proxy()

    def test_バージョンが取得できる(self):
        version = self.reports.version()
        self.assertEqual(version[:2], '2.')

    def test_JSON文字列を元にPDFを生成できる(self): 
        param = """{
            "template": {"paper": "A4"},
            "context": {
                "hello": {
                    "new": "Tx",
                    "value": "Hello, World!",
                    "rect": [100, 700, 400, 750]
                }
            }
        }"""
        pdf = self.reports.render(param)
        self.assertEqual(pdf[:8], b'%PDF-1.6')
        self.assertEqual(pdf[-6:], b'%%EOF\n')

    def test_辞書形式パラメータを元にPDFを生成できる(self): 
        param = {
            "template": {"paper": "A4"},
            "context": {
                "hello": {
                    "new": "Tx",
                    "value": "Hello, World!",
                    "rect": [100, 700, 400, 750]
                }
            }
        }
        pdf = self.reports.render(param)
        self.assertEqual(pdf[:8], b'%PDF-1.6')
        self.assertEqual(pdf[-6:], b'%%EOF\n')

    def test_パースエラーで例外が発生する(self): 
        with self.assertRaises(ReportsError):
            param = "{,}"
            pdf = self.reports.render(param)

    def test_PDFデータを解析できる(self):
        with open('tests/mitumori.pdf', 'rb') as f:
            result = self.reports.parse(f.read())
            self.assertIsInstance(result, dict)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestReports))
    return suite

if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(suite())
    if not result.wasSuccessful():
        sys.exit(1)
