import binascii
from struct import *
import datetime
import sys
import pcapy
import socket

iplist = ["unn-84-17-55-137.cdn77.com", "104.22.29.180", "172.67.41.203", "51."]

def eth_addr (a) :
	b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (a[0] , a[1] ,a[2], a[3], a[4] , a[5])
	return b

def getInterface():
    # Grab a list of interfaces that pcap is able to listen on.
    # The current user will be able to listen from all returned interfaces,
    # using open_live to open them.
    ifs = pcapy.findalldevs()

    # No interfaces available, abort.
    if 0 == len(ifs):
        print("You don't have enough permissions to open any interface on this system.")
        sys.exit(1)

    # Only one interface available, use it.
    elif 1 == len(ifs):
        print("Only one interface present, defaulting to it.")
        return ifs[0]

    # Ask the user to choose an interface from the list.
    count = 0
    for iface in ifs:
        print("%i - %s" % (count, iface))
        count += 1
    idx = int(input('Please select an interface: '))

    return ifs[idx] 


def main():
    inf = getInterface()
    cap = pcapy.open_live(inf,65538,1,0)
    count = 1 
    while (1==1):
        (header,payload) = cap.next()

        parse_packet(payload)
        count+=1

def parse_packet(packet) :
    try:
        with open("textowy.txt", "a") as f:
            #print (f)

            #parse ethernet header
            eth_length = 14

            eth_header = packet[:eth_length]
            eth = unpack('!6s6sH' , eth_header)
            eth_protocol = socket.ntohs(eth[2])
            #print ("Destination MAC : " + eth_addr(packet[0:6]) + " Source MAC : " + eth_addr(packet[6:12]) + " Protocol : " + str(eth_protocol))

            #Parse IP packets, IP Protocol number = 8

            if eth_protocol == 8 :
                #Parse IP header
                
                #take first 20 characters for the ip header
                #tab
                ip_header = packet[eth_length:20+eth_length]
                
                #now unpack them :)
                iph = unpack('!BBHHHBBH4s4s' , ip_header)

                version_ihl = iph[0]
                version = version_ihl >> 4
                ihl = version_ihl & 0xF

                iph_length = ihl * 4

                ttl = iph[5]
                protocol = iph[6]
                s_addr = socket.inet_ntoa(iph[8]);
                d_addr = socket.inet_ntoa(iph[9]);
                if (s_addr or d_addr) in iplist:
                    #tab
                        
                    


                        if protocol == 6:
                                # NA TCP WYSYLANE SA DANE Z MENU - INVENTORY ITP, DANE PRZESYLANE SA PODCZAS DOKONYWANIA TRANSAKCJI, 
                                # LUB W PRZYPADKU INVENTORY PO ZAMKNIECIU INVENTORY
                                t= iph_length + eth_length
                                tcp_header= packet[t:t+20]

                                tcph = unpack('!HHLLBBHHH' , tcp_header)
                                source_port = tcph[0]
                                dest_port = tcph[1]
                                sequence = tcph[2]
                                acknowledgement = tcph[3]
                                doff_reserved = tcph[4]
                                tcph_length = doff_reserved >> 4
                                print (" Protocol : " + str(protocol) + " Source Address : " + str(s_addr) + ":"+str(source_port) +  " Destination Address : " + str(d_addr) +":"+str(dest_port))
                                #print("Srouce port : " " Dest port : " + str(dest_port) + " sequence number : " + str(sequence) + " Acknowledgement : " + str(acknowledgement) + " TCP header length : " + str(tcph_length))
                                h_size = eth_length + iph_length + tcph_length *4
                                data_size = len(packet) - h_size

                                data = packet[h_size:]
                                out = binascii.b2a_hex(data)
                                #print ("data : " + str(data))
                                


                                print ("data 2 : " +str(out))

                                
                                #f=open("guru99.txt","a+")
                                
                                f.write(str(s_addr) +"->"+str(d_addr) +" " + str(out) + "\n")
                                #f.close()
                                
                                
                                #if (s_addr or d_addr) == "172.67.41.203":
                            #   print ("elo")

                        elif protocol == 17 :
                            u = iph_length + eth_length
                            udph_length = 8
                            udp_header = packet[u:u+8]

                            #now unpack them :)
                            udph = unpack('!HHHH' , udp_header)
                            
                            source_port = udph[0]
                            dest_port = udph[1]
                            length = udph[2]
                            checksum = udph[3]
                            
                            print ("Source Port : " + str(source_port) + " Dest Port : " + str(dest_port) + " Length : " + str(length) + " Checksum : " + str(checksum))
                            
                            h_size = eth_length + iph_length + udph_length
                            data_size = len(packet) - h_size
                            
                            #get data from the packet
                            data = packet[h_size:]
                            out = binascii.b2a_hex(data)
                            #print ("data : " + str(data))
                            print ("data 2 udp : " +str(out))
                            
                            #print ("Data : " + str(data))
                f.close() 
    except:
        print("error")
                    #else:
                    
                    #   print ("protocol 6")
                    

        

                

main()

