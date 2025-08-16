

---
name: Nmap Microagent
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - /nmap

# Nmap Microagent

## Overview
The Nmap (Network Mapper) microagent provides capabilities for network discovery and security auditing using the Nmap tool. This agent helps in scanning networks, identifying hosts and services, and detecting vulnerabilities.

## Prerequisites
- Ensure VPN is set up and configured with Tor routing enabled.

### Usage Example
\`\`\`bash
# Example command to check if Tor is running through VPN
curl --socks5 127.0.0.1:9050 https://check.torproject.org/
\`\`\`

## Capabilities
- Network scanning
- Service detection
- OS detection


---
name: Nmap Microagent
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - /nmap

# Nmap Microagent

## Overview
The Nmap (Network Mapper) microagent provides capabilities for network discovery and security auditing using the Nmap tool. This agent helps in scanning networks, identifying hosts and services, and detecting vulnerabilities.

## Prerequisites
- Ensure VPN is set up and configured with Tor routing enabled.
- Install Nmap on your system.
### Example Usage
\`\`\`bash
# Command to check if Tor is running through VPN
curl --socks5 127.0.0.1:9050 https://check.torproject.org/

# Basic Network Scan
nmap 192.168.1.0/24

# Service Detection
nmap -sV 192.168.1.1

# OS Detection
nmap -O 192.168.1.1
\`\`\`

## Capabilities
- Network scanning
- Service detection
- OS detection
- Vulnerability scanning

## Credentials and Environment Variables
No specific credentials or environment variables are required for basic usage. However, for advanced features or API integration, you might need to set up Nmap with appropriate permissions.

## Error Handling
- Ensure Nmap is installed on the system.
- Handle permission errors when scanning networks.
- Manage timeouts for large network scans.

## Usage Examples

### Basic Network Scan
\`\`\`bash
nmap 192.168.1.0/24
\`\`\`

### Service Detection
\`\`\`bash
nmap -sV 192.168.1.1
\`\`\`

### OS Detection
\`\`\`bash
nmap -O 192.168.1.1
\`\`\`

## Limitations
- Requires Nmap to be installed on the system.
- May need administrative privileges for certain scans.
- Large networks can take significant time to scan.

## Additional Resources
- [Nmap Official Documentation](https://nmap.org/docs.html)


- Vulnerability scanning

## Credentials and Environment Variables
No specific credentials or environment variables are required for basic usage. However, for advanced features or API integration, you might need to set up Nmap with appropriate permissions.

## Error Handling
- Ensure Nmap is installed on the system.
- Handle permission errors when scanning networks.
- Manage timeouts for large network scans.

## Usage Examples

### Basic Network Scan
\`\`\`bash
nmap 192.168.1.0/24
\`\`\`

### Service Detection
\`\`\`bash
nmap -sV 192.168.1.1
\`\`\`

### OS Detection
\`\`\`bash
nmap -O 192.168.1.1
\`\`\`

## Limitations
- Requires Nmap to be installed on the system.
- May need administrative privileges for certain scans.
- Large networks can take significant time to scan.

## Additional Resources
- [Nmap Official Documentation](https://nmap.org/docs.html)








