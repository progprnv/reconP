# reconP

![image](https://github.com/progprnv/reconP/assets/145828371/ee620ef9-a7e2-46b1-a734-3b54516fe3e2)


reconP is a simple web server scanner tool that checks for common vulnerabilities and issues on a given website. This tool reads common paths from a wordlist file and scans the target website.

## Features

- Interactive selection of target URL and wordlist file
- Scans for common vulnerabilities
- Simple and easy to use

## Installation and Usage

### Prerequisites

- Python 3.x
- `requests` library (Install using `pip install requests`)

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/reconP.git
   cd reconP


Example:
$ python reconP.py
Enter the target URL: example.com
Enter the path to the wordlist file: wordlist.txt
Scanning http://example.com for common vulnerabilities....
