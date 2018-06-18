from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr,formataddr
import smtplib
import re
import time

from news import Get_url

'''
@将转化邮件地址为email模块可以识别的地址
'''
def _format_addr(s):
    name,addr = parseaddr(s)
    print(name,addr)
    return formataddr((Header(name,'utf-8').encode(),addr))

'''
@判断邮件地址是否正确
'''
def judue_mail(mail):
    str = r"[^\._][\w\._-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$"
    res = re.match(str,mail)
    return res

'''
@用户输入信息
'''
def get_user_info():
    user_mail = input("请输入自己的邮箱（发件人）：")
    if not judue_mail(user_mail):
        user_mail = " "
    passwd = input("请输入密码(邮箱授权码)：")
    send_mail = input("请输入目的邮箱（收件人）：")
    if not judue_mail(send_mail):
        user_mail = " "
    return user_mail,passwd,send_mail

'''
@发送邮件
'''
def sendmail(text,user_mail,passwd,send_mail):
    # user_mail = "1075479026@qq.com"
    # #passwd = "yang1994@"
    # passwd = "uwzhcgusqpzwheff"
    # send_mail = "yy_dgs@126.com"
    smtp_url = "smtp.qq.com"

    msg = MIMEText(text,"plain",'utf-8')
    msg['From'] = _format_addr('news <%s>' %user_mail)
    msg['To'] = _format_addr('yuy <%s>' % send_mail)
    msg['Subject'] = Header('新闻提醒','utf-8').encode()

    server = smtplib.SMTP(smtp_url,25)
    server.set_debuglevel(1)
    server.starttls()
    server.login(user_mail,passwd)
    server.sendmail(user_mail,[send_mail],msg.as_string())
    server.quit()

def main():
    # @邮件开始打印信息
    print("@目前只支持用QQ邮箱发送@\n")

    #判断邮件格式是否正确，不正确则重新输入
    while True:
        user_mail,passwd,send_mail = get_user_info()
        if (user_mail != " " )& (send_mail != " "):
            break
        else:
            print("邮箱格式不正确，请重新输入！")

    #构造邮件正文
    start_text = "\n\r@***********活着就是填补世界的空白***************\n"
    text = start_text+"@@科技新闻\n\n"
    new_url = "http://tech.ifeng.com/listpage/6899/1/list.shtml"
    get_news = Get_url(new_url)
    fh_text = get_news.getFhUrlInfo()
    for f_text in fh_text:
        text += f_text + "\n"

    text = text + "\n@=============我是分割线===========\n\n" + "@@python 资讯\n\n"
    python_url = "http://www.pythontab.com/"
    get_python_url = Get_url(python_url)

    python_title_text = get_python_url.getPythonNew()
    for t_text in python_title_text:
        text += t_text + "\n"
    python_text = get_python_url.getBaseUrlInfo()
    for p_text in python_text:
        text += p_text + "\n"

    #@邮件末尾打印信息
    text_end1= "\n\r@***************mail end********************\n"
    text_end2 = "\n\r@***********生命不息，学习不止***************\n"

    send_text = text + text_end1 + text_end2

    #邮件正文构造完成，发送邮件，如果密码错误则重新运行
    try:
        sendmail(send_text,user_mail,passwd,send_mail)
    except:
        time.sleep(1)
        print("密码错误！请重新输入！")
        main()


if __name__ == '__main__':
    main()