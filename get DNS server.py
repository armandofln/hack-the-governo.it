import subprocess

def get_dns_servers():
	result = subprocess.run(['resolvectl', 'status'], capture_output=True, text=True)
	dns_servers = {}
	current_iface = None

	for line in result.stdout.splitlines():
		if line.strip().endswith(':'):
			current_iface = line.strip(':').strip()
		elif 'DNS Servers' in line:
			servers = line.split(':', 1)[1].strip().split()
			if current_iface:
				dns_servers[current_iface] = servers

	return dns_servers

dns_info = get_dns_servers()
for iface, servers in dns_info.items():
	print(f"{iface}: {servers}")
