# Task List

1. ✅ Add authentication support
Implemented Basic and Bearer prompts; refactored header handling
2. ✅ Implement scan profiles
Added stealth, balanced, fast profiles with preset threads, delay, auto-calibrate
3. ✅ Add decoy requests/WAF evasion
Prompted optional decoy URL list; integrated -D flag
4. ✅ Integrate live progress bar for scan
Use rich.status spinner to indicate live progress
5. 🔄 Enhance history menu
Top-level menu to view and re-run past scans
6. ⏳ Improve custom wordlist UX
Check file existence, preview lines
7. ⏳ Validate URLs
Ensure FUZZ placeholder and valid format
8. ⏳ Add non-interactive/argument mode
Support CLI flags for scripting/CI
9. ⏳ Implement interactive output drill-down
Enable expansion of specific status codes and filtering
10. ⏳ Define plugin hook interface
Allow post-scan modules
11. ⏳ Code quality improvements
Replace input(), add type hints, catch CalledProcessError
12. ⏳ Automated test suite
Smoke tests for scan types and errors

