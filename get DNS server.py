import subprocess

def get_dns_servers():
	result = subprocess.run(['resolvectl', 'status'], capture_output=True, text=True)
	dns_servers = {}
	current_iface = None

	DNS_section = False
	for line in result.stdout.splitlines():
		if DNS_section:
			if ": " in line:
				DNS_section = False
		

		if DNS_section:
			servers = line.split(':', 1)[1].strip().split()
			for server in servers:
				dns_servers[current_iface].append(server)
		elif line.strip().endswith(')'):
			current_iface = line.split("(")[1].split(")")[0]
		elif 'DNS Servers' in line:
			servers = line.split(':', 1)[1].strip().split()
			if current_iface:
				dns_servers[current_iface] = servers
				DNS_section = True

	return dns_servers

dns_info = get_dns_servers()
for iface, servers in dns_info.items():
	print(f"{iface}: {servers}")
