iptables -A FORWARD -p udp --dport 53 -j DROP
ip6tables -A FORWARD -p udp --dport 53 -j DROP
