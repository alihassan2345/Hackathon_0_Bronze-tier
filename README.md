# Personal AI Employee – Bronze Tier Implementation

**Project Title:** Autonomous Digital FTE (Full-Time Equivalent) – Bronze Tier  
**Hackathon:** Personal AI Employee Hackathon 0 (Panaversity, 2026)  
**Author:** Ali  
**Date:** February 2026  
**Status:** Bronze Tier – Minimum Viable Deliverable (Complete)

## Project Overview

This project implements the **Bronze Tier** of the Personal AI Employee hackathon challenge.  
The goal is to build a local-first, agent-driven system that acts as a proactive digital assistant (Digital FTE) using file-based task management.

Key features achieved:
- File system watcher that detects new files dropped in an `Inbox/` folder
- Automatic creation of metadata `.md` files in `Needs_Action/` for processing
- LLM-based agent (using Qwen CLI) that reads pending `.md` tasks
- Generates simple plan documents (`Plan_*.md`)
- Provides commands to move completed tasks to `Done/`
- Updates a central `Dashboard.md` file with activity logs

All operations are performed manually via CLI (no external MCP servers or full automation in Bronze tier).

## Architecture

```
AI_Employee_Vault/
├── Inbox/                  # Place files here for processing
├── Needs_Action/           # Watcher creates metadata .md files here
├── Done/                   # Completed task metadata files are moved here
├── Dashboard.md            # Central status and activity log
├── Company_Handbook.md     # Rules and guidelines for the agent
├── SKILLS.md               # Defined agent skills documentation
├── agent_prompt.txt        # Base prompt for the Qwen CLI agent
├── filesystem_watcher.py   # Python watcher script using watchdog
└── README.md               # This file
```

### Core Workflow

1. Drop any file (txt, pdf, jpg, etc.) into `Inbox/`
2. `filesystem_watcher.py` detects it and creates a metadata file in `Needs_Action/` (e.g., `FILE_example.txt.md`)
3. Run Qwen CLI with the prompt from `agent_prompt.txt`
4. Agent lists pending `.md` tasks → reads one → generates `Plan_*.md` → suggests `mv` command
5. Manually run the `mv` command to move `.md` file to `Done/`
6. Manually append activity lines to `Dashboard.md`

## Tech Stack

- **Language / Runtime**:
  - Python 3.13+ (for watcher)
  - Qwen CLI (or any compatible local LLM CLI tool)
- **Libraries**:
  - `watchdog` – for file system monitoring
- **Editor / IDE**:
  - Visual Studio Code (folder-based management instead of Obsidian)
- **No external dependencies**:
  - No MCP servers
  - No cloud APIs
  - No Git sync in Bronze tier

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd AI_Employee_Vault
   ```

2. Install Python dependencies:
   ```bash
   pip install watchdog
   ```

3. (Optional) Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate       # Windows
   ```

4. Start the file watcher (in a separate terminal):
   ```bash
   python filesystem_watcher.py
   ```

5. Drop test files into `Inbox/` folder to generate tasks.

6. Run the agent (example using Qwen CLI):
   ```bash
   cat agent_prompt.txt | qwen
   ```
   (Replace `qwen` with your actual LLM CLI command)

7. Follow the agent's output:
   - Copy-paste `Plan_*.md` content into a new file
   - Run the suggested `mv` command
   - Append activity lines to `Dashboard.md`

## Features Implemented (Bronze Tier Requirements)

- [x] Obsidian-style vault replaced with VS Code folder structure
- [x] Basic folder structure: `Inbox` / `Needs_Action` / `Done`
- [x] `Dashboard.md` and `Company_Handbook.md`
- [x] One working Watcher script (file system monitoring)
- [x] LLM (Qwen) reads from and suggests writes to the folder structure
- [x] All AI functionality described as Agent Skills (in `SKILLS.md`)
- [x] Human-in-the-loop: manual execution of `mv` commands and file creation

## Limitations (Bronze Tier)

- No automatic file moving or writing (human must run commands)
- No Ralph Wiggum-style autonomous loop (manual prompt execution)
- Only file-drop watcher implemented (no Gmail/WhatsApp yet)
- Dashboard updates are manual (copy-paste)

## Next Steps (Silver / Gold Tier)

- [ ] Add Gmail watcher
- [ ] Implement email sending via MCP
- [ ] Add cron scheduling for periodic checks
- [ ] Build full Ralph Wiggum loop with Qwen
- [ ] Integrate social media posting

## License

MIT License (or choose your preferred license)

---

**Last updated:** February 18, 2026  
**Built as part of:** Panaversity Personal AI Employee Hackathon 0
