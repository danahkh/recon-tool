import os
import subprocess
import argparse
from datetime import datetime

# Helper function to run a command and save output
def run_command(command, output_file):
    with open(output_file, "w") as f:
        subprocess.run(command, stdout=f, stderr=subprocess.DEVNULL, text=True)

# Helper function for smart file naming
def get_unique_filename(directory, base_name, extension):
    counter = 1
    while True:
        file_name = f"{base_name}{'' if counter == 1 else f'_{counter}'}.{extension}"
        full_path = os.path.join(directory, file_name)
        if not os.path.exists(full_path):
            return full_path
        counter += 1

# Recon Tool
def recon_tool(targets, wordlist, use_dirb, use_gobuster, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for target in targets:
        print(f"[+] Scanning target: {target}")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_dir = os.path.join(output_dir, target.replace("://", "_").replace("/", "_"))
        os.makedirs(target_dir, exist_ok=True)

        # Port Scanning
        ports_file = get_unique_filename(target_dir, "ports", "txt")
        run_command(["nmap", "-p", "22,80,443", "-Pn", target], ports_file)

        # Subdomain Enumeration
        subdomains_file = get_unique_filename(target_dir, "subdomains", "txt")
        run_command(["sublist3r", "-d", target, "-o", subdomains_file], subdomains_file)

        # Path Discovery
        if wordlist:
            if use_gobuster:
                paths_file = get_unique_filename(target_dir, "paths_gobuster", "txt")
                run_command(["gobuster", "dir", "-u", target, "-w", wordlist], paths_file)
            if use_dirb:
                paths_file = get_unique_filename(target_dir, "paths_dirb", "txt")
                run_command(["dirb", target, wordlist], paths_file)

        # DNS Information
        dns_file = get_unique_filename(target_dir, "dns_info", "txt")
        with open(dns_file, "w") as f:
            f.write(subprocess.getoutput(f"dig A {target} +short") + "\n")
            f.write(subprocess.getoutput(f"dig MX {target} +short") + "\n")
            f.write(subprocess.getoutput(f"dig TXT {target} +short") + "\n")

        print(f"[+] Results saved in: {target_dir}")

# Main Function
def main():
    parser = argparse.ArgumentParser(description="Robust Recon Tool for Pentesters")
    parser.add_argument("-u", "--url", help="Target URL/IP or file with list of targets", required=True)
    parser.add_argument("-w", "--wordlist", help="Wordlist for directory/path discovery")
    parser.add_argument("-di", "--use-dirb", action="store_true", help="Use Dirb for directory discovery")
    parser.add_argument("-gu", "--use-gobuster", action="store_true", help="Use Gobuster for directory discovery")
    parser.add_argument("-o", "--output", help="Output directory (default: current directory)", default="results")
    args = parser.parse_args()

    # Parse targets
    if os.path.isfile(args.url):
        with open(args.url, "r") as file:
            targets = [line.strip() for line in file.readlines()]
    else:
        targets = [args.url.strip()]

    # Run the recon tool
    recon_tool(targets, args.wordlist, args.use_dirb, args.use_gobuster, args.output)

if __name__ == "__main__":
    main()
