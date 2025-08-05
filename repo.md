

---
name: microagents
type: repo
agent: CodeActAgent
---

This repository contains the code for OpenHands MicroAgents. It has a Python backend.

## General Setup:
To set up the entire repo, including frontend and backend, run `make build`.
You don't need to do this unless the user asks you to, or if you're trying to run the entire application.

Before pushing any changes, you should ensure that any lint errors or simple test errors have been fixed.

* If you've made changes to the backend, you should run `pre-commit run --all-files --config ./dev_config/python/.pre-commit-config.yaml`

If either command fails, it may have automatically fixed some issues. You should fix any issues that weren't automatically fixed,
then re-run the command to ensure it passes.

## Repository Structure
Backend:
- Located in the `openhands` directory
- Testing:
  - All tests are in `tests/unit/test_*.py`
  - To test new code, run `poetry run pytest tests/unit/test_xxx.py` where `xxx` is the appropriate file for the current functionality
  - Write all tests with pytest

