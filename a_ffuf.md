---
name: FFUF Microagent
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - run ffuf
---

# FFUF Microagent

FFUF (Fuzz Faster U Fool) is a fast and flexible web fuzzer written in Go. It is ideal for security assessments and penetration testing, allowing you to discover hidden directories, files, parameters, subdomains, and vulnerabilities through concurrent HTTP requests.

## Key Features

- Directory & File Discovery: Brute-force common directory names and file extensions.
- Parameter & API Fuzzing: Discover hidden query parameters and API endpoints.
- Subdomain Enumeration: Check potential subdomains via HTTP Host header or DNS.
- Performance & Concurrency: High-speed scanning with configurable threads.
- Response Filtering: Filter results by status codes, sizes, words, or regex patterns.
- Recursive Scanning: Follow links and scan deeper levels automatically.
- Custom Headers & Methods: Test diverse HTTP methods and custom headers.
- Multiple Output Formats: JSON, CSV, and plain text for easy integration.
- Rate Limiting & Throttling: Control request rates to avoid server overload.

## Usage

### Quick Execution
Run any FFUF command directly:
```bash
run ffuf -w /workspace/wordlists/wordlist.txt -u http://example.com/FUZZ
```

### Interactive Guided Session
Trigger without flags to start a step-by-step workflow:
```bash
run ffuf
```
The agent will guide you through:
1. Choosing a scan type
2. Verifying/downloading the appropriate wordlist
3. Specifying the target URL or parameters
4. Executing the tailored FFUF command and returning results

## Interactive Guidance
1. Prompt: "What would you like to do with FFUF?"
   1) Directory & File Discovery
   2) API Endpoint Discovery
   3) Subdomain Enumeration
   4) File Leak Detection
   5) Virtual Host Discovery
   6) Path Traversal Fuzzing
   7) CORS Misconfiguration Checks
   8) JavaScript Endpoint Discovery
   9) Custom Wordlist

2. Wordlist Management:
   - Wordlists are stored under `/workspace/wordlists`.
   - Missing lists are downloaded automatically from SecLists using a loop and verbose `wget`, e.g.:
     ```bash
     mkdir -p /workspace/wordlists
     for list in directory-list-2.3-medium.txt subdomains-top1mil-5000.txt file-extensions.txt; do
       url="https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/$list"
       wget -v -P /workspace/wordlists "$url" -O "/workspace/wordlists/$list" || echo "Failed to download $list"
     done
     ```

3. Target Input:
   - The agent asks for the base URL and any additional parameters (e.g., query string, extensions).

4. Execution:
   - The agent runs the appropriate `ffuf` command and displays the results.

### Example Session
```text
User: run ffuf
Agent: What would you like to do with FFUF?
       1) Directory & File Discovery
       2) API Endpoint Discovery
       ...
User: 1
Agent: Verifying wordlist: directory-list-2.3-medium.txt
Agent: Downloading if missing...
Agent: Please provide the target URL:
User: http://example.com
Agent: Running:
       ffuf -w /workspace/wordlists/directory-list-2.3-medium.txt -u http://example.com/FUZZ -mc 200,204,301,403
Agent: [Results]
```

## Usage Options

1. Directory & File Discovery
   ```bash
   ffuf -w /workspace/wordlists/directory-list-2.3-medium.txt -u http://example.com/FUZZ -mc 200,204,301,403
   ```

2. API Endpoint Discovery
   ```bash
   ffuf -w /workspace/wordlists/api-endpoints.txt -u http://example.com/api/FUZZ -mc 200,403
   ```

3. Subdomain Enumeration
   ```bash
   ffuf -w /workspace/wordlists/subdomains-top1mil-5000.txt -u http://FUZZ.example.com -host
   ```

4. File Leak Detection
   ```bash
   ffuf -w /workspace/wordlists/file-extensions.txt -u http://example.com/FUZZ -mc 200,403
   ```

5. Virtual Host Discovery
   ```bash
   ffuf -w /workspace/wordlists/subdomains-top1mil-5000.txt -u http://FUZZ.example.com -host
   ```

6. Path Traversal Fuzzing
   ```bash
   ffuf -w /workspace/wordlists/path-traversal.txt -u http://example.com/vuln?file=../../FUZZ -mc 200,403
   ```

7. CORS Misconfiguration Checks
   ```bash
   ffuf -w /workspace/wordlists/origins.txt -u http://example.com/api \
        -H "Origin: FUZZ" -H "Access-Control-Request-Method: GET"
   ```

8. JavaScript Endpoint Discovery
   ```bash
   ffuf -w /workspace/wordlists/js-endpoints.txt -u http://example.com/js/FUZZ.js -mc 200,403
   ```

9. Custom Wordlist Usage
   ```bash
   ffuf -w /workspace/wordlists/custom.txt -u http://example.com/FUZZ -mc 200,403
   ```

10. Multiple Extensions
    ```bash
    ffuf -w raft-medium-words.txt -u http://example.com/FUZZ \
         -e .php,.aspx,.json,.xml -mc 200,204,301,302,307,401,403 -t 150 -ac
    ```
11. Recursive Scanning
    ```bash
    ffuf -w /workspace/wordlists/directory-list-2.3-medium.txt \
         -u http://example.com/FUZZ -recursion -recursion-depth 2
    ```



## Innovative Uses

- **Parameter Discovery**:
  ```bash
  ffuf -w /workspace/wordlists/parameters.txt -u http://example.com/page?FUZZ=test -mc 200,302
  ```

- **Recursive Scanning**:
  ```bash
  ffuf -w /workspace/wordlists/directory-list-2.3-medium.txt \
       -u http://example.com/FUZZ -recursion -recursion-depth 2
  ```

- **Custom Filtering**: Use `-fl`, `-fc`, or `-fw` to filter by size, code, or word count.

## Notes

- Ensure FFUF is installed at `/root/go/bin/ffuf` or in PATH.
- Wordlists are managed under `/workspace/wordlists` with auto-download.
- Adjust flags (`-mc`, `-t`, `-e`, etc.) to suit your testing environment.

## Base Command
```bash
/root/go/bin/ffuf -w wordlist.txt -u http://example.com/FUZZ
```
