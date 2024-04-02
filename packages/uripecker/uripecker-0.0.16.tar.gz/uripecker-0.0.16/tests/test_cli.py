import shutil
import tempfile
import unittest

import uripecker.__main__

import myatf


def nlsplit(text):
    tmp = text
    if text[-1] == '\n':
        tmp = text[:-1]
    return tmp.split('\n')


def nljoin(lines):
    return '\n'.join(lines) + '\n'


def maybe_nljoin(lines):
    if type(lines) is list:
        return '\n'.join(lines) + '\n'
    elif type(lines) is str:
        return lines
    else:
        return str(lines)


class BadSyntaxMapFileCase(myatf.case.FileCase):

    name = 'bad_syntax.map'

    def build_lines(self):
        return [
            'foo bar'
        ]


class MissingPlaceholderFileCase(myatf.case.FileCase):

    name = 'missing_placeholder.map'

    def build_lines(self):
        return [
            'bz = http://bugzilla.example.com/?query=%s',
            'g = http://google.example.com/search?q=%s',
            'storage = ftp://joe:secret@storage%s.files.example.com/',
            'issue = http://gitlab.example.org/issue?id=%s',
            'faq = http://faq.example.org/faq/',
        ]


class EmptyMapFileCase(myatf.case.FileCase):

    name = 'empty.map'


class EmptyTextFileCase(myatf.case.FileCase):

    name = 'empty.txt'


class NormalTextFileCase(myatf.case.FileCase):

    name = 'normal.txt'

    def build_lines(self):
        return [
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
        ]


class NormalMapFileCase(myatf.case.FileCase):

    name = 'normal.map'

    def build_lines(self):
        return [
            'bz = http://bugzilla.example.com/?query=%s',
            'g = http://google.example.com/search?q=%s',
            'storage = ftp://joe:secret@storage%s.files.example.com/',
            'issue = http://gitlab.example.org/issue?id=%s',
            'faq = http://faq.example.org/faq/%s',
        ]


class ShellOracle:

    def __init__(self, out=None, err=None, es=None):
        self.out = maybe_nljoin(out) if out else ''
        self.err = maybe_nljoin(err) if err else ''
        self.es = es if es else 0


class ShellResult:

    @staticmethod
    def _normalize_tb(err):
        if not err.startswith('Traceback (most recent call last):'):
            return err
        out = []
        lines = nlsplit(err)
        out.append(lines.pop(0))
        while lines:
            if lines[0].startswith('  File'):
                lines.pop(0)
                continue
            elif lines[0].startswith('    '):
                lines.pop(0)
                continue
            else:
                break
        out.extend(lines)
        return nljoin(out)

    @classmethod
    def normalize_shresult(cls, shresult):
        es = shresult.es
        out = shresult.out
        err = cls._normalize_tb(shresult.err)
        return cls(out=out, err=err, es=es)

    def __init__(self, out=None, err=None, es=None):
        self.out = maybe_nljoin(out) if out else ''
        self.err = maybe_nljoin(err) if err else ''
        self.es = es if es else 0


class ArgSet:

    def __init__(self, *args):
        self.args = args

    def fmt(self):
        return ' '.join(self.args)


class FileSet:

    def __init__(self, *files):
        self.files = files

    def fmt(self):
        return ' '.join([f.path for f in self.files])


class MainTest(unittest.TestCase):

    def setUp(self, *args, **kwargs):
        self.maxDiff = None
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def prep_fileset(self, mapfile_cls, textfile_cls):
        mapfile = mapfile_cls(root=self.tmp)
        textfile = textfile_cls(root=self.tmp)
        mapfile.create()
        textfile.create()
        return FileSet(mapfile, textfile)

    def runTest(self, fileset, oracle):
        shresult = myatf.sh.ShellScript(
            code=f'python3 -m uripecker {fileset.fmt()}',
            name='test_cli',
        ).run()
        result = ShellResult.normalize_shresult(shresult)
        if not result.es == oracle.es:
            print("===RESULT.ES/===")
            print(result.es)
            print("===/RESULT.ES===")
            print("===ORACLE.ES/===")
            print(oracle.es)
            print("===/ORACLE.ES===")
        if not result.out == oracle.out:
            print("===RESULT.OUT/===")
            print(result.out)
            print("===/RESULT.OUT===")
            print("===ORACLE.OUT/===")
            print(oracle.out)
            print("===/ORACLE.OUT===")
        if not result.err == oracle.err:
            print("===RESULT.ERR/===")
            print(result.err)
            print("===/RESULT.ERR===")
            print("===ORACLE.ERR/===")
            print(oracle.err)
            print("===/ORACLE.ERR===")
        self.assertEqual(result.es, oracle.es)
        self.assertEqual(result.out, oracle.out)
        self.assertEqual(result.err, oracle.err)

    def test_normal(self):
        self.runTest(
            fileset=self.prep_fileset(
                NormalMapFileCase,
                NormalTextFileCase,
            ),
            oracle=ShellOracle(
                out=[
                    "http://other.example.com/",
                    "https://secure.example.com/",
                    "https://secure.example.com/foo?id=2&name=bar+baz",
                    "https://urlescape.example.com/foo?name=Jan"
                    "%20%C5%A0varn%C3%BD%2C%20bytem%20%C5%98e"
                    "%C4%8Dkovice%2017",
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
            ),
        )

    def test_bad_syntax_map(self):
        self.runTest(
            fileset=self.prep_fileset(
                BadSyntaxMapFileCase,
                NormalTextFileCase,
            ),
            oracle=ShellOracle(
                es=1,
                err=[
                    'Traceback (most recent call last):',
                    'ValueError: not enough values to unpack'
                    ' (expected 2, got 1)'
                ]
            ),
        )

    def test_missing_placeholder_map(self):
        self.runTest(
            fileset=self.prep_fileset(
                MissingPlaceholderFileCase,
                NormalTextFileCase,
            ),
            oracle=ShellOracle(
                es=0,
                out=[
                    "http://other.example.com/",
                    "https://secure.example.com/",
                    "https://secure.example.com/foo?id=2&name=bar+baz",
                    "https://urlescape.example.com/foo?name=Jan"
                    "%20%C5%A0varn%C3%BD%2C%20bytem%20%C5%98e"
                    "%C4%8Dkovice%2017",
                    "http://anchor.example.org/foo/bar.html#baz",
                    "ftp://joe:secret@files.example.com/",
                    "http://localhost:15779/some//w+ird/@thing=/",
                    "http://example.com/normal/url",
                    "http://gitlab.example.org/issue?id=1",
                    "http://gitlab.example.org/issue?id=42",
                    "ftp://joe:secret@storage42.files.example.com/",
                ],
                err=[
                    "uripecker:ignoring pattern without '%s':"
                    " faq = http://faq.example.org/faq/"
                ]
            ),
        )

    def test_usage(self):
        self.runTest(
            fileset=ArgSet(),
            oracle=ShellOracle(
                es=2,
                err=[
                    'usage: python3 -m uripecker PATTERN_MAP_FILE [SOURCE_TEXT_FILE]',
                    'usage: python3 -m uripecker --help',
                    'usage: python3 -m uripecker --version',
                    '',
                    'missing PATTERN_MAP_FILE',
                ]
            ),
        )

    def test_help(self):
        self.runTest(
            fileset=ArgSet('--help'),
            oracle=ShellOracle(
                es=0,
                out=uripecker.__main__._HELP_TEXT.strip().split('\n')
            ),
        )

    def test_version(self):
        self.runTest(
            fileset=ArgSet('--version'),
            oracle=ShellOracle(
                es=0,
                out=uripecker._meta.VERSION.strip().split('\n')
            ),
        )
