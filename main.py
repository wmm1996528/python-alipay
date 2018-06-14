import requests
from setting import *
import time
import base64
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA, SHA256
from Cryptodome.PublicKey import RSA
from urllib import parse
import logging
import json
class Alipay():
    def __init__(self):
        # self.appid = APPID
        self.return_url = 'http://wx918.vipgz1.idcfengye.com/ali/return'
        self.notify_url = 'http://wx918.vipgz1.idcfengye.com/ali/notify'
        self.appid = '2018032802460862'
        self.pubkey = PUBKEY
        self.alipay_public_key = RSA.importKey(ALIPAY_KEY)
        self.app_private_key = PRIVATEKEY
        # self.sign = 'ERITJKEIJKJHKKKKKKKHJEREEEEEEEEEEE'
        self.session = requests.session()
        self._sign_type = "RSA2"
        self.baseurl = 'https://openapi.alipay.com/gateway.do?'
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(funcName)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        self.logger = logging.getLogger('ali')
    def timestamp(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    def _ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])


    def sign(self, unsigned_string):
        key = RSA.import_key(PRIVATEKEY)
        h = SHA256.new(unsigned_string.encode())
        sign = PKCS1_v1_5.new(key).sign(h)
        return base64.b64encode(sign)  # 转码方便传递的格式
    def _verify(self, message, signature):
        # 开始计算签名
        key = RSA.import_key(ALIPAY_KEY)
        h = SHA256.new(message.encode())
        try:
            PKCS1_v1_5.new(key).verify(h, signature)
            return True
        except:
            return False

    def trade_precreate_pay(self, mount):
        '''
        alipay.trade.precreate(统一收单线下交易预创建)
        DOC : https://docs.open.alipay.com/api_1/alipay.trade.precreate
        :param mount: 支付金额
        :return:
        '''

        out_trade_no = str(int(time.time() * 100000))
        data = {
            'app_id': self.appid,
            'method': 'alipay.trade.precreate',
            'timestamp': self.timestamp(),
            'charset': 'utf-8',
            'sign_type': 'RSA2',
            'version': '1.0',
            'notify_url': self.notify_url,
            'return_url': self.return_url,
            'biz_content': {
                "body": '测试商品',
                "subject": '测试商品',
                "out_trade_no": out_trade_no,
                'total_amount': mount,
                # 支付方式
                # 'enable_pay_channels':'credit_group',
            }
        }
        unsigned_items = self._ordered_data(data)
        unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items)

        sign = self.sign(unsigned_string)
        ordered_items = self._ordered_data(data)
        quoted_string = "&".join("{}={}".format(k, parse.quote_plus(v)) for k, v in ordered_items)

        # 获得最终的订单信息字符串
        signed_string = self.baseurl + quoted_string + "&sign=" + parse.quote_plus(sign)
        res = self.session.post(signed_string).json()
        return res['alipay_trade_precreate_response']['qr_code']

    def trade_page_pay(self, mount):
        '''
        电脑网站支付
        DOC https://docs.open.alipay.com/270/alipay.trade.page.pay
        :param mount:
        :return:
        '''
        #随机订单号出来
        out_trade_no = str(int(time.time()*100000))
        data = {
            'app_id':self.appid,
            'method':'alipay.trade.page.pay',
            'timestamp':self.timestamp(),
            'charset':'utf-8',
            'sign_type':'RSA2',
            'version':'1.0',
            'notify_url': self.notify_url,
            'return_url': self.return_url,
            'biz_content':{
                "body":'测试商品',
                "subject":'测试商品',
                "out_trade_no":out_trade_no,
                'total_amount':mount,
                'product_code':'FAST_INSTANT_TRADE_PAY',
                'goods_type':'1',
                #支付方式
                # 'enable_pay_channels':'credit_group',
            }
        }
        unsigned_items = self._ordered_data(data)
        unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items)

        sign = self.sign(unsigned_string)
        ordered_items = self._ordered_data(data)
        quoted_string = "&".join("{}={}".format(k, parse.quote_plus(v)) for k, v in ordered_items)

        # 获得最终的订单信息字符串
        signed_string = self.baseurl+quoted_string + "&sign=" + parse.quote_plus(sign)
        # res = self.session.post(self.baseurl +signed_string)
        return signed_string

    def trade_wap_pay(self, mount):
        '''
        支付宝手机网站支付
        DOC https://docs.open.alipay.com/api_1/alipay.trade.wap.pay
        :param mount:
        :return:
        '''
        #随机订单号出来
        out_trade_no = str(int(time.time()*100000))
        data = {
            'app_id':self.appid,
            'method':'alipay.trade.wap.pay',
            'timestamp':self.timestamp(),
            'charset':'utf-8',
            'sign_type':'RSA2',
            'version':'1.0',
            'notify_url': 'http://wx918.vipgz1.idcfengye.com/ali/notify',
            'return_url': 'http://wx918.vipgz1.idcfengye.com/ali/return',
            'biz_content':{
                "body":'测试商品',
                "subject":'测试商品',
                "out_trade_no":out_trade_no,
                'total_amount':mount,
                'product_code':'QUICK_WAP_WAY',
                'goods_type':'1',
                #支付方式
                # 'enable_pay_channels':'credit_group',
            }
        }
        unsigned_items = self._ordered_data(data)
        unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items)

        sign = self.sign(unsigned_string)
        ordered_items = self._ordered_data(data)
        quoted_string = "&".join("{}={}".format(k, parse.quote_plus(v)) for k, v in ordered_items)

        # 获得最终的订单信息字符串
        signed_string = self.baseurl+quoted_string + "&sign=" + parse.quote_plus(sign)
        return signed_string
    def _build_body(self, data):
        unsigned_items = self._ordered_data(data)
        unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items)

        sign = self.sign(unsigned_string)
        ordered_items = self._ordered_data(data)
        quoted_string = "&".join("{}={}".format(k, parse.quote_plus(v)) for k, v in ordered_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + parse.quote_plus(sign)
        return signed_string

    def trans_toaccount(self, userid, mount):
        '''
        转账到支付宝账户

        :return:
        '''
        out_biz_no = str(int(time.time() * 100000))
        data = {
            'app_id': self.appid,
            'method': 'alipay.fund.trans.toaccount.transfer',
            'timestamp': self.timestamp(),
            'charset': 'utf-8',
            'sign_type': 'RSA2',
            'version': '1.0',
            'biz_content': {
                # ALIPAY_LOGONID：支付宝登录号，支持邮箱和手机号格式。
                # ALIPAY_USERID：支付宝账号对应的支付宝唯一用户号。以2088开头的16位纯数字组成。
                'payee_type':'ALIPAY_LOGONID',
                #转账用户
                'payee_account':userid,
                #转账金额
                'amount':mount,
                #备注 可选
                'remark':'退款',
                #付款方姓名 可选
                'payer_show_name':'啊啊是大家来看'
            }
        }
        signed_string = self._build_body(data)
        res = self.session.post(self.baseurl + signed_string)
        resd = res.json()
        if resd['alipay_fund_trans_toaccount_transfer_response']['code'] !='10000':
            self.logger.warning('转账失败：%s' % resd['alipay_fund_trans_toaccount_transfer_response']['sub_msg'])
    def trade_pay_query(self, atuh_code):
        '''
        查询订单交易状态
        :return:
        '''
        data = {
            'app_id': self.appid,
            'method': 'alipay.trade.query',
            'timestamp': self.timestamp(),
            'charset': 'utf-8',
            'sign_type': 'RSA2',
            'version': '1.0',
            'biz_content': {
                "out_trade_no": atuh_code, #根据商家订单号查询
            }
        }
        signed_string = self._build_body(data)
        res = self.session.post(self.baseurl + signed_string)
        query_res = self.get_string_to_be_signed(res.text)
        if query_res['code'] == '10000':
            query = {
                'trade_status': query_res['trade_status'], #交易状态
                'trade_no':query_res['trade_no'], #支付宝订单号
                'buyer_logon_id':query_res['buyer_logon_id'],#交易对象
                'total_amount':query_res['total_amount'],#总金额
                'send_pay_date':query_res['send_pay_date'],#交易时间
                'buyer_pay_amount':query_res['buyer_pay_amount'],#实际支付金额

            }
            return query
        else:
            self.logger.info(query_res)
    def get_string_to_be_signed(self, raw_string):
        data = json.loads(raw_string)
        sign = data['sign'] #签名
        to_be_sign_string = data['alipay_trade_query_response'] #待签名的字符串
        if not self._verify(str(to_be_sign_string), sign):
            print('失败')
        return to_be_sign_string


if __name__ == '__main__':
    ali = Alipay()
    print(ali.trade_page_pay('0.01'))

    # print(ali.trade_pay_query('152895920071762'))