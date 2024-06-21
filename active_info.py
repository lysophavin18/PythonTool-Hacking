import nmap
import sys
import time
import os

if len(sys.argv) != 2:
    print("Usage: python active_info.py <target_ip>")
    sys.exit(1)

target_ip = sys.argv[1]

# Check if the script is running as root
if os.geteuid() != 0:
    print("This script must be run as root. Please use sudo.")
    sys.exit(1)

# Initialize the scanner
nmap_scan = nmap.PortScanner()
print('\nRunning.........\n')

try:
    # Perform the scan
    nmap_scanner = nmap_scan.scan(target_ip, '80', arguments='-O')

    # Gather scan results
    host_is_up = f"The host {nmap_scan['scan'][target_ip]['status']['state']}.\n"
    port_open = f"The port 80 is: {nmap_scan['scan'][target_ip]['tcp'][80]['state']}.\n"
    method_scan = f"The method of scanning is: {nmap_scan['scan'][target_ip]['tcp'][80]['reason']}\n"
    gussed_os = "There is a %s percent chance that the host is running %s" % (
        nmap_scan['scan'][target_ip]['osmatch'][0]['accuracy'],
        nmap_scan['scan'][target_ip]['osmatch'][0]['name']
    )

    # Write the results to a file
    with open(f"{target_ip}.txt", 'w') as f:
        f.write(host_is_up + port_open + method_scan + gussed_os)
        f.write("\nReport Generated: " + time.strftime("%Y-%m-%d_%H:%M:%S GMT", time.gmtime()))

    print("\nFinished....")

except nmap.PortScannerError as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
except KeyError as e:
    print(f"Unexpected response structure: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)
