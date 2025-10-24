# LifeOS Bot - Implementation Checklist

Quick reference for implementing the LifeOS Personal Assistant Bot.

---

## Pre-Implementation (When Home)

### Information to Gather

- [ ] LifeOS folder absolute path
- [ ] PARA folder structure (Projects, Areas, Resources, Archives locations)
- [ ] Daily tasks file format and location
- [ ] Task syntax (checkbox format, metadata, tags)
- [ ] Frontmatter usage (if any)
- [ ] Date format used in filenames
- [ ] Inbox/quick capture location
- [ ] Preferred voice note storage location

### Example to Document

```
LifeOS Structure:
/Users/username/Desktop/LifeOS/
├── 1. Projects/
│   ├── Project A/
│   └── Project B/
├── 2. Areas/
│   ├── Health/
│   └── Finance/
├── 3. Resources/
│   └── Reading List/
├── 4. Archives/
└── Daily/
    ├── 2025-10-24.md
    └── 2025-10-25.md

Daily Task File Format:
# 2025-10-24

## Tasks
- [ ] Task 1
- [x] Completed task
- [ ] Task with #tag

## Notes
...
```

---

## Phase 1: Core Infrastructure

### 1.1 Environment Setup

- [ ] Update `requirements.txt` with new dependencies
  ```
  python-telegram-bot
  openai
  GitPython
  python-dotenv
  python-frontmatter (if needed)
  pathlib
  ```

- [ ] Create `.env` file
  ```bash
  TELEGRAM_TOKEN=
  OPENAI_API_KEY=
  LIFEOS_PATH=/path/to/lifeos
  TIMEZONE=
  ```

- [ ] Create `config.py` for configuration management

- [ ] Install dependencies: `pip install -r requirements.txt`

### 1.2 Convert Webhook to Polling

- [ ] Remove webhook setup code from `main()`
- [ ] Replace `application.run_webhook()` with `application.run_polling()`
- [ ] Remove Heroku-specific environment variables
- [ ] Remove `WEBHOOK_URL` and `HEROKU_APP_NAME` references

```python
# Replace webhook code with:
application.run_polling(allowed_updates=Update.ALL_TYPES)
```

### 1.3 Remove Tarot Code

- [ ] Delete `tarotsystem_prompt` variable
- [ ] Remove `handle_tarot_reading()` function
- [ ] Remove "Tarot Reading" button from menu
- [ ] Update welcome messages
- [ ] Remove tarot-specific conversation context

### 1.4 Remove Discord Logging

- [ ] Delete `send_discord_message()` function
- [ ] Remove all calls to `send_discord_message()`
- [ ] Remove `DISCORD_WEBHOOK_URL` environment variable
- [ ] Add local logging if desired

### 1.5 Create LifeOS Manager Module

- [ ] Create `lifeos_manager.py`
- [ ] Implement `LifeOSManager` class
  - [ ] `__init__(base_path)`
  - [ ] `read_file(file_path)`
  - [ ] `write_file(file_path, content)`
  - [ ] `append_to_file(file_path, content)`
  - [ ] `list_files_in_category(category)`
  - [ ] `search_all(query)`

- [ ] Test file operations with your actual LifeOS structure

### 1.6 Git Integration

- [ ] Create `git_manager.py`
- [ ] Implement auto-commit functionality
  ```python
  def commit_changes(message, files=None)
  def generate_commit_message(action, details)
  ```
- [ ] Test git operations on dummy files first
- [ ] Add error handling for git conflicts

---

## Phase 2: Task Management

### 2.1 Create Task Manager Module

- [ ] Create `task_manager.py`
- [ ] Define `Task` class
  ```python
  class Task:
      text: str
      completed: bool
      line_number: int
      metadata: dict
  ```

### 2.2 Task Parser

- [ ] Implement `parse_tasks_from_file(file_path)`
- [ ] Create regex pattern for markdown checkboxes
- [ ] Handle edge cases (empty files, no tasks, etc.)
- [ ] Test with your actual daily task files

### 2.3 Task CRUD Operations

- [ ] Implement `get_tasks_for_date(date)`
- [ ] Implement `get_today_tasks()`
- [ ] Implement `add_task(task_text, date)`
- [ ] Implement `complete_task(task_index, date)`
- [ ] Implement `update_task(task_index, new_text, date)`
- [ ] Implement `delete_task(task_index, date)`

### 2.4 Bot Commands for Tasks

- [ ] Create `/today` command handler
  - [ ] Fetch today's tasks
  - [ ] Format as numbered list
  - [ ] Show completion status
  - [ ] Handle empty task list

- [ ] Create `/add` command handler
  - [ ] Parse task text from command args
  - [ ] Add to today's file
  - [ ] Commit to git
  - [ ] Send confirmation

- [ ] Create `/done` command handler
  - [ ] Parse task number
  - [ ] Mark as complete
  - [ ] Commit to git
  - [ ] Send confirmation

- [ ] Update main menu buttons
  - [ ] "Today's Tasks" button
  - [ ] "Add Task" button
  - [ ] Keep Help button

### 2.5 Testing

- [ ] Test viewing empty task list
- [ ] Test adding tasks
- [ ] Test completing tasks
- [ ] Test edge cases (invalid task numbers, etc.)
- [ ] Verify git commits are created

---

## Phase 3: Voice Integration

### 3.1 Voice Handler Module

- [ ] Create `voice_handler.py`
- [ ] Implement `VoiceHandler` class
  - [ ] `download_voice_note(telegram_file)`
  - [ ] `transcribe_audio(audio_data)`
  - [ ] `process_voice_note(audio_data)`
  - [ ] `save_voice_note(transcription, category)`

### 3.2 Whisper Integration

- [ ] Set up OpenAI Whisper API calls
  ```python
  response = client.audio.transcriptions.create(
      model="whisper-1",
      file=audio_file
  )
  ```
- [ ] Test with sample voice messages
- [ ] Handle API errors gracefully

### 3.3 Voice Message Handler

- [ ] Add voice message handler to bot
  ```python
  application.add_handler(MessageHandler(filters.VOICE, handle_voice))
  ```
- [ ] Implement `handle_voice()` function
  - [ ] Download voice file
  - [ ] Show "transcribing..." message
  - [ ] Transcribe with Whisper
  - [ ] Process transcription (task vs note)
  - [ ] Save to LifeOS
  - [ ] Update message with result

### 3.4 Voice Processing Options

- [ ] Implement intent detection for voice notes
  - [ ] Is this a task? (keywords: "add", "remind me", "todo")
  - [ ] Is this a note? (keywords: "note", "remember", "idea")
  - [ ] Default behavior if unclear

- [ ] Add user confirmation for ambiguous voice notes
  - [ ] "Did you mean to add this as a task or a note?"
  - [ ] Inline keyboard with options

### 3.5 Testing

- [ ] Test with various voice notes
- [ ] Test task-like voice notes
- [ ] Test note-like voice notes
- [ ] Test transcription accuracy
- [ ] Test save locations

---

## Phase 4: Knowledge Base Features

### 4.1 Search Implementation

- [ ] Implement basic text search
  ```python
  def search_all(query):
      results = []
      for file in all_markdown_files:
          if query in read_file(file):
              results.append(SearchResult(...))
      return results
  ```

- [ ] Add search command handler `/search <query>`
- [ ] Format search results for Telegram
- [ ] Add result limits (top 5-10)
- [ ] Highlight matched context

### 4.2 PARA Navigation

- [ ] Implement `/projects` command (list all projects)
- [ ] Implement `/areas` command (list all areas)
- [ ] Implement `/project <name>` (show project details)
- [ ] Implement `/area <name>` (show area details)

- [ ] Create inline keyboard navigation
  - [ ] Browse Projects → Select project → View files
  - [ ] Browse Areas → Select area → View files

### 4.3 Quick Capture

- [ ] Implement `/capture` command
  - [ ] Takes text input
  - [ ] Saves to inbox location
  - [ ] Timestamps entry
  - [ ] Commits to git

- [ ] Add voice note → quick capture option
  - [ ] Transcribe
  - [ ] Save to inbox with timestamp
  - [ ] Tag as "from voice"

### 4.4 Testing

- [ ] Test search across all files
- [ ] Test PARA navigation
- [ ] Test quick capture (text and voice)
- [ ] Verify proper file locations
- [ ] Verify git commits

---

## Phase 5: AI Enhancement

### 5.1 AI Processor Module

- [ ] Create `ai_processor.py`
- [ ] Implement natural language command processing
  ```python
  def process_natural_language_command(user_input, context):
      # Use GPT-4o to understand intent
      # Extract entities (task text, dates, categories)
      # Return structured data
  ```

### 5.2 Natural Language Handler

- [ ] Update `handle_message()` to use AI processor
- [ ] Parse user intent from free-form text
- [ ] Execute appropriate actions
- [ ] Respond conversationally

Examples:
- "Add buy milk to tomorrow" → Add task for tomorrow
- "What projects am I working on?" → List projects
- "Show me health notes" → Search in Health area

### 5.3 AI Features

- [ ] Implement note categorization
  - [ ] Determine which PARA category
  - [ ] Suggest tags

- [ ] Implement task breakdown
  - [ ] Complex task → suggest subtasks
  - [ ] Estimate effort

- [ ] Implement smart search
  - [ ] Understand synonyms
  - [ ] Related topics

### 5.4 Testing

- [ ] Test various natural language inputs
- [ ] Test edge cases and unclear inputs
- [ ] Verify AI categorization accuracy
- [ ] Test conversation flow

---

## Phase 6: Polish & Documentation

### 6.1 Error Handling

- [ ] Add try-catch blocks to all file operations
- [ ] Add try-catch blocks to all API calls
- [ ] Create user-friendly error messages
- [ ] Log errors for debugging

### 6.2 Help System

- [ ] Create comprehensive `/help` command
- [ ] List all available commands
- [ ] Provide usage examples
- [ ] Create command cheat sheet

### 6.3 User Experience

- [ ] Add loading messages for long operations
- [ ] Add confirmation messages for all actions
- [ ] Use emojis for visual clarity
- [ ] Format long messages properly (split if needed)

### 6.4 Testing

- [ ] Complete end-to-end testing
- [ ] Test all commands
- [ ] Test all voice features
- [ ] Test error scenarios
- [ ] Test with real daily usage

### 6.5 Documentation

- [ ] Update README.md
  - [ ] Project description
  - [ ] Setup instructions
  - [ ] Command reference
  - [ ] Troubleshooting

- [ ] Create USER_GUIDE.md
  - [ ] Getting started
  - [ ] Daily workflow examples
  - [ ] Tips and tricks

- [ ] Document code
  - [ ] Docstrings for all functions
  - [ ] Comments for complex logic
  - [ ] Type hints where appropriate

### 6.6 Deployment Setup

- [ ] Create systemd service file (Linux) or launchd plist (Mac)
- [ ] Set up auto-start on boot
- [ ] Configure logging
- [ ] Test restart/crash recovery

---

## Testing Checklist

### Functional Tests

- [ ] **Task Management**
  - [ ] View today's tasks
  - [ ] Add task via command
  - [ ] Complete task
  - [ ] Add task for future date
  - [ ] Handle empty task list
  - [ ] Handle invalid task numbers

- [ ] **Voice Notes**
  - [ ] Transcribe voice message
  - [ ] Voice → task
  - [ ] Voice → note
  - [ ] Voice → quick capture
  - [ ] Handle poor audio quality

- [ ] **Search & Navigation**
  - [ ] Search all files
  - [ ] Search specific category
  - [ ] Browse projects
  - [ ] Browse areas
  - [ ] View file contents

- [ ] **AI Processing**
  - [ ] Natural language task creation
  - [ ] Natural language search
  - [ ] Note categorization
  - [ ] Intent detection

- [ ] **Git Integration**
  - [ ] Commits created after task operations
  - [ ] Commit messages are descriptive
  - [ ] No conflicts with manual edits
  - [ ] Proper file tracking

### Error Scenarios

- [ ] File not found
- [ ] Permission denied
- [ ] OpenAI API failure
- [ ] Invalid command syntax
- [ ] Git conflicts
- [ ] Network issues

### Edge Cases

- [ ] Empty LifeOS folder
- [ ] No tasks for today
- [ ] Very long task descriptions
- [ ] Special characters in tasks
- [ ] Concurrent edits (bot + manual)

---

## Launch Checklist

### Pre-Launch

- [ ] All environment variables set
- [ ] LIFEOS_PATH is correct
- [ ] Telegram token is valid
- [ ] OpenAI API key is valid
- [ ] All dependencies installed
- [ ] Configuration validated
- [ ] Test bot with `/start` command

### Monitoring

- [ ] Set up logging
- [ ] Monitor error rates
- [ ] Track API usage (OpenAI costs)
- [ ] Watch git commit history

### Backup Plan

- [ ] Backup LifeOS before first use
- [ ] Test restore procedure
- [ ] Document rollback steps
- [ ] Keep old tarot bot code just in case

---

## Future Enhancements (Post-Launch)

### Short Term
- [ ] Inline task editing
- [ ] Task rescheduling
- [ ] Bulk task operations
- [ ] Task templates
- [ ] Better formatting options

### Medium Term
- [ ] Weekly/monthly task views
- [ ] Recurring tasks
- [ ] Reminders/notifications
- [ ] Calendar integration
- [ ] Statistics dashboard

### Long Term
- [ ] Multi-user support (family)
- [ ] Web interface
- [ ] Mobile app
- [ ] Email integration
- [ ] Meeting notes automation
- [ ] Smart scheduling

---

## Key Decisions to Make

Before starting implementation, decide:

1. **Deployment:** Local only or eventually cloud?
2. **Voice Storage:** Audio files or transcription only?
3. **Git Strategy:** Immediate commits or batched?
4. **Search Method:** Simple grep or indexed search?
5. **AI Usage:** Where to use AI vs. simple parsing?
6. **Error Handling:** How verbose? Retry logic?
7. **Logging:** How much? Where stored?
8. **Task Metadata:** What additional info to support?

---

## Resources & References

### Documentation
- [python-telegram-bot](https://docs.python-telegram-bot.org/)
- [OpenAI API](https://platform.openai.com/docs/)
- [GitPython](https://gitpython.readthedocs.io/)

### Code Examples
- Current bot: `/home/user/telegramtarot/bot.py`
- Planning docs: `PROJECT_SCOPE.md`, `TECHNICAL_OVERVIEW.md`

### Support
- Telegram Bot API: https://core.telegram.org/bots/api
- OpenAI Community: https://community.openai.com/

---

## Progress Tracking

Update this section as you complete phases:

- [x] Phase 0: Planning & Documentation
- [ ] Phase 1: Core Infrastructure
- [ ] Phase 2: Task Management
- [ ] Phase 3: Voice Integration
- [ ] Phase 4: Knowledge Base Features
- [ ] Phase 5: AI Enhancement
- [ ] Phase 6: Polish & Documentation

**Started:** 2025-10-24
**Target Completion:** TBD
**Current Status:** Awaiting LifeOS structure review

---

## Notes

- Keep this checklist updated as you work
- Check off items as they're completed
- Add notes about challenges or decisions made
- Use git commits to track progress
- Don't hesitate to refactor if needed

Good luck building your LifeOS Personal Assistant Bot! 🚀
