# -*- coding: utf-8 -*-

'''
同步google数据
'''

inited = False
email = None
password = None
def get_input_email_and_password():
    global inited,email,password
    email = raw_input('请输入Gmail邮箱：').strip()
    password = raw_input('请输入%s的密码：'%gd_client.email).strip()
    inited = True
    
def sync_bookmarks():
    global inited,email,password
    if not inited:
        get_input_email_and_password()
    pass

def sync_contacts():
    global inited,email,password
    if not inited:
        get_input_email_and_password()
    pass

def sync_reader_opml():
    global inited,email,password
    if not inited:
        get_input_email_and_password()
    pass

def sync_notebook_life():
    global inited,email,password
    if not inited:
        get_input_email_and_password()
    pass

def main():
    sync_contacts()
    sync_bookmarks()
    sync_reader_opml()
    sync_notebook_life()

if __name__ == '__main__':
    main()