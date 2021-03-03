import requests
import json
import re
import js2py


class BaiDuTranslate(object):
    '''百度翻译爬虫'''

    def __init__(self):
        self.base_url = 'https://fanyi.baidu.com/'
        self.base_trans_url = 'https://fanyi.baidu.com/basetrans'
        self.session = requests.Session()
        self.context = js2py.EvalJs()  # 创建执行js的环境

        self.headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }

    def langdetect(self, from_str):
        '''获取需要翻译的词句是哪种语言'''
        data = {'query': from_str}
        response = self.session.post('https://fanyi.baidu.com/langdetect',
                                     data=data, headers=self.headers).content.decode()
        response_data = json.loads(response)
        return response_data.get('lan')

    def get_token_and_gtk(self):
        '''获取token和gtk'''
        self.session.get(self.base_url)
        response = self.session.get(self.base_url)
        token = re.findall(r"token: '(.+?)',", response.content.decode())[0]
        gtk = re.findall(r"window.gtk = '(.+?)'", response.content.decode())[0]
        return token, gtk

    def get_sign(self, from_str, gtk):
        js_code = r'''
        function n(r, o) {
            for (var t = 0; t < o.length - 2; t += 3) {
                var e = o.charAt(t + 2);
                e = e >= "a" ? e.charCodeAt(0) - 87 : Number(e),
                e = "+" === o.charAt(t + 1) ? r >>> e : r << e,
                r = "+" === o.charAt(t) ? r + e & 4294967295 : r ^ e
            }
            return r
        }
        function a(r) {
            var t = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
            if (null === t) {
                var a = r.length;
                a > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(a / 2) - 5, 10) + r.substr(-10, 10))
            } else {
                for (var C = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), h = 0, f = C.length, u = []; f > h; h++)
                    "" !== C[h] && u.push.apply(u, e(C[h].split(""))),
                    h !== f - 1 && u.push(t[h]);
                var g = u.length;
                g > 30 && (r = u.slice(0, 10).join("") + u.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + u.slice(-10).join(""))
            }
            var l = void 0
              , d = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
            l = null !== i ? i : (i = o.common[d] || "") || "";
            for (var m = l.split("."), S = Number(m[0]) || 0, s = Number(m[1]) || 0, c = [], v = 0, F = 0; F < r.length; F++) {
                var p = r.charCodeAt(F);
                128 > p ? c[v++] = p : (2048 > p ? c[v++] = p >> 6 | 192 : (55296 === (64512 & p) && F + 1 < r.length && 56320 === (64512 & r.charCodeAt(F + 1)) ? (p = 65536 + ((1023 & p) << 10) + (1023 & r.charCodeAt(++F)),
                c[v++] = p >> 18 | 240,
                c[v++] = p >> 12 & 63 | 128) : c[v++] = p >> 12 | 224,
                c[v++] = p >> 6 & 63 | 128),
                c[v++] = 63 & p | 128)
            }
            for (var w = S, A = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), b = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), D = 0; D < c.length; D++)
                w += c[D],
                w = n(w, A);
            return w = n(w, b),
            w ^= s,
            0 > w && (w = (2147483647 & w) + 2147483648),
            w %= 1e6,
            w.toString() + "." + (w ^ S)
        }
        '''
        # 替换gtk值
        js_code = js_code.replace('null !== i ? i : (i = o.common[d] || "") || ""', '"' + gtk + '"')
        # print(js_code)
        self.context.execute(js_code)
        sign = self.context.a(from_str)  # 调用js函数生成sign
        # print(sign)
        return sign

    def get_data(self):
        token, gtk = self.get_token_and_gtk()
        from_lan = self.langdetect(from_str)
        to_lan = 'en' if from_lan == 'zh' else 'zh'
        sign = self.get_sign(from_str, gtk)
        data = {
            'from': from_lan,
            'to': to_lan,
            'token': token,
            'sign': sign
        }
        # print(data)
        return data

    def run(self, from_str):
        data = self.get_data()
        data['query'] = from_str
        response = self.session.post(url=self.base_trans_url, data=data, headers=self.headers).content.decode()
        # print(response)
        return json.loads(response)['trans'][0]['dst']


if __name__ == '__main__':
    translator = BaiDuTranslate()
    while True:
        from_str = input('输入要翻译的词句(输入q退出):')
        if from_str == 'q':
            break
        print(translator.run(from_str))
