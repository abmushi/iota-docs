# -*- coding: utf-8 -*-
import urllib2
import json

#今回はgetNodeInfoをリクエストする。
cmd = 'getNodeInfo'

command = {
    'command': cmd
}

stringified = json.dumps(command)

headers = {
    'content-type': 'application/json',
    'X-IOTA-API-Version': '1.4.1.2'
}

#あなたのフルノードのIPアドレス
node_url = "http://YOUR.IP.ADD.RESS:14265"

request = urllib2.Request(url=node_url, data=stringified, headers=headers)

#先ほどiri.iniに加えたユーザー名とパスワード
username = 'user'
password = 'password'

p = urllib2.HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, node_url, username, password)

handler = urllib2.HTTPBasicAuthHandler(p)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

returnData = urllib2.urlopen(request).read()

jsonData = json.loads(returnData)
print jsonData