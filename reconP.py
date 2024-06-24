import requests

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

def check_url(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
    return False

def scan_website(base_url, wordlist_file):
    paths = load_wordlist(wordlist_file)
    if not paths:
        print("No paths to scan. Please check the wordlist file.")
        return

    if not base_url.startswith('http://') and not base_url.startswith('https://'):
        base_url = 'http://' + base_url

    print(f"Scanning {base_url} for common vulnerabilities...")

    for path in paths:
        full_url = base_url.rstrip('/') + path
        if check_url(full_url):
            print(f"[+] Found: {full_url}")
        else:
            print(f"[-] Not found: {full_url}")

    print("Scan complete.")

if __name__ == "__main__":
    target_url = input("Enter the target URL: ")
    wordlist_file = input("Enter the path to the wordlist file: ")
    scan_website(target_url, wordlist_file)
