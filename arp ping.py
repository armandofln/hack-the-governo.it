import threading
from scapy.all import Ether, ARP, srp

def arp_scan(network, iface):
	pkt = (
		Ether(dst = "ff:ff:ff:ff:ff:ff") /
		ARP(pdst = network, timeout = 5, iface = iface)
	)
	ans, _ = srp(pkt)
	print(ans)

arp_scan("192.168.0.0/24", "eth0")