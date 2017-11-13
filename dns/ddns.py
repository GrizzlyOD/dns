import socket
import mydic
import charhandle
import makeframe

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 53
the_dic = mydic.get_web_ip()
client_request = {}
client_request_index = {}
reverse_map = {}
key_record = 0
client_wait = []
s.bind(('',port))
time_rest = 0
request_general = ''
print ('running')
while True:
    try:
        msg,(client,port) = s.recvfrom(1024)
        # print(msg)
        # print(msg.decode('gbk'))
    except:
        print ('Time out! ')
        continue
    request = []
    request = list(msg)


    requre_web = charhandle.get_request(request[12:])
    website = ''.join(requre_web)
    print(website)
    if(port == 53):
        answer = []
        answer = list(msg)
        print("Type:Remote Response")
        print("remote answer is: ")
        print(msg[-4] + msg[-3] + msg[-2] + msg[-1])
        response_ip = msg[-4] + msg[-3] + msg[-2] + msg[-1]
        char_ip = socket.inet_ntoa(response_ip)
        print(website + ' has the ip : ' + char_ip)
        fre = mydic.storeForUpdate(website, char_ip)
        print('with the frequence of ' + str(fre))
        ###real_request = client_request[request[0]+request[1]]
        for each_client in client_wait:
            my_key = client_request[request[0] + request[1] + str(each_client)]
            if client_request_index.get(my_key) != None:
                s.sendto(msg, client_request_index[my_key])
                print("Response to ip and Client port:")
                print(client_request_index[my_key])
                break
    else:

        print("Type: Client Request")
        print("ip and port：")
        print(client, port)
        ### requre_web = charhandle.get_request(request[12:])
        ###  website = ''.join(requre_web)
        print("Request website:" + website)
        if (the_dic.get(website) != None):
            print("Found in local cache:")
            re_ip = the_dic.get(website)
            print(re_ip)
            fre = mydic.storeForUpdate(website)
            print(re_ip[0] + ' with frequence ' + str(fre))
            zhen = makeframe.make(re_ip[0], msg)
            s.sendto(zhen, (client, port))
        else:
            print("need to ask remote server")
            key_record = key_record + 1
            request_general = key_record
            client_request[str(request[0])+str(request[1]) + str(client)] = request_general
            client_request_index[request_general] = (client, port)
            if client not in client_wait:
                client_wait.append(client)
            # select authority DNS server as you wish
            s.sendto(msg, ('114.114.114.114', 53))
    time_rest = time_rest + 1
    try:
        if (time_rest == 50):
            print('pay attention')
            print('######################')
            mydic.updateCache()
            print('######################')
            the_dic = mydic.get_web_ip()
            time_rest = 0
    except:
        print('not valid frequence')
    print('--------------------')
s.close()