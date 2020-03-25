import requests, sys, json
import hashlib   #md5

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/72.0.3626.121 Safari/537.36'
    }
url = 'http://10.161.92.193/cgi-bin/mgw.cgi'
def getsid():
    payload = {'m': '{"jsonrpc":"2.0","method":"GetSessionID","id":"1"}'}
    rsp = requests.get(url, params=payload, headers=headers)
    #print(r.request)
    rest = rsp.json()
    return rest['result']['sid']

#m: {"jsonrpc":"2.0","method":"Login","params":{"username":"user","password":"3fad88420a85798e4e41157311047fc0","sid":"4f046c3f-fee8-4f26-8557-a2b99c995604"},"id":"44"}
def mgw_login(sid, user, passwd):
    login_param = {
        "jsonrpc":"2.0",
        "method":"Login",
        "params":{"username":"user","password":"abc",
            "sid":"abc"
            },
        "id":"44"
    }
    #print("old tmp2: %s" % (login_param))
    login_param["params"]["username"] = user
    login_param["params"]["sid"] = sid
    #passwd = passwd  #"3fad88420a85798e4e41157311047fc0"
    login_param["params"]["password"]  = hashlib.md5(passwd.encode()).hexdigest()
    #print("new tmp2: %s" % (login_param))
    login_param_str = json.dumps(login_param)
    payload = {"m": login_param_str}
    #print(payload)
    #print(json.dumps(payload))
 
    r = requests.post(url, data=payload, headers=headers)
    
    return r.status_code
#m: {"jsonrpc":"2.0","method":"AddApp","params":{"apptype":"IPX 6 Relay","sid":"47ff2d19-883d-4b6a-8b19-3dcd9b1a41e4"},"id":"33"}
#{"jsonrpc":"2.0","result":{"appname":"IPX 6 RL_001","apptype":"IPX 6 Relay","iid":"1883685548"},"id":"33"}
def add_ipx6(sid):
    add_param = {
        "jsonrpc":"2.0",
        "method":"AddApp",
        "params":{"apptype":"IPX 6 Relay",
            "sid":"abc"
            },
        "id":"44"
    }
    #print("old tmp2: %s" % (login_param))
    add_param["params"]["sid"] = sid
    add_param_str = json.dumps(add_param)
    print(add_param_str)
    payload = {"m": add_param_str}
    
    rsp = requests.post(url, data=payload, headers=headers)
    
    r = rsp.json()
    return r['result']['iid']

#m: {"jsonrpc":"2.0","method":"CommissionDevices","params":{"apps":[{"iid":"433127183","name":{"pid":"AppName","val":"IPX 6 RL_002"},"port":{"pid":"Route","val":"1"},"address":{"pid":"DevAddr","val":"15"}}],"sid":"0b0d3b8e-e54a-4186-b711-e0e441475c3c"},"id":"74"}
#{"jsonrpc":"2.0","result":{"apps":[{"iid":"433127183"}]},"id":"74"}

#m: {"jsonrpc":"2.0","method":"RemoveApp","params":{"iid":"2659420626","sid":"47ff2d19-883d-4b6a-8b19-3dcd9b1a41e4"},"id":"63"}
#{{"jsonrpc":"2.0","result":{"iid":"2659420626"},"id":"63"}
def remove_ipx6(sid, iid):
    remove_param = {
        "jsonrpc":"2.0",
        "method":"RemoveApp",
        "params":{"iid":"123",
            "sid":"abc"
            },
        "id":"63"
    }
    #print("old tmp2: %s" % (login_param))
    remove_param["params"]["iid"] = iid
    remove_param["params"]["sid"] = sid
    remove_param_str = json.dumps(remove_param)
    print(remove_param_str)
    payload = {"m": remove_param_str}
    
    rsp = requests.post(url, data=payload, headers=headers)
    
    r = rsp.json()
    print(r)
    #return r['result']['iid']


if __name__ == "__main__":
    sid = getsid()
    user = input("Please enter your name:")
    passwd = input("Please enter your passwd:")
    if (mgw_login(sid, user, passwd) == 200):
        for cnt in range(100):
            print("====================> ipx cnt: %d" %(cnt))
            iid = add_ipx6(sid)
            print("next remove the ipx: %s" %(iid))
            remove_ipx6(sid, iid)


