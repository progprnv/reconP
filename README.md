

![image](https://github.com/progprnv/reconP/assets/145828371/ee620ef9-a7e2-46b1-a734-3b54516fe3e2)

# reconP

## Description

**reconP** is a powerful subdomain discovery and verification tool that integrates multiple APIs to gather and check the status of subdomains for a given target domain. It utilizes various services to enhance subdomain enumeration and validate the operational status of discovered subdomains.

## Features

- **API Integration**: Fetches subdomains from multiple APIs including Censys, VirusTotal, Intelx, ZoomEye, RedHunt Labs, and DNSDumpster.
- **Subdomain Verification**: Asynchronously checks if the discovered subdomains are alive.
- **Command-Line Interface**: Easily run the tool via command-line arguments.

## APIs Used

- **Censys**: For certificate-based subdomain discovery.
- **VirusTotal**: To obtain subdomain data from domain reports.
- **Intelx**: Provides subdomain information from intelligent searches.
- **ZoomEye**: Fetches subdomains from host searches.
- **RedHunt Labs**: Retrieves subdomains from reconnaissance data.
- **DNSDumpster**: Gathers DNS records and subdomains.

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone https://github.com/your-repo/reconP.git
   cd reconP
   pip install requests httpx

