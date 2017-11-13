import socket
def make(re_ip,msg):
    tmp_list = []
    for ch in msg:
        tmp_list.append(ch)
        tmp_list[4:12] = ['\x00','\x01','\x00','\x01','\x00','\x00','\x00','\x00']
        tmp_list = tmp_list+['\xc0','\x0c','\x00','\x01','\x00\ ','\x01','\x00','\x00','\x02','\x58','\x00','\x04']
        dive_ip = socket.inet_aton(re_ip)
        ch_ip = []
        for each_ch in dive_ip:
            ch_ip.append(each_ch)
        tmp_list = tmp_list + ch_ip
        re_msg = ''.join(tmp_list)
        return re_msg