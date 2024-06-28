import requests
import httpx
import asyncio
import threading

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; reconP/1.0; +https://example.com/bot)'
}

def load_wordlist(wordlist_file):
    try:
        with open(wordlist_file, 'r') as file:
            paths = [line.strip() for line in file if line.strip()]
        return paths
    except FileNotFoundError:
        print(f"Wordlist file '{wordlist_file}' not found.")
        return []

async def check_alive_subdomain(subdomain, alive_subdomains):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(subdomain, headers=HEADERS, timeout=5)
            if response.status_code == 200:
                alive_subdomains.append(subdomain)
                print(f"[+] Alive: {subdomain}")
            else:
                print(f"[-] Not alive: {subdomain}")
        except httpx.RequestError as e:
            print(f"Error checking {subdomain}: {e}")

async def check_all_subdomains(subdomains):
    alive_subdomains = []
    tasks = [check_alive_subdomain(subdomain, alive_subdomains) for subdomain in subdomains]
    await asyncio.gather(*tasks)
    return alive_subdomains

def check_url(url, results):
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            results.append(f"[+] Found: {url}")
        else:
            results.append(f"[-] Not found: {url}")
    except requests.RequestException as e:
        results.append(f"Error checking {url}: {e}")

def scan_website(base_url, wordlist_file, threads=10):
    paths = load_wordlist(wordlist_file)
    if not paths:
        print("No paths to scan. Please check the wordlist file.")
        return

    if not base_url.startswith('http://') and not base_url.startswith('https://'):
        base_url = 'http://' + base_url

    print(f"Scanning {base_url} for common vulnerabilities...")

    results = []
    threads_list = []

    for path in paths:
        full_url = base_url.rstrip('/') + '/' + path
        thread = threading.Thread(target=check_url, args=(full_url, results))
        threads_list.append(thread)
        thread.start()

        if len(threads_list) >= threads:
            for t in threads_list:
                t.join()
            threads_list = []

    for t in threads_list:
        t.join()

    for result in results:
        print(result)

    print("Scan complete.")

    save_results = input("Would you like to save the results to a file? (y/n): ").strip().lower()
    if save_results == 'y':
        file_name = input("Enter the filename to save the results: ").strip()
        with open(file_name, 'w') as file:
            for result in results:
                file.write(result + '\n')
        print(f"Results saved to {file_name}")

if __name__ == "__main__":
    target_url = input("Enter the target URL: ").strip()
    wordlist_file = input("Enter the path to the wordlist file: ").strip()
    
    subdomains_file = input("Enter the path to the subdomains file: ").strip()
    subdomains = load_wordlist(subdomains_file)
    
    print("Checking for alive subdomains...")
    alive_subdomains = asyncio.run(check_all_subdomains(subdomains))
    
    for alive_subdomain in alive_subdomains:
        scan_website(alive_subdomain, wordlist_file)
