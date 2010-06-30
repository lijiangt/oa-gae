# -*- coding: utf-8 -*-
import sys
import os
import logging as logger
import datetime
import getopt
import getpass
import atom
import gdata.contacts
import gdata.contacts.service

import csv

from zhutils import pinyin

logger.basicConfig(level=logger.INFO)

# see: http://code.google.com/apis/contacts/developers_guide_python.html
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

class ContactConstant():
    TYPE_REL_PREFIX = 'http://schemas.google.com/g/2005'
    
    
    MOBILE_PHONE_REL_SUFFIX = '#mobile'
    HOME_PHONE_REL_SUFFIX = '#home'
    WORK_PHONE_REL_SUFFIX = '#work'
    PAGER_PHONE_REL_SUFFIX = '#pager'
    OTHER_PHONE_REL_SUFFIX = '#other'
    HOME_FAX_REL_SUFFIX = '#home_fax'
    WORK_FAX_REL_SUFFIX = '#work_fax'
    
    CHANGE_LOG_TITLE = '电话号码变更记录：'
    BEFORE_CHANGE_LOG_TITLE_SEPARATOR = '\n\n\n\n\n'
    CHANGE_LOG_SEPARATOR = '\n'
    
def __add_change_log(contact,num,add=False):
    if not contact.content or not contact.content.text:
        contact.content = atom.Content(text=ContactConstant.BEFORE_CHANGE_LOG_TITLE_SEPARATOR + ContactConstant.CHANGE_LOG_TITLE+ContactConstant.CHANGE_LOG_SEPARATOR)
    if contact.content.text.find(ContactConstant.CHANGE_LOG_TITLE) == -1:
        contact.content.text  = contact.content.text + ContactConstant.BEFORE_CHANGE_LOG_TITLE_SEPARATOR + ContactConstant.CHANGE_LOG_TITLE + ContactConstant.CHANGE_LOG_SEPARATOR
    action = '删除'
    if add:
        action = '添加'
    contact.content.text  = contact.content.text + '%s：%s电话号码:%s。%s'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),action,num,ContactConstant.CHANGE_LOG_SEPARATOR)

def __get_phone_num(contact,rel_suffix):
    num = []
    if not contact.phone_number:
        return num
    for phone_number in contact.phone_number:
        if phone_number.rel and phone_number.rel.endswith(rel_suffix):
            num.append(phone_number.text.strip())
    return num

def __add_phone_num(contact,rel,num):
    if not contact.phone_number:
        contact.phone_number = []
    contact.phone_number.append(gdata.contacts.PhoneNumber(rel=rel,text=num))
    __add_change_log(contact,num,True)
    
def __del_phone_num(contact,rel_suffix,num):
    for phone_number in contact.phone_number:
        if (phone_number.rel and phone_number.rel.endswith(rel_suffix)) and num==phone_number.text.strip():
            contact.phone_number.remove(phone_number)
            __add_change_log(contact,num)

def get_other_phone_num(contact):
    num = []
    if not contact.phone_number:
        return num
    for phone_number in contact.phone_number:
        type_label = phone_number.label
        if not type_label and phone_number.rel and phone_number.rel.endswith(ContactConstant.OTHER_PHONE_REL_SUFFIX):
            num.append(phone_number.text.strip())
    return num

def add_other_phone_num(contact,num):
     __add_phone_num(contact,ContactConstant.TYPE_REL_PREFIX+ContactConstant.OTHER_PHONE_REL_SUFFIX,num)
     __add_change_log(contact,num,True)

def del_other_phone_num(contact,num):
    for phone_number in contact.phone_number:
        label = phone_number.extension_attributes.get('label',None)
        if (not label or (phone_number.rel and phone_number.rel.endswith(ContactConstant.OTHER_PHONE_REL_SUFFIX))) and num==phone_number.text.strip():
            contact.phone_number.remove(phone_number)
            __add_change_log(contact,num)


inited = False
gd_client = None
read_only = True
limit_delete = True #限制删除，仅进行更新和添加
phone_type_code = 1 # 1:Nokia 1600，2:K-Touch A905

contacts = []
all_type = {'M':{'get_fun':lambda contact:__get_phone_num(contact,  ContactConstant.MOBILE_PHONE_REL_SUFFIX) ,
                'del_fun': lambda contact,num:__del_phone_num(contact, ContactConstant.MOBILE_PHONE_REL_SUFFIX,num) ,
                'add_fun': lambda contact,num:__add_phone_num(contact,ContactConstant.TYPE_REL_PREFIX+ContactConstant.MOBILE_PHONE_REL_SUFFIX,num) ,
                'add_info': '将在%s下添加手机号码%s',
                'not_del_info': '未在%s下删除手机号码%s',
                'del_info': '将在%s下删除手机号码%s',},
            'H':{'get_fun':lambda contact: __get_phone_num(contact,ContactConstant.HOME_PHONE_REL_SUFFIX) ,
                'del_fun': lambda contact,num:__del_phone_num(contact,ContactConstant.HOME_PHONE_REL_SUFFIX,num) ,
                'add_fun': lambda contact,num:__add_phone_num(contact,ContactConstant.TYPE_REL_PREFIX+ContactConstant.HOME_PHONE_REL_SUFFIX,num) ,
                'add_info': '将在%s下添加住宅电话号码%s',
                'not_del_info': '未在%s下删除住宅电话号码%s',
                'del_info': '将在%s下删除住宅电话号码%s',},
            'O':{'get_fun': lambda contact:__get_phone_num(contact,ContactConstant.WORK_PHONE_REL_SUFFIX),
                'del_fun': lambda contact,num:__del_phone_num(contact,ContactConstant.WORK_PHONE_REL_SUFFIX,num),
                'add_fun': lambda contact,num:__add_phone_num(contact,ContactConstant.TYPE_REL_PREFIX+ContactConstant.WORK_PHONE_REL_SUFFIX,num) ,
                'add_info': '将在%s下添加工作电话号码%s',
                'not_del_info': '未在%s下删除工作电话号码%s',
                'del_info': '将在%s下删除工作电话号码%s',},
            'P':{'get_fun': lambda contact: __get_phone_num(contact,ContactConstant.PAGER_PHONE_REL_SUFFIX),
                'del_fun': lambda contact,num:__del_phone_num(contact,ContactConstant.PAGER_PHONE_REL_SUFFIX,num),
                'add_fun': lambda contact,num:__add_phone_num(contact,ContactConstant.TYPE_REL_PREFIX+ContactConstant.PAGER_PHONE_REL_SUFFIX,num),
                'add_info': '将在%s下添加寻呼机/小灵通号码%s',
                'not_del_info': '未在%s下删除寻呼机/小灵通号码%s',
                'del_info': '将在%s下删除寻呼机/小灵通号码%s',},
            'U':{'get_fun': get_other_phone_num,
                'del_fun': del_other_phone_num,
                'add_fun': add_other_phone_num,
                'add_info': '将在%s下添加其它电话号码%s',
                'not_del_info': '未在%s下删除其它电话号码%s',
                'del_info': '将在%s下删除其它电话号码%s',},
            'WF':{'get_fun': lambda contact:__get_phone_num(contact,ContactConstant.WORK_FAX_REL_SUFFIX),
                'del_fun': lambda contact,num:__del_phone_num(contact,ContactConstant.WORK_FAX_REL_SUFFIX,num),
                'add_fun': lambda contact,num:__add_phone_num(contact,ContactConstant.TYPE_REL_PREFIX+ContactConstant.WORK_FAX_REL_SUFFIX,num),
                'add_info': '将在%s下添加住宅传真号码%s',
                'not_del_info': '未在%s下删除住宅传真号码%s',
                'del_info': '将在%s下删除住宅传真号码%s',},
            'HF':{'get_fun': lambda contact:__get_phone_num(contact,ContactConstant.HOME_FAX_REL_SUFFIX),
                'del_fun': lambda contact,num:__del_phone_num(contact,ContactConstant.HOME_FAX_REL_SUFFIX,num),
                'add_fun': lambda contact,num:__add_phone_num(contact,ContactConstant.TYPE_REL_PREFIX+ContactConstant.HOME_FAX_REL_SUFFIX,num),
                'add_info': '将在%s下添加工作传真号码%s',
                'not_del_info': '未在%s下删除工作传真号码%s',
                'del_info': '将在%s下删除工作传真号码%s',},
            }

def get_contact_company(contact):
    if contact and contact.organization and contact.organization.org_name:
        return contact.organization.org_name.text
    else:
        return None

def get_contact_email(contact):
    email = []
    if contact and contact.email:
        for e in contact.email:
            email.append(e.address)
    return email 

def get_chinese_name(contact):
    if not contact or not contact.title:
        return None
    name = contact.title.text
    if not name:
        return None
    index = 0
    for char in name:
        if(char.isalnum() or char == ' '):
            index +=1
    return name[index:]

def get_all_contacts():
    global inited,contacts,gd_client,read_only,limit_delete
    # TODO: 首选使用AuthSub proxy authentication
    gd_client = gdata.contacts.service.ContactsService()
    gd_client.email = raw_input('请输入Gmail邮箱：').strip()
#    gd_client.password = raw_input('请输入%s的密码：'%gd_client.email).strip()
    if os.isatty(sys.stdin.fileno()):
        gd_client.password = getpass.getpass(prompt='请输入%s的密码：'%gd_client.email).strip()
    else:
#        print '请输入%s的密码：'%gd_client.email
#        gd_client.password = sys.stdin.readline().rstrip()
        gd_client.password = raw_input('请输入%s的密码：'%gd_client.email).strip()
#    gd_client.source = 'exampleCo-exampleApp-1'
    gd_client.ProgrammaticLogin()
    query = gdata.contacts.service.ContactsQuery()
#    query.orderby = 'title'
#    query['sortorder'] = 'ascending'
    query.max_results=10000
#    feed = gd_client.GetContactsFeed()
    feed = gd_client.GetContactsFeed(query.ToUri())
    for i, entry in enumerate(feed.entry):
        contacts.append(entry)
    inited = True

def search_contact(real_name):
    if not inited:
        get_all_contacts()
    english_name = pinyin.hanzi2pinyin(real_name).capitalize()
    contact_name = '%s%s'%(english_name,real_name)
    result = []
    for c in contacts:
        if c.title.text == contact_name:
            result.append(c)
    if result:
        return result
    for c in contacts:
        if  c.title and c.title.text and c.title.text.find(real_name)!=-1:
            result.append(c)
    if result:
        return result
    for c in contacts:
        if c.title and c.title.text and c.title.text.find(english_name)!=-1:
            result.append(c)
    return result

def __process_number(records,type,real_name,number):
    record = records.get(real_name,None)
    if record and record.has_key(type):
        record[type].append(number)
    elif record:
        record[type] = [number]
    else:
        records[real_name] = {}
        records[real_name][type] = [number]

def read_all_phone_num_from_csv_of_NOKIA1600():
    reader = unicode_csv_reader(open("../../csv/contacts.csv", "rb"))
    records = {}
    for i,row in enumerate(reader):
        i += 1
        if i == 1 or i==2:
            continue
        name = row[2].strip()
        number = row[3].strip()
        real_name = name
        if name.startswith('L') or name.startswith('J'):
            continue #TODO: 处理L和J开头的记录
        processed = False
        for type in all_type.keys():
            if name.endswith(type):
                real_name = name[:(0-len(type))]
                __process_number(records,type,real_name,number)
                processed = True
            if name.endswith(tuple([type+str(i) for i in range(0,10)])):
                real_name = name[:(0-len(type)-1)]
                __process_number(records,type,real_name,number)
                processed = True
        if not processed:
            logger.error('不能识别的姓名格式：%s。'%name)
    return records

def read_all_phone_num_from_csv_of_KTouchA905():
    reader = unicode_csv_reader(open("../../csv/contacts.csv", "rb"))
    records = {}
    for i,row in enumerate(reader):
        i += 1
        if i == 1:
            continue
        real_name = row[0].strip();
        records[real_name] = {}#﻿Name,Mobile,Home,Company name,Email,Office,Fax,Birthdya
        if row[1].strip():
            records[real_name]['M'] = [row[1].strip()]
        if row[2].strip():
            records[real_name]['H'] = [row[2].strip()]
        if row[5].strip():
            records[real_name]['O'] = [row[5].strip()]
        if row[4].strip():
            records[real_name]['EMAIL'] = [row[4].strip()]
        if row[6].strip():
            records[real_name]['WF'] = [row[6].strip()]
#        if row[7].strip():
#            records[real_name]['BIRTHDAY'] = [row[7].strip()]
    return records
    
def sync_contacts_to_gmail():
    global limit_delete
    read_only_str = raw_input('要进行数据更新吗？如果输入Y/y将更新Gmail通讯录，如果输入其它字符则只进行数据的对比，并不更新！默认值为N:').strip()
    read_only = True;
    if read_only_str and (read_only_str == 'Y' or read_only_str == 'y'):
        read_only = False
    if not read_only:
        limit_delete_str = raw_input('是否不限制删除，仅进行更新和添加，不限制请输入Y/y,限制请输入其它字符！默认值为N').strip()
        if limit_delete_str and (limit_delete_str == 'Y' or limit_delete_str == 'y'):
            limit_delete = False
    if read_only:
        logger.info('将只进行数据的对比！')
    elif limit_delete:
        logger.info('将以限制删除模式更新Gmail通讯录！')
    else:
        logger.info('将以非限制删除模式更新Gmail通讯录！')
    all_phone_nums = {}
    if(phone_type_code==1):
        all_phone_nums = read_all_phone_num_from_csv_of_NOKIA1600();
    elif(phone_type_code==2):
        all_phone_nums = read_all_phone_num_from_csv_of_KTouchA905();
    else:
        logger.warn("不支持其它类型的手机型号！");
        return;
    for name,record in all_phone_nums.items():
        result = search_contact(name)
        if result:
            if len(result)!=1:
                logger.warn('Gmail联系人中找到%s个姓名为%s的记录！将根据电话号码进行分辨！'%(len(result),name))
                new_result = []
                for type in all_type.keys():
                    value = all_type[type]
                    if record.has_key(type):
                        number = record[type]
                        for contact in result:
                            gdata_num = value['get_fun'](contact)
                            for num in gdata_num:
                                if num in number and  not contact in new_result:
                                    new_result.append(contact)
                if len(new_result)==1:
                    logger.warn('根据电话号码分辨了%s，其号码信息为%s'%(name,str(record)))
                    result = new_result
                else:
                    logger.error('不能根据电话号码分辨%s，将忽略该记录，请手工同步，其号码信息为%s'%(name,str(record)))
                    continue
            contact = result[0]
            changed = False
            for type in all_type.keys():
                value = all_type[type]
                number = []
                if record.has_key(type):
                    number = record[type]
                gdata_num = value['get_fun'](contact)
                will_add = False
                for num in number:
                    if num in gdata_num:
                        continue
                    else:
                        logger.info(value['add_info']%(name,num))
                        value['add_fun'](contact,num)
                        changed = True
                        will_add = True
                for num in gdata_num:
                    if num in number:
                        continue
                    else:
                        if read_only or not limit_delete or will_add:
                            logger.info(value['del_info']%(name,num))
                            value['del_fun'](contact,num)
                            changed = True
                        elif limit_delete:
                            logger.warn(value['not_del_info']%(name,num))
            if changed and not read_only:
                try:
                    gd_client.UpdateContact(contact.GetEditLink().href, contact)
                except BaseException,e:
                    logger.error('更新%s:%s时出错，请手工更新！错误信息为: %s'%(name,record,e.message))
        else:
            logger.info('即将添加 %s:%s！'%(name,str(record)))  
            contact = gdata.contacts.ContactEntry(
              title=atom.Title(text='%s%s'%(pinyin.hanzi2pinyin(name).capitalize(),name)))
            for type in all_type.keys():
                value = all_type[type]
                if record.has_key(type):
                    number = record[type]
                    for num in number:
                        logger.info(value['add_info']%(name,num))
                        value['add_fun'](contact,num)
            if not read_only:
                try:
                    contact_entry = gd_client.CreateContact(contact) 
                except BaseException,e:
                    logger.error('添加%s:%s时出错，请手工添加！错误信息为: %s'%(name,record,e.message))
    logger.info('操作完成！')
    

def __select_main_item(name,l,item_name):
    if not l:
        return ''
    elif len(l)==1:
        return l[0]
    else:
        return l[0]  # FIXME: 
        alert_text = ''
        i = 0
        for item in l:
            i +=1
            alert_text += '%s:%s\n'%(item,i)
        while(True):
            choice = raw_input('%s有多个%s，请选取一个%s：\n%s'%(name,item_name,item_name,alert_text)).strip()
            try:
                if int(choice)-1 in range(i):
                    return l[int(choice)-1]
            except ValueError:
                continue;

def sync_contacts_from_gmail_to_KTouchA905():
    if not inited:
        get_all_contacts()
    contact_file = file("../../csv/new_contacts.csv", 'w')
    contact_file.write('Name    Mobile    Home    Company    Email    Office    Fax    Birthday\n')
    for contact in contacts:
        name = get_chinese_name(contact)
        if not name:
            continue
        m = __select_main_item(name,all_type['M']['get_fun'](contact),'手机号码');
        if not m:
            m = __select_main_item(name,all_type['P']['get_fun'](contact),'寻呼机/小灵通号码');
        h = __select_main_item(name,all_type['H']['get_fun'](contact),'住宅电话号码');
        company = get_contact_company(contact)
        if not company:
            company = ''
        email = __select_main_item(name,get_contact_email(contact),'电子邮箱');
        w = __select_main_item(name,all_type['O']['get_fun'](contact),'工作电话号码');
        f = __select_main_item(name,all_type['WF']['get_fun'](contact),'工作传真号码');
        contact_file.write('"%s"    "%s"    "%s"    "%s"    "%s"    "%s"    "%s"    ""\n'%(name,m,h,company,email,w,f))
    contact_file.close()
    logger.info('操作完成！')
    # TODO: 读取小灵通号码

def main():
    global phone_type_code
    while(True):
        phone_type = raw_input('请输入操作针对的手机型号：\nNokia 1600请输入1\nK-Touch A905请输入2\n').strip()
        if(phone_type=='1'):
            phone_type_code = 1;
            break;
        elif(phone_type=='2'):
            phone_type_code = 2;
            break;
        else:
            logger.warn("不支持其它类型的手机型号！");
            return;
    action = raw_input('同步通讯簿到Gmail中请输入Y/y,若从Gmail中下载通讯簿保存为特定手机支持的文件请直接按回车键！').strip()
    if('y' == action or 'Y' == action):
        sync_contacts_to_gmail()
    else:
        if(phone_type_code==1):
            logger.warn("暂不支持从Gmail中下载通讯簿保存为Nokia 1600所支持的文件格式！");
            return
        elif(phone_type_code==2):
            sync_contacts_from_gmail_to_KTouchA905()
        else:
            logger.warn("不支持其它类型的手机型号！");
            return;
    
def migration():
    if not inited:
        get_all_contacts()
    for contact in contacts:
        changed = False
        if contact.email:
            for email in contact.email:
                label = email.label
                rel = email.rel
                address = email.address.strip()
                if (label and label.strip() == u'个人信息') or (not label and rel and rel.endswith('#other')):
                    contact.email.remove(email)
                    contact.email.append(gdata.contacts.Email(rel='http://schemas.google.com/g/2005#home',address=address))
                    changed = True
                    logger.info('name: %s    label: %s    rel: %s    address: %s'%(contact.title.text,label,rel,address));
                elif label:
                    logger.info('name: %s    label: %s    rel: %s    address: %s'%(contact.title.text,label,rel,address));
        if contact.phone_number:
            for phone_number in contact.phone_number:
                label = phone_number.label
                rel = phone_number.rel
                num = phone_number.text.strip()
                if not label and rel.endswith('#pager'):
                    logger.info('name: %s    label: %s    rel: %s    num: %s'%(contact.title.text,label,rel,phone_number.text.strip()));
                if label:
                    if label.strip() == u'个人信息 / Mobile':
                        __del_phone_num(contact,(label,),"#other",num)
                        __add_phone_num(contact,'http://schemas.google.com/g/2005#mobile',num)
                        changed = True
                        logger.info('name: %s    label: %s    rel: %s    num: %s'%(contact.title.text,label,rel,phone_number.text.strip()));
                    elif label.strip() == u'个人信息':
                        __del_phone_num(contact,(label,),"#other",num)
                        __add_phone_num(contact,'http://schemas.google.com/g/2005#home',num)
                        changed = True
                        logger.info('name: %s    label: %s    rel: %s    num: %s'%(contact.title.text,label,rel,phone_number.text.strip()));
                    else:
                        logger.info('name: %s    label: %s    rel: %s    num: %s'%(contact.title.text,label,rel,phone_number.text.strip()));
#        if changed:
#            try:
#                gd_client.UpdateContact(contact.GetEditLink().href, contact)
#            except BaseException,e:
#                logger.error('更新%s时出错，请手工更新！错误信息为: %s'%(contact.title.text,e.message))                

def check_contact_name():
    if not inited:
        get_all_contacts()
    for contact in contacts:
        if not contact or not contact.title:
            return
        name = contact.title.text
        if not name:
            return 
        index = 0
        for char in name:
            if(char.isalnum() or char == ' ' or char == '@'):
                index +=1
#        logger.info('index: %s len: %s'%(index,len(name)))
        if index == len(name):
            logger.info(name);

if __name__ == '__main__':
    main()
#    migration()
#    check_contact_name();
# test commit2
