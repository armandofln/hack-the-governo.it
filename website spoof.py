from scapy.all import sniff, send, IP, TCP, Raw
import dns.resolver
import threading
import time



TARGET_DOMAIN = "governo.it"
REAL_TARGET_IP = None

connection_map = {}

def get_ip_and_ttl(domain):
    answer = dns.resolver.resolve(domain, 'A')
    ip = answer[0].to_text()
    ttl = answer.rrset.ttl
    return ip, ttl

def update_real_ip_loop():
    global REAL_TARGET_IP
    while True:
        try:
            ip, ttl = get_ip_and_ttl(TARGET_DOMAIN)
            REAL_TARGET_IP = ip
            #print(f"[DNS] {TARGET_DOMAIN} → {ip} (TTL: {ttl}s)")
            time.sleep(ttl)
        except Exception as e:
            print("[!] DNS resolution error:", e)
            time.sleep(2)

def process_packet(pkt):
    global REAL_TARGET_IP

    if IP not in pkt or TCP not in pkt:
        return

    ip = pkt[IP]
    tcp = pkt[TCP]

    if ip.dst == REAL_TARGET_IP:
        connection_map[tcp.sport] = ip.src

        ip.dst = "127.0.0.1"
        del ip.chksum
        del tcp.chksum

        send(ip / tcp / (pkt[Raw].load if Raw in pkt else b''), verbose=False)

    elif ip.src == "127.0.0.1" and tcp.sport == 80:
        if ip.dport in connection_map:
            real_dst_ip = connection_map[ip.dport]

            ip.src = real_dst_ip
            del ip.chksum
            del tcp.chksum

            send(ip / tcp / (pkt[Raw].load if Raw in pkt else b''), verbose=False)

if __name__ == "__main__":
    threading.Thread(target=update_real_ip_loop, daemon=True).start()

    print("[*] Starting packet interceptor...")
    sniff(filter="tcp", prn=process_packet, store=0)
