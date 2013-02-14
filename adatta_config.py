#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 
# (c) Roberto Gambuzzi
# Creato:          14/02/2013 11:20:46
# Ultima Modifica: 14/02/2013 17:27:45
# 
# v 0.0.1.0
# 
# file: C:\Progetti\php4win_script\adatta_config.py
# auth: Roberto Gambuzzi <gambuzzi@gmail.com>
# desc: 
# 
# $Id: adatta_config.py 14/02/2013 17:27:45 Roberto $
# --------------

import re
import os
import sys
import win32com.shell.shell as shell

ASADMIN = 'asadmin'
SMTP = 'out.alice.it'
PORT = '25'
MAIL = 'gbinside@gmail.com'

PHPPATH = 'c:\\Program Files\\php\\'
PHPPATHSL = PHPPATH.replace('\\','/')

APACHEPATH = "C:\\Program Files\\Apache Software Foundation\\Apache2.2"
APACHEPATHSL = APACHEPATH.replace('\\','/')

def sed(file_in, regex_match, substitute, inplace=True, file_out=None, flags = re.I):
   rec = re.compile(regex_match, flags=flags)
   stringa = open(file_in,'rb').read()
   stringa = rec.sub(substitute, stringa)
   open(file_in,'wb').write(stringa)

def main(argv):
    print "1"
    sed(PHPPATH+"php.ini", r'(display_errors\s*=\s*)Off', r'\1On')
    sed(PHPPATH+"php.ini", r'(SMTP\s*=\s*).*?\n', r'\1'+SMTP+r'\n')
    sed(PHPPATH+"php.ini", r'(smtp_port\s*=)\s*.*?\n', r'\1 '+PORT+r'\n')
    sed(PHPPATH+"php.ini", r';(sendmail_from\s*=\s*).*?\n', r'\1'+MAIL+r'\n')

    open(APACHEPATH+r"\conf\httpd.conf", "a").write('''\n\nScriptAlias /php/ "'''+PHPPATHSL+'''"
    AddType application/x-httpd-php .php
    AddType application/x-httpd-php .phtml
    Action application/x-httpd-php "/php/php-cgi.exe"\n\n''')

    find = r'(<Directory "'+re.escape(APACHEPATHSL)+r'/cgi-bin">.*?</Directory>)'
    append = r'''\1
<Directory "'''+PHPPATHSL+'''">
    AllowOverride None
    Options None
    Order allow,deny
    Allow from all
</Directory>'''
    sed(APACHEPATH+r"\conf\httpd.conf", find, append, flags = re.I|re.S)
    sed(APACHEPATH+r"\conf\httpd.conf", r"(DirectoryIndex index\.html)", r"\1 index.php")

if  __name__=="__main__":
    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        sys.exit(0)

    sys.exit(main(sys.argv))