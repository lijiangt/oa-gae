import datetime
import logging
def get_datetime_interval(year,month):
    start = datetime.datetime(year,month,1,0,0,0,0)
    if month==12:
        year +=1
        month = 1
    else:
        month +=1
    end = datetime.datetime(year,month,1,0,0,0,0)
    return (start,end)

def get_date_by_str(s,default_format='%Y-%m-%d %H:%M:%S'):
    format = (default_format,'%Y-%m-%d %H:%M:%S')
    for f in format:
        try:
            return datetime.datetime.strptime(s,f)
        except ValueError:
            continue
    if len(s)>8:
        try:
            return datetime.datetime.strptime(s[:-4],f)
        except ValueError:
            pass
        try:
            return datetime.datetime.strptime(s[:-7],f)
        except ValueError:
            pass
    logging.warn('get_date_by_str return None, s is %s, default_format is %s.'%(s,default_format))
    return None 
            
    