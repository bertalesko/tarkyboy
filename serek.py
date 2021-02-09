import dpkt
import pcapy
import socket
import datetime

iplist = ["unn-84-17-55-137.cdn77.com", "104.22.29.180", "172.67.41.203"]


def inet_to_str(inet):
    try:
        return socket.inet_ntop(socket.AF_INET, inet)

    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)

        
def print_packets(pcap):
    """Print out information about each packet in a pcap

       Args:
           pcap: dpkt pcap reader object (dpkt.pcap.Reader)
    """
    # For each packet in the pcap process the contents
    for timestamp, buf in pcap:

        # Print out the timestamp in UTC
        #print("Timestamp: ", timestamp)

        # Unpack the Ethernet frame (mac src/dst, ethertype)
        #eth = dpkt.ethernet.Ethernet(buf)
        #print("Ethernet Frame: ", mac_addr(eth.src), mac_addr(eth.dst), eth.type)

        # Make sure the Ethernet data contains an IP packet
        if not isinstance(eth.data, dpkt.ip.IP):
            print("Non IP Packet type not supported %s\n" % eth.data.__class__.__name__)
            continue

        # Now unpack the data within the Ethernet frame (the IP packet)
        # Pulling out src, dst, length, fragment info, TTL, and Protocol
        ip = eth.data

        # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
        do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
        more_fragments = bool(ip.off & dpkt.ip.IP_MF)
        fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

        # Print out the info
        print("IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)\n" % \
              (inet_to_str(ip.src), inet_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments, fragment_offset))


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


cap=pcapy.open_live(dev,65538,1,0)
(header,payload)=cap.next()
print("start")
while header:
    eth=dpkt.ethernet.Ethernet(payload)
    

    # Check whether IP packets: to consider only IP packets 
    if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
            continue
            # Skip if it is not an IP packet
    ip=eth.data
   
    s_addr = str(inet_to_str(ip.src))
    d_addr = str(inet_to_str(ip.dst))
    if (s_addr or d_addr) in iplist:
        print(".")
        if ip.p==dpkt.ip.IP_PROTO_TCP: # Check for TCP packets
            TCP=ip.data 
            print("/###################TCP###############")
            print(inet_to_str(ip.src) +"->" + inet_to_str(ip.dst))
            print_packets(eth)
            # ADD TCP packets Analysis code here
        elif ip.p==dpkt.ip.IP_PROTO_UDP: # Check for UDP packets
            UDP=ip.data 
            
            print("/###################UDP###############")
            print(eth)
            # UDP packets Analysis code here

    (header,payload)=cap.next()


