# MEMORY.md - Your Long-Term Memory

- **ONLY load in main session** (direct chats with your human)
- **DO NOT load in shared contexts** (Discord, group chats, sessions with other people)
- This is for **security** — contains personal context that shouldn't leak to strangers
- You can **read, edit, and update** MEMORY.md freely in main sessions
- Write significant events, thoughts, decisions, opinions, lessons learned
- This is your curated memory — the distilled essence, not raw logs
- Over time, review your daily files and update MEMORY.md with what's worth keeping

## Session Continuity Issue

### Problem:
Previous session context is lost when starting a new session.

### Root Cause:
OpenClaw does not persist conversation history across sessions by default. Each session starts fresh, independent of prior ones.

### Solution:
To maintain continuity:
1. Use `MEMORY.md` for long-term persistent notes
2. Use `memory/YYYY-MM-DD.md` for daily logs
3. When you want to preserve context from a previous session, explicitly save key information to these files
4. In future sessions, read these files to recover context

This design prioritizes security and privacy — sensitive information isn't automatically retained across sessions.

### Recommendation:
For ongoing projects, regularly summarize key points in `MEMORY.md` or `memory/2026-03-04.md` so you can pick up where you left off.