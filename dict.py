from __future__ import unicode_literals
import sys
import json
import re

__name__ = 'dict-cli'
__version__ = '1.3.4'
__description__ = '命令行下中英文翻译工具（Chinese and English translation tools in the command line）'
__keywords__ = 'Translation English2Chinese Chinese2English Command-line'
__author__ = 'Feei'
__contact__ = 'feei@feei.cn'
__url__ = 'https://github.com/wufeifei/dict'
__license__ = 'MIT'

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    from urllib.parse import quote
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    from urllib import quote


class Dict:
    key = '716426270'
    keyFrom = 'wufeifei'
    api = 'http://fanyi.youdao.com/openapi.do' \
          '?keyfrom=wufeifei&key=716426270&type=data&doctype=json&version=1.1&q='
    content = None

    def __init__(self, argv):
        message = ''
        if len(argv) > 0:
            for s in argv:
                message = message + s + ' '
            self.api = self.api + quote(message.encode('utf-8'))
            self.translate()
        else:
            print('Usage: dict test')

    def translate(self):
        try:
            content = urlopen(self.api).read()
            self.content = json.loads(content.decode('utf-8'))
            output = self.parse()
            return output
        except Exception as e:
            print('ERROR: Network or remote service error!')
            print(e)

    def parse(self):
        output = ''
        code = self.content['errorCode']
        if code == 0:  # Success
            c = None
            try:
                u = self.content['basic']['us-phonetic']  # English
                e = self.content['basic']['uk-phonetic']
            except KeyError:
                try:
                    c = self.content['basic']['phonetic']  # Chinese
                except KeyError:
                    c = 'None'
                u = 'None'
                e = 'None'

            try:
                explains = self.content['basic']['explains']
            except KeyError:
                explains = 'None'

            try:
                phrase = self.content['web']
            except KeyError:
                phrase = 'None'

            s = '{0} {1}'.format(
                self.content['query'], self.content['translation'][0])
            output = output + s + '\n'

            if u != 'None':
                s = '(U: {0} E: {1})'.format(u, e)
                output = output + s + '\n'
            elif c != 'None':
                s = '(Pinyin: {0})'.format(c)
            else:
                pass

            if explains != 'None':
                for i in range(0, len(explains)):
                    s = '{0}'.format(explains[i])
                    # output = output + s + '\n'
            else:
                s = 'Explains None'
                output = output + s + '\n'


            if phrase != 'None':
                for p in phrase:
                    s = '{0} : {1}'.format(
                        p['key'], p['value'][0])
                    output = output + s + '\n'
                    if len(p['value']) > 0:
                        if re.match('[ \u4e00 -\u9fa5]+', p['key']) is None:
                            blank = len(p['key'].encode('gbk'))
                        else:
                            blank = len(p['key'])
                        for i in p['value'][1:]:
                            s = '{0} {1}'.format(
                                ' ' * (blank + 3), i)
                            output = output + s + '\n'

        elif code == 20:  # Text to long
            print('WORD TO LONG')
        elif code == 30:  # Trans error
            print('TRANSLATE ERROR')
        elif code == 40:  # Don't support this language
            print('CAN\'T SUPPORT THIS LANGUAGE')
        elif code == 50:  # Key failed
            print('KEY FAILED')
        elif code == 60:  # Don't have this word
            print('DO\'T HAVE THIS WORD')

        return output

# dc = Dict(['hello'])
# result = dc.translate()
# print(result)