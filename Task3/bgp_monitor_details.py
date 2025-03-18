from jsonrpclib import Server
import pprint
import ssl
import json
import os

# Disable SSL verification if using self-signed certificates
ssl._create_default_https_context = ssl._create_unverified_context

# Dictionary of switch IPs mapped to their names
switches = {
    "172.20.20.3": "ASBR1",
    "172.20.20.12": "ASBR2",
    "172.20.20.11": "ASBR3",
    "172.20.20.15": "ASBR4",
    "172.20.20.2": "ASBR5",
    "172.20.20.14": "ASBR6",
    "172.20.20.9": "ASBR7",
    "172.20.20.7": "ASBR8",
    "172.20.20.10": "R1",
    "172.20.20.8": "R2",
    "172.20.20.4": "R3",
    "172.20.20.6": "R4",
    "172.20.20.5": "Ri"
}

# Username and password
username = "admin"
password = "NEW_PASSWORD"  # Use the new password here

# Output folder
output_folder = "bgp_outputs"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to gather and save data for each switch
def gather_info(ip, hostname):
    try:
        print(f"Connecting to {hostname} ({ip})...")
        switch = Server(f"https://{username}:{password}@{ip}/command-api")

        # Run multiple commands
        response = switch.runCmds(1, [
            "show hostname",           # Show hostname
            "show ip bgp",             # Show BGP info
            "show ip route",           # Show routing table
            "show interfaces"          # Show interfaces
        ])

        # Print the response
        pprint.pprint(response)

        # Save the output to a JSON file named after the switch hostname
        output_file = os.path.join(output_folder, f"{hostname}_bgp_monitor.json")
        with open(output_file, "w") as f:
            json.dump(response, f, indent=4)

        print(f"Saved output to {output_file}")

    except Exception as e:
        print(f"Error connecting to {hostname} ({ip}): {e}")

# Run the function for each switch
for ip, hostname in switches.items():
    gather_info(ip, hostname)

