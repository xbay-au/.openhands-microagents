# Task List

1. ✅ Add authentication support
Implemented Basic and Bearer prompts; refactored header handling
2. 🔄 Implement scan profiles
Add stealth, balanced, fast profiles with preset threads, delay, auto-calibrate
3. ⏳ Add decoy requests/WAF evasion
Allow --decoy option to send periodic decoy requests
4. ⏳ Integrate live progress bar for scan
Show progress for ffuf run to user (spinner or tqdm) based on wordlist length
5. ⏳ Enhance history menu
Top-level menu to view past scans and re-run with modifications
6. ⏳ Improve custom wordlist UX
Check file existence, preview first/last lines before using
7. ⏳ Validate URLs
Use urllib.parse to ensure URL format and presence of FUZZ placeholder
8. ⏳ Add non-interactive/argument mode
Parse CLI flags to run without wizard for scripting/CI
9. ⏳ Implement interactive output drill-down
After summary, allow user to expand specific status codes, filter, and export subsets
10. ⏳ Define plugin hook interface
Allow chaining additional checks/modules post-scan
11. ⏳ Code quality improvements
Replace input() with console.input, fix undefined variables, add type hints, catch CalledProcessError
12. ⏳ Automated test suite
Smoke tests for each scan type and error conditions

