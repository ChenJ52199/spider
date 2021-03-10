from fontTools.ttLib import TTFont


class MaoYanFont(object):
    def __init__(self):
        self._bytes2num = self._get_font_dict()

    def _get_font_dict(self):
        # 加载字体文件
        font = TTFont('maoyanfont.woff')

        # 保存为xml文件
        # font.saveXML('maoyanfont2.xml')

        # 字体编码和实际数字对应字典
        font_code2num = {
            'uniF4EF': 6,
            'uniF848': 3,
            'uniF88A': 7,
            'uniE7A1': 9,
            'uniE343': 1,
            'uniE137': 8,
            'uniF489': 0,
            'uniE5E2': 4,
            'uniF19B': 2,
            'uniE8CD': 5,
        }

        # 获取所有字体编码 去除前两个
        font_code_list = font.getGlyphOrder()[2:]

        # 建立字体对象和实际表示的数字之间的对应关系
        # font['glyf']['uniF4EF'].coordinates.array  # 获取对应字体编码对应的字体对象的数组格式
        return {font['glyf'][font_code].coordinates.array.tobytes(): font_code2num[font_code]
                for font_code in font_code_list}

    def get_num(self, font_code, font_file_path):
        '''
        获取字体编码对应的实际数字
        :param font_code: 字体编码
        :param font_file_path: 当前字体文件路径
        :return:
        '''
        if font_code == '.':
            return '.'
        font_code_ = 'uni' + '%x'.upper() % ord(font_code)
        # print(font_code_)
        font_bytes = TTFont(font_file_path)['glyf'][font_code_].coordinates.array.tobytes()
        # print(font_bytes)
        return str(self._bytes2num.get(font_bytes, None))


get_num = MaoYanFont().get_num
