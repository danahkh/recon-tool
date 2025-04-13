# Recon Tool

A robust reconnaissance tool for penetration testing. It automates various scans like port scanning, subdomain enumeration, and path discovery.

## Features
- Accepts IPs, domains, or lists of both.
- Customizable wordlist support for path discovery.
- Flexible tool selection (Dirb or Gobuster).
- Organized results in plain-text files.
- Smart file naming to avoid overwriting.

## Usage
Run the tool with the following options:
```bash
python recon_tool.py -u <target> [-w <wordlist>] [-di | -gu] [-o <output_dir>]
