


---
name: user-bin_tools Microagent
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - run nmap

# Nmap Microagent

This microagent provides a simple interface to run `nmap` scans.

## Usage

To use this microagent, trigger it with the phrase "run nmap". The agent will execute the `nmap` command and return the output.

## Example

User: run nmap
Agent: [Executes `nmap` and returns the output]

## Notes

- Ensure that `nmap` is installed on your system.
- This microagent runs `nmap` with default options. You can modify the command as needed within the agent's code.

## Command

The command run by this microagent is:
```bash
/nmap
```

---







