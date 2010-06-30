#!/usr/bin/python   
import sys, os   
  
# Add a custom Python path.   
#sys.path.insert(0, "/usr/local/bin/python")   
  
# Switch to the directory of your project. (Optional.)   
# os.chdir("/usr/htdocs/oa")   
  
# Set the DJANGO_SETTINGS_MODULE environment variable.   
os.environ['DJANGO_SETTINGS_MODULE'] = "oa.settings"  
  
from django.core.servers.fastcgi import runfastcgi   
runfastcgi(method="threaded", daemonize="false")  