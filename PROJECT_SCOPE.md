# LifeOS Personal Assistant Bot - Project Scope

## Project Overview
Convert the existing Telegram Tarot Bot into a personal assistant bot that interacts with a PARA-style LifeOS knowledge management system stored locally.

**Current State:** Telegram bot providing AI-generated tarot readings with conversation history
**Target State:** Personal assistant for task management, note capture, and knowledge base interaction

---

## Core Requirements

### 1. LifeOS Integration
- **Database Location:** Local folder on desktop (git-enabled, not on GitHub)
- **Structure:** PARA methodology (Projects, Areas, Resources, Archives)
- **Format:** Markdown files (assumed - to be confirmed)
- **Access Method:** Direct file system access (local deployment)

### 2. Primary Features

#### Task Management
- **View Today's Tasks**
  - Display current day's task list
  - Show task status (completed/pending)
  - Support different priority levels if applicable

- **Add Tasks**
  - Text-based task creation
  - Voice note task creation (transcribed)
  - Quick capture with minimal friction
  - Assign to today or specific future dates

- **Complete Tasks**
  - Mark tasks as done
  - Update markdown checkbox status
  - Provide confirmation feedback

- **Task Operations**
  - Reschedule tasks
  - Delete tasks
  - Modify task descriptions
  - Add task metadata (priority, tags, etc.)

#### Voice Notes
- **Transcription:** Use OpenAI Whisper API or Telegram's voice-to-text
- **Processing Options:**
  - Transcribe and save as note
  - Transcribe and create task
  - Transcribe and process with AI for categorization

- **Storage:**
  - Save transcriptions in appropriate PARA category
  - Option to save audio files or just text
  - Auto-categorize based on content (using AI)

#### Knowledge Base Interaction
- **Search Functionality**
  - Full-text search across all markdown files
  - Search within specific PARA categories
  - AI-powered semantic search

- **Quick Capture**
  - Add notes/ideas to inbox or specific areas
  - Voice or text input
  - Auto-timestamp entries

- **Retrieval**
  - Get project summaries
  - View area information
  - Access resources
  - Browse archives

#### PARA Navigation
- **Browse Projects:** List active projects, view project details
- **Browse Areas:** Access different life areas
- **Browse Resources:** Search reference materials
- **Browse Archives:** Access completed/archived items

---

## Technical Architecture

### Deployment Options

#### RECOMMENDED: Local Deployment
**Pros:**
- Direct file system access to LifeOS
- No sync complexity
- Full control over data
- Simpler git operations

**Cons:**
- Desktop must be running
- No remote access (unless VPN)
- Need to handle local environment setup

**Implementation:**
- Use `polling` instead of `webhooks`
- Remove Heroku-specific code
- Run as background service on desktop
- Consider systemd/launchd for auto-start

#### Alternative: Cloud with Git Sync
**Pros:**
- Access from anywhere
- Always available

**Cons:**
- Complex git sync operations
- Security concerns with private data
- Potential merge conflicts
- Requires GitHub setup

### Technology Stack

#### Current Dependencies (Keep)
- `python-telegram-bot[webhooks]==20.3` - Telegram bot framework
- `openai==1.51.2` - AI processing
- `requests==2.26.0` - HTTP requests

#### New Dependencies Required
```
- python-telegram-bot (switch to polling mode)
- openai (for Whisper voice transcription)
- GitPython (for git operations)
- python-frontmatter (for markdown metadata parsing)
- watchdog (optional: file system monitoring)
```

#### APIs & Services
- **Telegram Bot API** - Core bot functionality
- **OpenAI API**
  - GPT-4o for natural language processing
  - Whisper for voice transcription
  - Embeddings for semantic search (optional)

### File Operations

#### Read Operations
- Parse markdown files
- Extract task lists (checkbox items)
- Read frontmatter metadata
- Search file contents

#### Write Operations
- Update task status (check/uncheck boxes)
- Append new tasks to daily files
- Create new notes/entries
- Update timestamps

#### Git Operations
- Auto-commit after changes
- Meaningful commit messages (e.g., "Added task via bot", "Completed 3 tasks")
- Optional: auto-push (if syncing to GitHub)
- Handle conflicts gracefully

---

## Data Structure Questions (To Answer When Home)

### LifeOS Structure
- [ ] What is the exact folder path?
- [ ] How are files organized? (folder per category? all in one folder?)
- [ ] Naming conventions for files?

### Daily Tasks
- [ ] File format: Single file per day? One file with all days?
- [ ] File naming: `2025-10-24.md`? `Daily/October-24.md`?
- [ ] Task format: Standard markdown checkboxes?
  ```markdown
  - [ ] Task description
  - [x] Completed task
  ```
- [ ] Task metadata: Tags, priority, time estimates?

### PARA Categories
- [ ] Folder structure for Projects/Areas/Resources/Archives?
- [ ] How to identify which category a file belongs to?
- [ ] Any metadata in frontmatter?

### Voice Notes
- [ ] Where should voice transcriptions be saved?
- [ ] Should audio files be kept or just transcriptions?
- [ ] Default category for quick captures?

---

## Feature Specifications

### Bot Commands

#### Essential Commands
```
/start - Welcome message, show main menu
/today - View today's tasks
/add [task] - Add task to today
/done [task_number] - Mark task as complete
/voice - Instructions for voice notes
/search [query] - Search knowledge base
/capture [note] - Quick capture to inbox
/help - Show all commands and usage
```

#### Advanced Commands
```
/tomorrow - View tomorrow's tasks
/week - View this week's tasks
/projects - List all active projects
/areas - List all areas
/project [name] - View specific project details
/stats - Show productivity statistics
/new - Start fresh conversation
```

### Inline Keyboards (Buttons)
- Quick actions menu (Today's Tasks, Add Task, Capture Note)
- Task list with complete buttons
- PARA category browser
- Common task templates

### Natural Language Processing
Use OpenAI to process free-form messages:
- "Add buy milk to my tasks"
- "What projects am I working on?"
- "Show me my health area notes"
- "Add this to my reading list"

AI should:
1. Understand intent
2. Extract entities (task text, categories, dates)
3. Execute appropriate function
4. Respond conversationally

---

## Implementation Phases

### Phase 1: Core Infrastructure (Week 1)
- [ ] Convert webhook to polling for local deployment
- [ ] Remove tarot-specific code
- [ ] Create LifeOS file system handler module
- [ ] Implement basic file read/write operations
- [ ] Set up git auto-commit functionality

### Phase 2: Task Management (Week 1-2)
- [ ] Implement task list parser
- [ ] Create task viewer (display today's tasks)
- [ ] Add task creation functionality
- [ ] Implement task completion
- [ ] Add task modification features

### Phase 3: Voice Integration (Week 2)
- [ ] Set up voice message handling
- [ ] Implement Whisper transcription
- [ ] Create voice-to-task workflow
- [ ] Create voice-to-note workflow
- [ ] Test transcription accuracy

### Phase 4: Knowledge Base Features (Week 3)
- [ ] Implement file search across LifeOS
- [ ] Create PARA navigation
- [ ] Build quick capture system
- [ ] Add AI-powered categorization
- [ ] Implement retrieval functions

### Phase 5: AI Enhancement (Week 3-4)
- [ ] Natural language command processing
- [ ] Smart task suggestions
- [ ] Context-aware responses
- [ ] Semantic search (embeddings)
- [ ] Summarization features

### Phase 6: Polish & Testing (Week 4)
- [ ] Error handling and edge cases
- [ ] User experience improvements
- [ ] Performance optimization
- [ ] Documentation
- [ ] Deployment setup (systemd/service)

---

## Security & Privacy Considerations

### Data Security
- All personal data stays local (recommended deployment)
- No Discord logging for personal information
- Environment variables for API keys
- Git credentials securely stored

### API Key Management
```bash
# Required environment variables
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_key
LIFEOS_PATH=/path/to/lifeos/folder
```

### Backup Strategy
- LifeOS already git-enabled
- Bot changes create automatic commits
- Consider automated backups before major operations

---

## Success Metrics

### Functionality
- [ ] Can view and manage daily tasks via Telegram
- [ ] Voice notes successfully transcribed and saved
- [ ] Can search and retrieve knowledge base content
- [ ] AI understands natural language commands
- [ ] All changes properly committed to git

### User Experience
- [ ] Response time < 2 seconds for most operations
- [ ] Intuitive command structure
- [ ] Helpful error messages
- [ ] Mobile-friendly interaction patterns

### Reliability
- [ ] Bot runs continuously on desktop
- [ ] Graceful error handling
- [ ] No data loss on failures
- [ ] Git conflicts handled properly

---

## Open Questions

1. **Daily Task File Structure:** How exactly are daily tasks organized?
2. **PARA Implementation:** Specific folder/file structure for PARA categories?
3. **Voice Storage:** Keep audio files or transcription only?
4. **Git Workflow:** Auto-commit every change or batch commits?
5. **Search Scope:** Search everything or require category specification?
6. **Task Metadata:** What additional info do tasks carry (tags, priority, etc.)?
7. **Timezone:** What timezone for "today" calculations?
8. **Inbox Location:** Where do uncategorized captures go?
9. **Discord Logging:** Keep, remove, or replace with local logging?
10. **Scheduling:** Want recurring tasks or reminders?

---

## Next Steps

1. **When Home:** Review LifeOS structure and answer open questions
2. **Confirm:** Local deployment approach
3. **Prioritize:** Which features are must-haves for v1?
4. **Begin:** Phase 1 implementation
5. **Iterate:** Build, test, refine based on actual usage

---

## Notes

- Current bot uses GPT-4o - continue using for consistency
- Conversation history feature from tarot bot can be repurposed for context-aware assistance
- Existing message splitting logic useful for long search results
- Consider keeping version number system for tracking updates
