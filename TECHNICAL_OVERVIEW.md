# LifeOS Personal Assistant Bot - Technical Overview

## Architecture Design

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                      Telegram User                           │
└───────────────────────┬─────────────────────────────────────┘
                        │ (Messages, Voice Notes, Commands)
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                   Telegram Bot API                           │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────────┐
│                  Bot Application (bot.py)                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Command Handlers                                      │   │
│  │  - /today, /add, /done, /search, etc.                │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Message Processors                                    │   │
│  │  - Text messages, Voice notes                        │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ AI Integration Layer                                  │   │
│  │  - OpenAI GPT-4o (NLP, understanding)               │   │
│  │  - OpenAI Whisper (Voice transcription)             │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────────┐
│              LifeOS Manager Module (lifeos.py)               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ File System Handler                                   │   │
│  │  - Read markdown files                               │   │
│  │  - Write/update markdown files                       │   │
│  │  - Parse frontmatter metadata                        │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Task Manager                                          │   │
│  │  - Parse task lists from markdown                    │   │
│  │  - Update task status                                │   │
│  │  - Create new tasks                                  │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Search Engine                                         │   │
│  │  - Full-text search                                  │   │
│  │  - Semantic search (optional)                        │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Git Integration                                       │   │
│  │  - Auto-commit changes                               │   │
│  │  - Generate commit messages                          │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────────┐
│              Local LifeOS File System                        │
│                                                               │
│  Projects/                                                    │
│  Areas/                                                       │
│  Resources/                                                   │
│  Archives/                                                    │
│  Daily/ (or equivalent task storage)                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Module Structure

### Proposed File Organization

```
telegramtarot/
├── bot.py                    # Main bot application (refactored)
├── lifeos_manager.py         # NEW: LifeOS file system operations
├── task_manager.py           # NEW: Task-specific operations
├── ai_processor.py           # NEW: AI/NLP processing
├── voice_handler.py          # NEW: Voice transcription
├── config.py                 # NEW: Configuration management
├── utils.py                  # NEW: Utility functions
├── requirements.txt          # Updated dependencies
├── .env                      # Environment variables
├── README.md                 # Updated documentation
├── PROJECT_SCOPE.md          # This planning document
├── TECHNICAL_OVERVIEW.md     # This technical document
└── tests/                    # NEW: Test suite
    ├── test_lifeos.py
    ├── test_tasks.py
    └── test_bot.py
```

---

## Detailed Component Specifications

### 1. LifeOS Manager (`lifeos_manager.py`)

#### Purpose
Central module for all LifeOS file system interactions.

#### Key Classes

```python
class LifeOSManager:
    def __init__(self, base_path: str):
        """Initialize with LifeOS root directory."""
        self.base_path = Path(base_path)
        self.projects_path = self.base_path / "Projects"
        self.areas_path = self.base_path / "Areas"
        self.resources_path = self.base_path / "Resources"
        self.archives_path = self.base_path / "Archives"
        # Path to daily tasks (TBD based on actual structure)
        self.daily_path = self.base_path / "Daily"

    # File Operations
    def read_file(self, file_path: str) -> str:
        """Read markdown file content."""
        pass

    def write_file(self, file_path: str, content: str):
        """Write content to markdown file."""
        pass

    def append_to_file(self, file_path: str, content: str):
        """Append content to existing file."""
        pass

    # PARA Navigation
    def list_projects(self) -> List[str]:
        """Get all project names."""
        pass

    def list_areas(self) -> List[str]:
        """Get all area names."""
        pass

    def get_project_files(self, project_name: str) -> List[Path]:
        """Get all files in a project."""
        pass

    # Search
    def search_all(self, query: str) -> List[SearchResult]:
        """Search across all markdown files."""
        pass

    def search_in_category(self, category: str, query: str) -> List[SearchResult]:
        """Search within specific PARA category."""
        pass
```

#### Key Methods

**File Discovery:**
- Recursively scan LifeOS directory
- Identify markdown files
- Parse frontmatter metadata
- Build file index for fast access

**Search Implementation:**
- Option 1: Simple grep-style text search
- Option 2: Build search index (using whoosh or similar)
- Option 3: Semantic search using OpenAI embeddings

**PARA Navigation:**
- Detect which files belong to which category
- Support nested folder structures
- Handle special files (indexes, templates, etc.)

---

### 2. Task Manager (`task_manager.py`)

#### Purpose
Handle all task-related operations (CRUD for tasks).

#### Key Classes

```python
class Task:
    def __init__(self, text: str, completed: bool = False,
                 line_number: int = None, metadata: dict = None):
        self.text = text
        self.completed = completed
        self.line_number = line_number  # Track position in file
        self.metadata = metadata or {}  # Tags, priority, etc.

    def to_markdown(self) -> str:
        """Convert to markdown checkbox format."""
        checkbox = "[x]" if self.completed else "[ ]"
        return f"- {checkbox} {self.text}"

class TaskManager:
    def __init__(self, lifeos: LifeOSManager):
        self.lifeos = lifeos

    # Read Operations
    def get_tasks_for_date(self, date: datetime) -> List[Task]:
        """Get all tasks for a specific date."""
        pass

    def get_today_tasks(self) -> List[Task]:
        """Get today's tasks."""
        return self.get_tasks_for_date(datetime.now())

    def parse_tasks_from_file(self, file_path: str) -> List[Task]:
        """Extract tasks from markdown file."""
        # Regex to find: - [ ] or - [x] followed by task text
        pass

    # Write Operations
    def add_task(self, task_text: str, date: datetime = None):
        """Add new task to specified date (default today)."""
        pass

    def complete_task(self, task_index: int, date: datetime = None):
        """Mark task as complete."""
        pass

    def update_task(self, task_index: int, new_text: str, date: datetime = None):
        """Update task description."""
        pass

    def delete_task(self, task_index: int, date: datetime = None):
        """Remove task from list."""
        pass

    # Git Integration
    def commit_task_changes(self, action: str, task_text: str):
        """Commit task changes with descriptive message."""
        message = f"Bot: {action} task - {task_text[:50]}"
        # Use GitPython to commit
        pass
```

#### Task Parsing Strategy

**Markdown Checkbox Format:**
```markdown
## Tasks for 2025-10-24

- [ ] Incomplete task
- [x] Completed task
- [ ] Task with #tag and @context
- [ ] High priority task ⭐
```

**Regex Pattern:**
```python
import re
TASK_PATTERN = r'^- \[([ x])\] (.+)$'

def parse_task_line(line: str) -> Task:
    match = re.match(TASK_PATTERN, line)
    if match:
        completed = match.group(1) == 'x'
        text = match.group(2)
        return Task(text=text, completed=completed)
    return None
```

**Metadata Extraction:**
- Tags: `#work`, `#personal`
- Contexts: `@home`, `@computer`
- Priority: `⭐`, `!!`, `[P1]`
- Time estimates: `[30m]`, `[2h]`

---

### 3. AI Processor (`ai_processor.py`)

#### Purpose
Handle all OpenAI interactions for NLP and understanding.

#### Key Functions

```python
class AIProcessor:
    def __init__(self, openai_client: OpenAI):
        self.client = openai_client

    def process_natural_language_command(self, user_input: str,
                                        context: dict) -> dict:
        """
        Understand user intent and extract entities.

        Returns:
        {
            'intent': 'add_task' | 'view_tasks' | 'search' | 'capture_note',
            'entities': {
                'task_text': '...',
                'date': '...',
                'category': '...',
                'tags': [...]
            },
            'confidence': 0.95
        }
        """
        pass

    def categorize_note(self, note_text: str) -> str:
        """
        Determine which PARA category a note belongs to.
        Returns: 'Projects', 'Areas', 'Resources', or 'Archives'
        """
        pass

    def summarize_project(self, project_files: List[str]) -> str:
        """Generate AI summary of project from multiple files."""
        pass

    def suggest_task_improvements(self, task_text: str) -> str:
        """Suggest better task phrasing or breakdown."""
        pass
```

#### Natural Language Processing Flow

```
User: "Add buy milk and eggs to my shopping list tomorrow"
       ↓
AI Processing:
  - Intent: add_task
  - Task text: "buy milk and eggs"
  - Context: shopping list
  - Date: tomorrow
       ↓
Task Manager:
  - Create task for tomorrow's date
  - Add tag: #shopping
       ↓
Response: "Added 'buy milk and eggs' to your shopping list for tomorrow"
```

---

### 4. Voice Handler (`voice_handler.py`)

#### Purpose
Process voice messages and transcribe to text.

#### Implementation

```python
class VoiceHandler:
    def __init__(self, openai_client: OpenAI, lifeos: LifeOSManager):
        self.client = openai_client
        self.lifeos = lifeos

    async def download_voice_note(self, telegram_file) -> bytes:
        """Download voice note from Telegram."""
        pass

    def transcribe_audio(self, audio_data: bytes) -> str:
        """
        Use OpenAI Whisper API to transcribe audio.
        """
        # OpenAI Whisper transcription
        response = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_data
        )
        return response.text

    def process_voice_note(self, audio_data: bytes,
                          save_audio: bool = False) -> dict:
        """
        Full voice note processing pipeline.

        Returns:
        {
            'transcription': '...',
            'intent': 'task' | 'note' | 'search',
            'processed': True/False
        }
        """
        # 1. Transcribe
        transcription = self.transcribe_audio(audio_data)

        # 2. Understand intent
        intent = self._determine_intent(transcription)

        # 3. Process accordingly
        if intent == 'task':
            # Add as task
            pass
        elif intent == 'note':
            # Save as note
            pass

        return {
            'transcription': transcription,
            'intent': intent,
            'processed': True
        }

    def save_voice_note(self, transcription: str,
                       audio_data: bytes = None,
                       category: str = 'Inbox'):
        """Save voice note to appropriate location in LifeOS."""
        pass
```

#### Voice Note Workflow Options

**Option 1: Auto-categorize**
```
Voice Note → Transcribe → AI Categorize → Save to appropriate PARA category
```

**Option 2: Ask user**
```
Voice Note → Transcribe → "Is this a task or a note?" → Save accordingly
```

**Option 3: Default to Inbox**
```
Voice Note → Transcribe → Save to Inbox → User can process later
```

---

### 5. Git Integration

#### Auto-commit Strategy

```python
from git import Repo

class GitManager:
    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)

    def commit_changes(self, message: str, files: List[str] = None):
        """
        Commit specified files or all changes.
        """
        if files:
            self.repo.index.add(files)
        else:
            self.repo.index.add('*')

        self.repo.index.commit(message)

    def generate_commit_message(self, action: str, details: str) -> str:
        """
        Generate descriptive commit messages.

        Examples:
        - "Bot: Added task - Buy groceries"
        - "Bot: Completed 3 tasks on 2025-10-24"
        - "Bot: Added voice note to Health area"
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        return f"Bot [{timestamp}]: {action} - {details}"
```

#### Commit Timing Options

1. **Immediate:** Commit after every change
   - Pro: Never lose data
   - Con: Messy git history

2. **Batched:** Commit every N changes or every X minutes
   - Pro: Cleaner history
   - Con: Risk of losing changes if bot crashes

3. **Session-based:** Commit when user ends session
   - Pro: Logical grouping
   - Con: Long-running sessions create large commits

**Recommendation:** Immediate commits with well-formatted messages.

---

## Bot Command Handlers

### Command Structure

```python
# In bot.py

async def cmd_today(update: Update, context: CallbackContext):
    """Show today's tasks."""
    task_manager = context.bot_data['task_manager']
    tasks = task_manager.get_today_tasks()

    if not tasks:
        await update.message.reply_text("No tasks for today! 🎉")
        return

    # Format task list
    message = "📋 Today's Tasks:\n\n"
    for i, task in enumerate(tasks, 1):
        checkbox = "✅" if task.completed else "⬜"
        message += f"{i}. {checkbox} {task.text}\n"

    await update.message.reply_text(message)

async def cmd_add(update: Update, context: CallbackContext):
    """Add a task: /add Task description here"""
    if not context.args:
        await update.message.reply_text(
            "Usage: /add <task description>\n"
            "Example: /add Buy groceries"
        )
        return

    task_text = ' '.join(context.args)
    task_manager = context.bot_data['task_manager']
    task_manager.add_task(task_text)

    await update.message.reply_text(f"✅ Added task: {task_text}")

async def cmd_done(update: Update, context: CallbackContext):
    """Complete a task: /done 1"""
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "Usage: /done <task number>\n"
            "Example: /done 1"
        )
        return

    task_index = int(context.args[0]) - 1  # Convert to 0-indexed
    task_manager = context.bot_data['task_manager']

    try:
        task = task_manager.complete_task(task_index)
        await update.message.reply_text(f"✅ Completed: {task.text}")
    except IndexError:
        await update.message.reply_text("Task number not found!")

async def cmd_search(update: Update, context: CallbackContext):
    """Search knowledge base: /search query"""
    if not context.args:
        await update.message.reply_text("Usage: /search <query>")
        return

    query = ' '.join(context.args)
    lifeos = context.bot_data['lifeos_manager']
    results = lifeos.search_all(query)

    if not results:
        await update.message.reply_text(f"No results found for '{query}'")
        return

    # Format search results
    message = f"🔍 Search results for '{query}':\n\n"
    for result in results[:5]:  # Limit to top 5
        message += f"📄 {result.file_name}\n"
        message += f"   {result.snippet}\n\n"

    await update.message.reply_text(message)

async def handle_voice(update: Update, context: CallbackContext):
    """Handle voice messages."""
    voice_handler = context.bot_data['voice_handler']

    # Download voice file
    voice_file = await update.message.voice.get_file()
    audio_data = await voice_file.download_as_bytearray()

    # Show processing message
    processing_msg = await update.message.reply_text("🎤 Transcribing...")

    # Process voice note
    result = voice_handler.process_voice_note(bytes(audio_data))

    # Update message with transcription
    await processing_msg.edit_text(
        f"📝 Transcription:\n{result['transcription']}\n\n"
        f"Saved to LifeOS!"
    )
```

---

## Configuration Management

### Environment Variables

```bash
# .env file
TELEGRAM_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
LIFEOS_PATH=/Users/username/Desktop/LifeOS
TIMEZONE=America/New_York

# Optional
AUTO_COMMIT=true
COMMIT_BATCH_SIZE=5
VOICE_SAVE_AUDIO=false
DEFAULT_INBOX_PATH=Inbox/QuickCaptures.md
```

### Configuration File

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # LifeOS
    LIFEOS_PATH = os.getenv('LIFEOS_PATH')
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')

    # Features
    AUTO_COMMIT = os.getenv('AUTO_COMMIT', 'true').lower() == 'true'
    VOICE_SAVE_AUDIO = os.getenv('VOICE_SAVE_AUDIO', 'false').lower() == 'true'

    # Paths (to be confirmed with actual structure)
    DAILY_TASKS_PATH = 'Daily'
    INBOX_PATH = 'Inbox/QuickCaptures.md'

    @classmethod
    def validate(cls):
        """Ensure all required config is present."""
        required = ['TELEGRAM_TOKEN', 'OPENAI_API_KEY', 'LIFEOS_PATH']
        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")
```

---

## Error Handling Strategy

### Common Errors

1. **File Not Found**
   - Daily task file doesn't exist yet
   - Solution: Create file with template

2. **Git Conflicts**
   - User edited LifeOS while bot was processing
   - Solution: Detect conflicts, notify user, ask for resolution

3. **API Failures**
   - OpenAI API down or rate limited
   - Solution: Graceful degradation, queue messages

4. **Permission Errors**
   - Can't write to LifeOS directory
   - Solution: Clear error message, check permissions

### Error Response Examples

```python
try:
    tasks = task_manager.get_today_tasks()
except FileNotFoundError:
    # Create today's task file
    task_manager.create_daily_file(datetime.now())
    tasks = []
except PermissionError:
    await update.message.reply_text(
        "❌ Can't access LifeOS directory. Please check permissions."
    )
    return
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    await update.message.reply_text(
        "❌ Something went wrong. Please try again."
    )
    return
```

---

## Performance Considerations

### File System Access
- Cache file list to avoid repeated directory scans
- Use file watchers to detect external changes
- Index files for faster search

### API Rate Limits
- OpenAI Whisper: 50 requests/minute
- OpenAI GPT-4o: Depends on tier
- Implement rate limiting and queuing

### Response Time Targets
- Simple commands (view tasks): < 1 second
- Voice transcription: < 5 seconds
- Search operations: < 3 seconds
- AI processing: < 5 seconds

---

## Testing Strategy

### Unit Tests
```python
# tests/test_task_manager.py
def test_parse_task_line():
    line = "- [ ] Buy groceries"
    task = parse_task_line(line)
    assert task.text == "Buy groceries"
    assert task.completed == False

def test_complete_task():
    # Test task completion
    pass

# tests/test_lifeos.py
def test_search_files():
    # Test search functionality
    pass
```

### Integration Tests
- Test full workflows (add task → view → complete)
- Test voice note processing end-to-end
- Test git commits

### Manual Testing Checklist
- [ ] Add task via command
- [ ] Add task via voice
- [ ] Complete task
- [ ] Search knowledge base
- [ ] Navigate PARA categories
- [ ] Git commits properly created
- [ ] Error handling works

---

## Deployment Guide

### Local Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your tokens and paths

# 3. Test configuration
python -c "from config import Config; Config.validate()"

# 4. Run bot
python bot.py
```

### Running as Service (Linux/Mac)

**Option 1: systemd (Linux)**
```ini
# /etc/systemd/system/lifeos-bot.service
[Unit]
Description=LifeOS Telegram Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/telegramtarot
ExecStart=/usr/bin/python3 /path/to/telegramtarot/bot.py
Restart=always
Environment=PATH=/usr/bin:/usr/local/bin

[Install]
WantedBy=multi-user.target
```

**Option 2: launchd (Mac)**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lifeos.bot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/bot.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

---

## Migration from Current Bot

### Changes Required

1. **Remove:**
   - Tarot system prompt
   - Tarot reading generation
   - Discord webhook logging
   - Heroku webhook setup
   - "Ask a Question" button

2. **Modify:**
   - Welcome message
   - Main menu buttons
   - Version number and description
   - Conversation context (from tarot to task/life management)

3. **Add:**
   - LifeOS file system integration
   - Task management functions
   - Voice transcription
   - PARA navigation
   - Search functionality
   - Git integration

### Backward Compatibility
None needed - this is a complete transformation of purpose.

---

## Future Enhancements

### Phase 2 Features
- Recurring tasks
- Reminders/notifications
- Task templates
- Project templates
- Weekly/monthly reviews
- Statistics and insights

### Advanced AI Features
- Automatic task prioritization
- Smart scheduling suggestions
- Meeting notes extraction
- Email-to-task conversion (via forwarding)
- Voice commands ("Hey bot, what's next?")

### Integration Ideas
- Calendar sync (Google Calendar, Apple Calendar)
- Email integration
- Web clipper companion
- Mobile shortcuts
- Desktop widgets

---

## Questions for Final Implementation

1. **Date Format:** How are dates written in your system? (2025-10-24, Oct 24 2025, etc.)
2. **Daily File Name:** What's the naming convention? (daily-2025-10-24.md, 2025-10-24.md, etc.)
3. **Task Location:** Are tasks in separate daily files or one master file?
4. **Frontmatter:** Do your markdown files use YAML frontmatter?
5. **Tagging System:** Do you use hashtags, @contexts, or other metadata?
6. **Inbox:** Where do quick captures go before processing?
7. **Completed Tasks:** Archive them or keep in same file?
8. **Voice Storage:** Preferred location for voice note transcriptions?

---

## Summary

This technical overview provides the blueprint for transforming the Telegram Tarot Bot into a powerful LifeOS personal assistant. The modular architecture ensures:

- **Maintainability:** Clear separation of concerns
- **Extensibility:** Easy to add new features
- **Reliability:** Proper error handling and git integration
- **Usability:** Intuitive commands and natural language support

Next step: Review LifeOS structure when home and answer the open questions to begin Phase 1 implementation.
