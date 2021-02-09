import time
import socket
from struct import *
import datetime
import pcapy
import sys

def getInterface():
    ifs = pcapy.findalldevs()
    if len(ifs) == 0:
        print("you don't have enough permission to open any interface")
        sys.exit(1)
    elif len(ifs) == 1:
        print("only one interface present, defaulting to it")
        return ifs[0]
    count = 0
    for iface in ifs:
        print(count, ": ", iface)
        count += 1
    idx = int(input('Please select an interface: '))
    return ifs[idx]

dev = getInterface()
index = 0
cap = pcapy.open_live(dev,
                      65536,  # to ensure capturing all of the
                      1,  # promiscious mode on
                      0)  # time out
print("Listening on %s: net=%s, mask=%s, linktype=%d" % (dev, cap.getnet(),
                                                         cap.getmask(),
                                                         cap.datalink()))
print("capturing data...")
dumper = cap.dump_open('data_p.txt')
while True:
    (header, packet) = cap.next()
    if ((len(packet) == 542) and
            (packet[26] == 169) and
            (packet[27] == 254) and
            (packet[29] == 15)):
        index += 1
        print(index)
        dumper.dump(header, packet)





