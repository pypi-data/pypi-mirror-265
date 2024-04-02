import unittest

import uripecker


def nljoin(lines):
    return '\n'.join(lines) + '\n'


class MainTest(unittest.TestCase):

    def runTest(self, test_lines, oracle_lines):
        test = nljoin(test_lines)
        oracle = nljoin(oracle_lines)
        result = nljoin(uripecker.peck(
            pmap={
                'bz': 'http://bugzilla.example.com/?query=%s',
                'g': 'http://google.example.com/search?q=%s',
                'storage': 'ftp://joe:secret@storage%s.files.example.com/',
                'issue': 'http://gitlab.example.org/issue?id=%s',
                'faq': 'http://faq.example.org/faq/%s',
            },
            text=test
        ))
        if not result == oracle:
            print('====RESULT/====')
            print(result)
            print('====/RESULT====')
            print('====ORACLE/====')
            print(oracle)
            print('====/ORACLE====')
        self.assertEqual(result, oracle)

    def testIsTrue(self):
        self.assertTrue(uripecker)

    def test_uri(self):
        self.runTest(
            test_lines=[
                "http://distinct.uri1.example.com/",
            ],
            oracle_lines=[
                "http://distinct.uri1.example.com/",
            ],
        )

    def test_uris(self):
        self.runTest(
            test_lines=[
                "http://distinct.uri1.example.com/",
                "also http://distinct.uri2.example.com/get",
                "http://distinct.uri3.example.com/?x=1 as well",
                "http://44.33.222.111:8080/",
                "then there's http://distinct.uri4.example.com/?x=1&y=2"
                " as well",
                "and finally:",
                "http://distinct.uri5.example.com/get?x=1&y=2&foo=bar+%20+baz",
                "http://distinct.uri6.example.com:350/",
                "https://taggy.uri.example.com/69698d2d-g219-looksliketag",
                "https://hashy.uri.example.com/69698d2d-#g220-lookslikehash",
                "https://expy.uri.example.com/69698d2d-g=lookslikeexp",
            ],
            oracle_lines=[
                "http://distinct.uri1.example.com/",
                "http://distinct.uri2.example.com/get",
                "http://distinct.uri3.example.com/?x=1",
                "http://44.33.222.111:8080/",
                "http://distinct.uri4.example.com/?x=1&y=2",
                "http://distinct.uri5.example.com/get?x=1&y=2&foo=bar+%20+baz",
                "http://distinct.uri6.example.com:350/",
                "https://taggy.uri.example.com/69698d2d-g219-looksliketag",
                "https://hashy.uri.example.com/69698d2d-#g220-lookslikehash",
                "https://expy.uri.example.com/69698d2d-g=lookslikeexp",
            ],
        )

    def test_id(self):
        self.runTest(
            test_lines=[
                "bz#123456789",
            ],
            oracle_lines=[
                "http://bugzilla.example.com/?query=123456789",
            ],
        )

    def test_ids(self):
        self.runTest(
            test_lines=[
                "bz#1",
                "BZ#999",
                "also bz#2",
                "also bz#345 as well",
                "then there's bz#42 as well",
                "and finally:",
                "bz#6789",
            ],
            oracle_lines=[
                "http://bugzilla.example.com/?query=1",
                "http://bugzilla.example.com/?query=999",
                "http://bugzilla.example.com/?query=2",
                "http://bugzilla.example.com/?query=345",
                "http://bugzilla.example.com/?query=42",
                "http://bugzilla.example.com/?query=6789",
            ],
        )

    def test_exp(self):
        self.runTest(
            test_lines=[
                "bz = 123456789",
            ],
            oracle_lines=[
                "http://bugzilla.example.com/?query=123456789",
            ],
        )

    def test_exps(self):
        self.runTest(
            test_lines=[
                "bz = 1",
                "also bz = 2",
                "also bz = 345 as well",
                "then there's bz = 42 as well",
                "and finally:",
                "bz = 6789",
            ],
            oracle_lines=[
                "http://bugzilla.example.com/?query=1",
                "http://bugzilla.example.com/?query=2",
                "http://bugzilla.example.com/?query=345",
                "http://bugzilla.example.com/?query=42",
                "http://bugzilla.example.com/?query=6789",
            ],
        )

    def test_tag(self):
        self.runTest(
            test_lines=[
                "bz123456789",
            ],
            oracle_lines=[
                "http://bugzilla.example.com/?query=123456789",
            ],
        )

    def test_tags(self):
        self.runTest(
            test_lines=[
                "bz1",
                "bz345 as well",
                "and finally:",
                "bz6789",
            ],
            oracle_lines=[
                "http://bugzilla.example.com/?query=1",
                "http://bugzilla.example.com/?query=345",
                "http://bugzilla.example.com/?query=6789",
            ],
        )

    def test_kw(self):
        self.runTest(
            test_lines=[
                "g foo",
            ],
            oracle_lines=[
                "http://google.example.com/search?q=foo",
            ],
        )

    def test_kws(self):
        self.runTest(
            test_lines=[
                "g foo",
                "g  bar",
                "g baz qux quux",
                "g learn 中文 in no time",
            ],
            oracle_lines=[
                "http://google.example.com/search?q=foo",
                "http://google.example.com/search?q=bar",
                "http://google.example.com/search?q=baz+qux+quux",
                "http://google.example.com/search?q=learn"
                "+%E4%B8%AD%E6%96%87+in+no+time",
            ],
        )

    def test_mixed(self):
        self.runTest(
            test_lines=[
                "issue = 1",
                "http://other.example.com/",
                "faq#225",
                "https://secure.example.com/",
                "issue42",
                "https://secure.example.com/foo?id=2&name=bar+baz",
                "faq 14",
                "https://urlescape.example.com/foo?name=Jan"
                "%20%C5%A0varn%C3%BD%2C%20bytem%20%C5%98e%C4%8Dkovice%2017",
                "or faq 15",
                "http://anchor.example.org/foo/bar.html#baz",
                "ftp://joe:secret@files.example.com/",
                "storage 42",
                "http://localhost:15779/some//w+ird/@thing=/  ",
                "I like to look like *a GMail produced link"
                " <http://example.com/normal/url>.*  Is it OK?",
            ],
            oracle_lines=[
                "http://other.example.com/",
                "https://secure.example.com/",
                "https://secure.example.com/foo?id=2&name=bar+baz",
                "https://urlescape.example.com/foo?name=Jan"
                "%20%C5%A0varn%C3%BD%2C%20bytem%20%C5%98e%C4%8Dkovice%2017",
                "http://anchor.example.org/foo/bar.html#baz",
                "ftp://joe:secret@files.example.com/",
                "http://localhost:15779/some//w+ird/@thing=/",
                "http://example.com/normal/url",
                "http://faq.example.org/faq/225",
                "http://gitlab.example.org/issue?id=1",
                "http://gitlab.example.org/issue?id=42",
                "http://faq.example.org/faq/14",
                "ftp://joe:secret@storage42.files.example.com/",
            ],
        )

    def test_uris_in_lang(self):
        self.runTest(
            test_lines=[
                'Hello,',
                '',
                'please download the new version here:'
                ' https://build.example.com/new#build.',
                'Full changelog can be found at release notes'
                ' page(http://release.example.com/cl/v1.2.0)'
                ' within few minutes.',
                '',
                'Cheers,',
                'Joe',
                '',
                '-- ',
                'Joe the Builder',
                'http://joe.example.com/joe#contact',
            ],
            oracle_lines=[
                'https://build.example.com/new#build',
                'http://release.example.com/cl/v1.2.0',
                'http://joe.example.com/joe#contact',
            ],
        )

