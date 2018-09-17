#!/usr/bin/env python3
# coding=utf-8 ##
# This is MAC OPEN TOOLS  Version 1.0
# Only for GUET

import socket

server = '172.16.1.1'  # GUET 172.16.1.1  GXNU 202.193.160.123
addr = (server, 20015)


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def int_overflow(val):
    maxint = 2147483647
    if not -maxint - 1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val


def send_handshake(mac, ip, isp):
    localInfo = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                           0xac, 0x10, 0x40, 0x12, 0x30, 0x30, 0x3a, 0x31,
                           0x46, 0x3a, 0x31, 0x36, 0x3a, 0x32, 0x32, 0x3a,
                           0x42, 0x38, 0x3a, 0x45, 0x43, 0x00, 0x00, 0x00,
                           0x03, 0x00, 0x00, 0x00, 0x00, 0x00])
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1.connect(addr)
    ispKey = 0x4e67c6a7
    localInfo[0] = 0x61
    nmac = len(mac)
    nInfo = len(localInfo)
    ipaddress = [0, 0, 0, 0]
    fff = ip.split('.')
    for k in range(0, 4):
        ipaddress[k] = int(fff[k])
    for i in range(0, 4):
        localInfo[i + 30] = ipaddress[i]
    print('Package Length:', nInfo)
    for i in range(0, nmac):
        localInfo[i + 34] = ord(mac[i])
    localInfo[54] = isp

    # Generate check code
    ESI = int(0)
    EBX = int(0)
    ECX = int(0)
    ESI2 = int(0)
    ECX = int(ispKey)
    for i in range(0, nInfo - 4):
        ESI = ECX
        ESI = int_overflow(ECX << 5)
        if (ECX > 0):
            EBX = ECX
            EBX = ECX >> 2
        else:
            EBX = ECX
            EBX = ECX >> 2
            EBX = EBX | (0xC0000000)
        ESI = ESI + int(localInfo[i])
        EBX = int_overflow(EBX + ESI)
        ECX = ECX ^ EBX
    ECX = ECX & (0x7FFFFFFF)

    for i in range(0, 4):
        keypart = ((ECX >> (i * 8)) & 0x000000FF)
        localInfo[nInfo - (4 - i)] = keypart

    for i in localInfo:
        print(hex(i), end=' ')
    print('')
    s1.send(localInfo)  # Send it!


def main(mac, isp):
    print('MAC Address:', mac)
    try:
        ip = get_ip()
    except OSError as e:
        print('无网络连接，请检查您的网线是否插好')
        print('若确认网线插好了还是无法连接，你可以尝试手动填写ip地址')
        exit(1)
    ## 若自动获取ip地址失败则修改下一行
    # ip = 10.10.10.10
    print('IP Address:', ip)
    print('ISP:', isp)
    send_handshake(mac, ip, isp)
    print('OK!')


if __name__ == "__main__":
    mac = "98:e7:f4:53:d9:08"
    # isp  0x01(China Unicom)  0x02(China Telecom)  0x03(China Mobile)
    isp = 0x02
    main(mac, isp)
    exit
