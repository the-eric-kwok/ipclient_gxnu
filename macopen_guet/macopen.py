#!/usr/bin/env python
# coding=utf-8 ##
################This is MAC OPEN TOOLS  Version 1.0###################
################Only for GUET###########################
import socket
import uuid

server='172.16.1.1'  #GUET 172.16.1.1  GXNU 202.193.160.123
addr=(server,20015)

def get_ip():
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def get_mac():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ':'.join([mac[e:e+2] for e in range(0,11,2)])

def int_overflow(val):
    maxint = 2147483647
    if not -maxint-1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val

def send_handshake(mac,ip,isp):
 localInfo=bytearray([0x00,0x00,0x00,0x00,0x00,0x00,
                         0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                         0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                         0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                         0xac,0x10,0x40,0x12,0x30,0x30,0x3a,0x31,
                         0x46,0x3a,0x31,0x36,0x3a,0x32,0x32,0x3a,
                         0x42,0x38,0x3a,0x45,0x43,0x00,0x00,0x00,
                         0x03,0x00,0x00,0x00,0x00,0x00])
 s1=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
 s1.connect(addr)
 ispKey=0x4e67c6a7
 localInfo[0]=0x61
 nmac=len(mac)
 nInfo=len(localInfo)
 ipaddress=[0,0,0,0]
 fff=ip.split('.')
 for k in range(0,4):
   ipaddress[k]=int(fff[k])
 print(ipaddress)
 for i in range(0,4):
  localInfo[i+30]=ipaddress[i]
 print(nInfo)
 for i in range(0,nmac):
  localInfo[i+34]=ord(mac[i])
 localInfo[54]=isp
#----------------
 ESI=int(0)
 EBX=int(0)
 ECX=int(0)
 ESI2=int(0)
 ECX=int(ispKey)
 for i in range(0,nInfo-4):
    ESI=ECX
    ESI=int_overflow(ECX<<5)
    if (ECX>0):
      EBX=ECX
      EBX=ECX>>2
    else:
      EBX=ECX
      EBX=ECX>>2
      EBX=EBX|(0xC0000000)
    ESI=ESI+int(localInfo[i])
    EBX=int_overflow(EBX+ESI)
    ECX=ECX^EBX
 ECX=ECX&(0x7FFFFFFF)

 for i in range(0,4):
  keypart=((ECX>>(i*8))&0x000000FF)
  localInfo[nInfo-(4-i)]=keypart
 s1.send(localInfo)

if __name__=="__main__":
    #mac="98:e7:f4:53:d9:08"
    mac = get_mac()
    #ip="10.21.123.64" ##!!!!ip is local machine's ip address but not router's ip
    try:
        ip = get_ip()
    except OSError as e:
        print('无网络连接，请检查您的网线是否插好')
        exit(1)
    isp = 0x02
    ###isp  0x01(China Unicom)  0x02(China Telecom)  0x03(China Mobile) ###
    send_handshake(mac,ip,isp)
    exit

