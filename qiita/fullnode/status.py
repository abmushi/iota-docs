import urllib2
import json

cmd1 = 'getNodeInfo'
cmd2 = 'getNeighbors'

command1 = {
        'command': cmd1
}

command2 = {
    'command': cmd2
}

stringified1 = json.dumps(command1)
stringified2 = json.dumps(command2)

headers = {
    'content-type': 'application/json',
}
local_url ="http://localhost:14600"

request1 = urllib2.Request(url=local_url, data=stringified1, headers=headers)
request2 = urllib2.Request(url=local_url, data=stringified2, headers=headers)

returnData1 = urllib2.urlopen(request1).read()
jsonData1 = json.loads(returnData1)

returnData2 = urllib2.urlopen(request2).read()
jsonData2 = json.loads(returnData2)

print '\n- IRI - "'+cmd1+'" - - - - - - - - - - - - - - - - - - - - - - - - - -'
for key1,val1 in jsonData1.items():
        print str(key1)+'       : '+str(val1)
print '\n- IRI - "'+cmd2+'" - - - - - - - - - - - - - - - - - - - - - - - - - -'
for key1,val1 in jsonData2.items():
        if key1 == 'neighbors':
                for each in val1:
                        print '- - - - - '+each['address']+' - - - - -'
                        for k,v in each.items():
                                if k != 'address':
                                        print str(k)+' :                '+str(v)
        else:
                print str(key1)+'       : '+str(val1)


