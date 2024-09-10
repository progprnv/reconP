import requests
import argparse
import asyncio
import httpx
import subprocess

# Add your API keys here
SHODAN_API_KEY = 'your_shodan_api_key'
WHOIS_API_KEY = 'your_whoislookup_api_key'
VIRUSTOTAL_API_KEY = 'your_virustotal_api_key'
CENSYS_API_ID = '9f5a-be11-4b9e-9564-9596e78'
CENSYS_API_SECRET = 'Va92kyMYPS7ANKpI8CjV'
GOOGLE_API_KEY = 'AIzaSyCcEqqOERofbkudEY_iVC2_Wfv0A'
ZOOMEYE_API_KEY = '3833802-b9FF-6E1A5-7d2d-9792d64082adf'
INTELX_API_KEY = '1995e804-3c71-4938042-8042802-efa29ae2964d'
REDHUNT_API_KEY = 'VRp7HK3jWiRSnpPfois7979spn4tvDVi0vM'
DNSDUMPSTER_API_KEY = 'zsdqYb0rvIVYh2uPHo5Yk4EljV9GEKn44hDL9V2DFXznflW37Q5pZl8pvQHUHWav'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; SubFinder/1.0; +https://example.com/bot)'
}

# Function to get subdomains from Censys
def get_censys_subdomains(domain):
    print(f"[*] Searching Censys for subdomains of {domain}...")
    try:
        url = f"https://search.censys.io/api/v1/search/certificates"
        data = {
            "query": domain,
            "fields": ["parsed.names"],
            "flatten": True
        }
        response = requests.post(url, json=data, auth=(CENSYS_API_ID, CENSYS_API_SECRET), headers=HEADERS)
        if response.status_code == 200:
            subdomains = response.json().get('results', [])
            return [sub for result in subdomains for sub in result['parsed.names'] if domain in sub]
        else:
            print(f"[-] Censys API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[-] Error fetching data from Censys: {e}")
    return []

# Function to get subdomains from VirusTotal
def get_virustotal_subdomains(domain):
    print(f"[*] Searching VirusTotal for subdomains of {domain}...")
    try:
        url = f"https://www.virustotal.com/vtapi/v2/domain/report?apikey={VIRUSTOTAL_API_KEY}&domain={domain}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get('subdomains', [])
        else:
            print(f"[-] VirusTotal API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[-] Error fetching data from VirusTotal: {e}")
    return []

# Function to get subdomains from Intelx
def get_intelx_subdomains(domain):
    print(f"[*] Searching Intelx for subdomains of {domain}...")
    try:
        url = f"https://2.intelx.io/intelligent/search/domain/{domain}?apikey={INTELX_API_KEY}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get('subdomains', [])
        else:
            print(f"[-] Intelx API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[-] Error fetching data from Intelx: {e}")
    return []

# Function to get subdomains from ZoomEye
def get_zoomeye_subdomains(domain):
    print(f"[*] Searching ZoomEye for subdomains of {domain}...")
    try:
        url = f"https://api.zoomeye.org/host/search?query=site:{domain}&apikey={ZOOMEYE_API_KEY}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return [hit['name'] for hit in response.json().get('matches', []) if 'name' in hit]
        else:
            print(f"[-] ZoomEye API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[-] Error fetching data from ZoomEye: {e}")
    return []

# Function to get subdomains from RedHunt Labs
def get_redhunt_subdomains(domain):
    print(f"[*] Searching RedHunt Labs for subdomains of {domain}...")
    try:
        url = f"https://reconapi.redhuntlabs.com/community/v1/domains/subdomains/{domain}?apikey={REDHUNT_API_KEY}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get('subdomains', [])
        else:
            print(f"[-] RedHunt Labs API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[-] Error fetching data from RedHunt Labs: {e}")
    return []

# Function to get subdomains from DNSDumpster
def get_dnsdumpster_subdomains(domain):
    print(f"[*] Searching DNSDumpster for subdomains of {domain}...")
    try:
        url = f"https://dnsdumpster.com/api/{domain}?apikey={DNSDUMPSTER_API_KEY}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get('dns_records', {}).get('hostnames', [])
        else:
            print(f"[-] DNSDumpster API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[-] Error fetching data from DNSDumpster: {e}")
    return []

# Function to get URLs from Waybackurls
def get_waybackurls(domain):
    print(f"[*] Searching Waybackurls for URLs of {domain}...")
    try:
        result = subprocess.run(['waybackurls', domain], capture_output=True, text=True)
        urls = result.stdout.splitlines()
        return urls
    except Exception as e:
        print(f"[-] Error fetching data from Waybackurls: {e}")
    return []

# Function to get URLs from Katana
def get_katana_urls(domain):
    print(f"[*] Searching Katana for URLs of {domain}...")
    try:
        result = subprocess.run(['katana', '-d', domain], capture_output=True, text=True)
        urls = result.stdout.splitlines()
        return urls
    except Exception as e:
        print(f"[-] Error fetching data from Katana: {e}")
    return []

# Function to check if subdomains are alive
async def check_alive_subdomain(subdomain, alive_subdomains):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"http://{subdomain}", headers=HEADERS, timeout=5)
            if response.status_code == 200:
                alive_subdomains.append(subdomain)
                print(f"[+] Alive: {subdomain}")
        except Exception as e:
            print(f"[-] Error checking {subdomain}: {e}")

# Main function to gather subdomains and check if they are alive
async def find_and_check_subdomains(domain):
    all_subdomains = set()
    all_urls = set()

    # Get subdomains from various APIs
    all_subdomains.update(get_censys_subdomains(domain))
    all_subdomains.update(get_virustotal_subdomains(domain))
    all_subdomains.update(get_intelx_subdomains(domain))
    all_subdomains.update(get_zoomeye_subdomains(domain))
    all_subdomains.update(get_redhunt_subdomains(domain))
    all_subdomains.update(get_dnsdumpster_subdomains(domain))

    # Get URLs from Waybackurls and Katana
    all_urls.update(get_waybackurls(domain))
    all_urls.update(get_katana_urls(domain))

    print(f"[*] Total discovered subdomains: {len(all_subdomains)}")
    print(f"[*] Total discovered URLs: {len(all_urls)}")

    # Check which subdomains are alive
    if all_subdomains:
        alive_subdomains = []
        tasks = [check_alive_subdomain(subdomain, alive_subdomains) for subdomain in all_subdomains]
        await asyncio.gather(*tasks)

        print(f"[*] Total alive subdomains: {len(alive_subdomains)}")
        return alive_subdomains, all_urls
    else:
        print("[-] No subdomains found.")
        return [], all_urls

# Command-line interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomain Finder using multiple APIs.")
    parser.add_argument("-u", "--url", help="Target domain to find subdomains and URLs for", required=True)
    args = parser.parse_args()

    target_domain = args.url.strip()

    print(f"[*] Starting subdomain and URL discovery for {target_domain}...")
    alive_subdomains, discovered_urls = asyncio.run(find_and_check_subdomains(target_domain))

    print(f"\n[*] Discovered Subdomains:")
    for subdomain in alive_subdomains:
        print(f"  - {subdomain}")

    print(f"\n[*] Discovered URLs:")
    for url in discovered_urls:
        print(f"  - {url}")
