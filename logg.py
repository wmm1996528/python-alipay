import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText
class mailLog():
    def __init__(self):
        # 第三方 SMTP 服务
        self.mail_host = "smtp.163.com"      # SMTP服务器
        self.mail_user = "wmm1996528@163.com"                  # 用户名
        self.mail_pass = "aq918927"               # 授权密码，非登录密码

        self.sender = 'wmm1996528@163.com'    # 发件人邮箱(最好写全, 不然会失败)
        self.receivers = ['912594746@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


    def sendEmail(self, title, content):

        message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
        message['From'] = "{}".format(self.sender)
        message['To'] = ",".join(self.receivers)
        message['Subject'] = title

        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(self.mail_user, self.mail_pass)  # 登录验证
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())  # 发送
            print("mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(e)


class logText():
    def __init__(self, name):
        self.name = name
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(funcName)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        self.logger = logging.getLogger(name)
        # fh = logging.FileHandler(name+'.txt', mode='a',delay=False)
        # formatter = logging.Formatter("%(asctime)s - %(funcName)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        # fh.setFormatter(formatter)
        # self.logger.addHandler(fh)
        self.mail = mailLog()
    def warning(self,msg):
        return self.logger.warning(msg)
    def info(self,msg):
        self.logger.info(msg)
    def debug(self,msg):
        self.logger.debug(msg)
    def error(self,msg):
        self.logger.error(msg)
        self.mail.sendEmail(self.name, msg)

    def toDict(self,text):
        '''
        将 headers 或 form-data
        转为dict
        方便使用
        :param text:
        :return:
        '''
        newDict = {}
        for i in text.split('\n'):
            a = i.split(':')
            newDict[a[0]] = a[1]
        return newDict




if __name__ == '__main__':
    log = logText('masdkjlasd')
    log.error('asd')


