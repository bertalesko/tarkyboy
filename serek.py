import dpkt
import pcapy

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


cap=pcapy.open_live('eth0',100000,1,0)
(header,payload)=cap.next()

while header:
    eth=dpkt.ethernet.Ethernet(str(payload))

    # Check whether IP packets: to consider only IP packets 
    if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
            continue
            # Skip if it is not an IP packet
    ip=eth.data
    if ip.p==dpkt.ip.IP_PROTO_TCP: # Check for TCP packets
           TCP=ip.data 
           # ADD TCP packets Analysis code here
    elif ip.p==dpkt.ip.IP_PROTO_UDP: # Check for UDP packets
           UDP=ip.data 
           # UDP packets Analysis code here

    (header,payload)=cap.next()


