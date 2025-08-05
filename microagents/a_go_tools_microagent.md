

---
name: Go Tools Microagent
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - run hakcheckurl
  - run hakip2host
  - run haklistgen
  - run hakoriginfinder
  - run hakrawler
  - run hakrevdns
  - run haktldextract
  - run haktrails
  - run httpx
  - run subfinder
  - run assetfinder
  - run waybackurls
  - run ffuf

# Go Tools Microagent

This microagent provides a simple interface to run various Go-based tools.

## Usage

To use this microagent, trigger it with one of the following phrases:
- "run hakcheckurl"
- "run hakip2host"
- "run haklistgen"
- "run hakoriginfinder"
- "run hakrawler"
- "run hakrevdns"
- "run haktldextract"
- "run haktrails"
- "run httpx"
- "run subfinder"
- "run assetfinder"
- "run waybackurls"
- "run ffuf"

The agent will execute the corresponding Go tool and return the output.

## Examples

User: run hakcheckurl
Agent: [Executes `hakcheckurl` and returns the output]

User: run hakip2host
Agent: [Executes `hakip2host` and returns the output]

## Notes

- Ensure that the respective Go tools are installed on your system.
- This microagent runs the tools with default options. You can modify the commands as needed within the agent's code.

## Commands

The commands run by this microagent are:
```bash
/root/go/bin/hakcheckurl
/root/go/bin/hakip2host
/root/go/bin/haklistgen
/root/go/bin/hakoriginfinder
/root/go/bin/hakrawler
/root/go/bin/hakrevdns
/root/go/bin/haktldextract
/root/go/bin/haktrails
/root/go/bin/httpx
/root/go/bin/subfinder
/root/go/bin/assetfinder
/root/go/bin/waybackurls
/root/go/bin/ffuf
```









