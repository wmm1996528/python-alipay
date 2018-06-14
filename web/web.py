from flask import Flask
from flask import *
import mysql.connector
app = Flask(__name__)
conn = mysql.connector.connect(host='47.98.165.242',user='root', password='123456',db='alipay')
cursor = conn.cursor()
@app.route('/ali/return')
def return_page():
    return 'zhifuchengg le '


@app.route('/ali/notify', methods=['POST'])
def notify():
    if request.method == 'POST':
        data = request.form
        notify_time = data.get('notify_time')
        notify_type = data.get('notify_type')
        notify_id = data.get('notify_id')
        app_id = data.get('app_id')
        sign = data.get('sign')
        trade_no = data.get('trade_no')
        buyer_logon_id = data.get('buyer_logon_id')
        trade_status = data.get('trade_status')
        total_amount = data.get('total_amount')
        receipt_amount = data.get('receipt_amount')
        version = data.get('version')
        gmt_payment = data.get('gmt_payment')
        print(trade_status)
        return trade_status
def parse_notify():
    pass

if __name__ == '__main__':
    app.run()
    sql = '''insert alipay.trade 
(user,trade_no,code,total_amount,buyer_logon_id)
values(%s, "%s", '%s', '%s', '%s');
'''
    cursor.execute(sql)
    conn.commit()