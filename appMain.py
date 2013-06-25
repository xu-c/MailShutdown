# -*- coding: utf-8 -*-
# Author: xuc
# Mail: xu_c@live.cn


import poplib, os, time, sys
from email import parser, header
from select import select
from sys import stdout, stdin
from stdio import stdio

#连接参数
server = ''
user = ''
passwd = ''
sleepTime = 15

#首次连接到服务器
mailServer = poplib.POP3_SSL(server)
mailServer.user(user)
mailServer.pass_(passwd)

#记录现有邮件的标识
uids=[]
for uid in mailServer.uidl()[1]:
    uids.append(uid.split(' ', 2)[1])
mailServer.quit()
print u'%%已做好运行准备%%'

#开始循环检测新邮件
loopNum = 0
while True:
    loopNum += 1
    time.sleep(sleepTime - 2)
    print '\n'
    print 10*'*' + u'第'+str(loopNum) + u'次运行' + 10 * '*'
    print u'正在检测新邮件……'
    
    #连接到服务器
    mailServer = poplib.POP3_SSL(server)
    mailServer.user(user)
    mailServer.pass_(passwd)
    (mailCount, size) = mailServer.stat()

    #获取最新邮件的标识
    latestUid = mailServer.uidl(mailCount).split(' ', 3)[2]
    
    #如果是新邮件
    if latestUid not in uids:

        print u'检测到新邮件'
        uids.append(latestUid)

        #读取邮件标题
        message = parser.Parser().parsestr('\n'.join(mailServer.retr(mailCount)[1]))
        subject = header.decode_header(message['Subject'])
        cmd = unicode(subject[0][0], subject[0][1])

        #执行命令
        if cmd == 'Shutdown':
            print u'即将关机！'
            os.system('shutdown -s -t 60')
        if cmd == 'Cancel':
            print u'取消关机！'
            os.system('shutdown -a')
            
    else:
        print u'未检测到新邮件'
    mailServer.quit()

    #询问是否退出
    print u'2秒内按回车退出……'
    r, w , x = select([stdio.STDIN_FILENO], [], [], 2)
    if r:
        print u'即将退出程序'
        sys.exit()