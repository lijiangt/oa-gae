# -*- coding: utf-8 -*-
import string, sys, os
import logging as logger

from chardet.universaldetector import UniversalDetector

#logger.basicConfig(level=logger.INFO)
logger.basicConfig(level=logger.ERROR)

def detect_file_encoding(filename):
    detector = UniversalDetector()
    f = file(filename, 'rb')
    for line in f:
        detector.feed(line)
        if detector.done: break
    detector.close()
    f.close()
    return detector.result

def get_file_encoding(filename):
    result = detect_file_encoding(filename)
    if result.has_key('encoding'):
        if 'gb2312' == result['encoding']:
            return 'gb18030'
        return result['encoding']
    else:
        return None;
    
def is_text_file(filename):
    f = open(filename)
    s = f.read(1024)
    f.close()
    if "\0" in s:
        return False
    if not s:  # Empty files are considered text
        return True
    result = os.popen('/usr/bin/file -b ' + filename).readlines();
    if len(result) == 1:
        out = result[0]
        if out:
            if out.startswith('HTML document text'):
                return True;
            if out.startswith('ISO-8859 text'):
                return True;
            if out.startswith('Unicode text'):
                return True;
            if out.startswith('ASCII'):
                return True;
            if out.startswith('UTF-8'):
                return True;
            if out.startswith('ISO-8859'):
                return True;
            if out.startswith('Non-ISO'):
                return True;
            if out.startswith('exported SGML document text'):
                return True;
            if out.startswith('MIME entity text'):
                return True;
            if out.startswith('Little-endian UTF-16 Unicode C program character data'):
                return True;
            if out.startswith('DOS executable (COM)'):
                return True;
            if out.startswith('XML'):
                return True;
            if out.startswith('PDF document'):
                return False;
            if out.startswith('PC bitmap data'):
                return False;
            if out.startswith('Audio file'):
                return False;
            if out.startswith('gzip compressed data'):
                return False;
            if out.startswith('RAR archive data'):
                return False;
            if out.startswith('MPEG ADTS'):
                return False;
            if out.startswith('Microsoft ASF'):
                return False;
            if out.startswith('Microsoft Office'):
                return False;
            if out.startswith('GIF image data'):
                return False;
            if out.startswith('JPEG image data'):
                return False;
            if out.startswith('PNG image data'):
                return False;
            if out.startswith('Macromedia Flash data'):
                return False;
            if out.startswith('Zip archive data'):
                return False;
            if out.startswith('MS Windows icon resource'):
                return False;
            if out.startswith('RIFF (little-endian) data, WAVE audio, MPEG Layer 3'):
                return False;
            if out.startswith('Minix filesystem (big endian)'):
                return False;
            if out.startswith('Perl5 module source text'):
                return False;
            if out.startswith('data'):
                return False;
            logger.error(' %s : %s ' % (out, filename));
            return False;
    logger.error(' %s 的文件类型（是否为二进制）判断失败！' % filename);
    return False
#    f = open(filename)
#    result = is_text(f.read(blocksize))
#    f.close()
#    return result

#text_characters = "".join(map(chr, range(32, 255)) + list("\n\r\t\b"))
#_null_trans = string.maketrans("", "")
#
#def is_text_file(filename, blocksize=1024):
#    f = open(filename)
#    result = is_text(f.read(blocksize))
#    f.close()
#    return result
#
#def is_text(s):
#    if "\0" in s:
#        return False
#   
#    if not s:  # Empty files are considered text
#        return True
#
#    # Get the non-text characters (maps a character to itself then
#    # use the 'remove' option to get rid of the text characters.)
#    t = s.translate(_null_trans, text_characters)
#
#    # If more than 30% non-text characters, then
#    # this is considered a binary file
#    if len(t) / len(s) > 0.30:
#        return False
#    return True

def convert(filename, out_enc="utf-8"):
    if is_text_file(filename):
        encoding = get_file_encoding(filename)
        if not encoding:
            logger.error(' %s 的编码获取失败，将不进行转换！' % filename);
            return False;
        elif out_enc.lower() == encoding.lower():
            logger.info(' %s 的原编码即为%s，将不进行转换！' % (filename, out_enc))
            return True;
        else:
            try:
                logger.info('convert ' + filename),
                f = open(filename)
                new_content = f.read().decode(encoding)
                new_content = new_content.encode(out_enc)
                f.close()
                f = open(filename, 'w') 
                f.write(new_content)
                f.close()
                logger.info('convert %s done' % filename)
                return True;
            except Exception, e:
                logger.error(' %s error: %s！'%(filename,e))
                return False;
    else:
        logger.info(' %s 是二进制文件，将不进行转换！' % filename);
        return True;

if __name__ == "__main__":
    convert('/home/lijt/tmp/content.20090108.SAKAI.GBK18030.bak/vol1/2008/347/04/1d505cb1-9023-49f7-be6f-fc384212e8fc');