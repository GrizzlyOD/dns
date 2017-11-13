import pickle
import os
import threading
A=[]
d_web_ip = {}
d_ip_web = {}

update_dic = {}

data = open('dnsrelay.txt')
i=0
for each_line in data:
    try:
        (ip,sitecopy) = each_line.split(' ',1)
        (site,nothing) = sitecopy.split('\n',1)
        d_web_ip[site] = ip
        d_ip_web[ip] = site
    except:
        print('file error')
data.close()
try:
    with open('newdnsrelay.pickle','wb')as newdnsrelay_file:
        pickle.dump(d_web_ip,newdnsrelay_file)
except IOError as err:
    print ('File error:'+str(err))
except pickle.PickleError as perr:
    print ('Pickling error:'+str(perr))

def get_web_ip():
    with open('newdnsrelay.pickle','rb') as f:
        global update_dic
        update_dic = pickle.load(f)
        return update_dic.copy()
    return(None)

def storeForUpdate(web_site, add = None):
    global update_dic
    if(update_dic.get(web_site) != None):
        add_frequen = update_dic[web_site]
        add_frequen[1] = add_frequen[1] + 1
        print (web_site+' frequence incrase 1,with ip '+add_frequen[0])
        return add_frequen[1]
    else:
        update_dic[web_site] = [add,1]
        print ('record for a new site')
        return 1
def updateCache():
    global update_dic
    m = update_dic.copy()
    t = threading.Thread(target=my_thread,kwargs=m)
    print ('ready to update local cache')
    t.start()
    t.join()

def my_thread(*argu,**arg):
    frequence = []
    remain_dic = {}
    for each_key in arg:
        tmp = arg[each_key]
        if(tmp[1] not in frequence):
            frequence.append(tmp[1])
        if(tmp[0] == '0.0.0.0'):
            remain_dic[each_key] = '0.0.0.0'

    print ('various frequence:')
    for each in frequence:
        print ('have '+ str(each))
    for each_key in remain_dic:
        arg.pop(each_key)#enimilate ban
    i = 0
    while(i < 30):
        max_frequence = max(frequence)
        for each_key in arg:
            tmp = arg[each_key]
            if(tmp[1] == max_frequence):
                remain_dic[each_key] = tmp[0]
                i = i + 1
            if(i == 30):
                break
            frequence.remove(max_frequence)
            if(not frequence):###no more
                break

    updateFile(remain_dic)

def updateFile(new_dic):
    f = open('dnsrelaycopy.txt','w')
    for each_key in new_dic:
        word = str(new_dic[each_key]) + ' ' + str(each_key)
        f.write(word)
        f.write('\n')
        new_dic[each_key] = [new_dic[each_key],0]
    try:
        with open('newdnsrelay.pickle','wb') as newdnsrelay_file:
            pickle.dump(new_dic,newdnsrelay_file)
    except IOError as err:
        print ('File error:'+str(err))
    except pickle.PickleError as perr:
        print ('Pickling error:'+str(perr))