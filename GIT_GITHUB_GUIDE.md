# Git & GitHub Basics - Simple Guide

A practical explanation of Git and GitHub concepts, using your bot project as an example.

---

## What is Git?

**Git** is version control software that tracks changes to your files over time.

Think of it like **Track Changes in Microsoft Word**, but way more powerful:
- Records every change you make
- Lets you go back to any previous version
- Allows multiple people to work on the same project
- Shows who changed what and when

**Git runs on your computer** - it's the underlying technology.

---

## What is GitHub?

**GitHub** is a website that hosts Git repositories (projects) online.

Think of it like **Dropbox or Google Drive for code**:
- Stores your code in the cloud
- Makes it accessible from anywhere
- Allows collaboration with others
- Provides a web interface to view your project

**GitHub is the online service** - it's where you back up and share your Git projects.

---

## Key Concepts Explained

### 1. Repository (Repo)

**What it is:** A project folder that Git is tracking.

**Your example:**
```
telegramtarot/  ← This is your repository
├── bot.py
├── PROJECT_SCOPE.md
├── FEATURES_EXPLAINER.md
└── .git/  ← Hidden folder where Git stores all the history
```

**Think of it as:** The entire project, including all its history.

---

### 2. Commit

**What it is:** A snapshot of your project at a specific moment in time.

**Your example:**
```
Commit f574d5b: "Add user-friendly features explainer for LifeOS bot"
- Added FEATURES_EXPLAINER.md
- Date: 2025-10-24
- Author: You (with Claude)
```

**Think of it as:** A save point in a video game. You can always go back to it.

**How it works:**
```
1. Make changes to files
2. "Stage" the changes (tell Git which changes to include)
3. "Commit" the changes (save the snapshot with a message)
```

**The commands you've seen:**
```bash
git add FEATURES_EXPLAINER.md    # Stage the file
git commit -m "Add features doc"  # Commit with a message
```

---

### 3. Branch

**What it is:** A parallel version of your project where you can work without affecting the main version.

**The Analogy:**
Imagine a tree:
```
        main (trunk)
         |
         |------ feature-branch (your branch)
         |         |
         |         |-- work on new feature
         |         |-- make commits
         |         |
         |         |-- eventually merge back to main
         |
```

**Your example:**
```
main branch:
  - The stable, "official" version of your bot
  - Currently has the tarot bot code

claude/convert-to-telegram-bot-011CUSqAXyxkCZtA1oR6MhYV:
  - Your working branch where we're planning the new bot
  - Has all the planning documents
  - Won't affect the main branch until you merge it
```

**Why use branches?**
- **Experiment safely** - Won't break the working code
- **Work on multiple features** - Each gets its own branch
- **Review before merging** - Can check the changes first
- **Collaborate** - Multiple people can work on different branches

**Common branch names:**
```
main or master  - The primary, stable branch
develop         - Work-in-progress branch
feature/xyz     - New feature branch
bugfix/abc      - Bug fix branch
claude/...      - Claude Code creates these automatically
```

---

### 4. Pull Request (PR)

**What it is:** A request to merge your branch into another branch (usually main).

**The Analogy:**
Like submitting homework for review before it's graded. You're saying:
> "Hey, I've done this work on my branch. Can you review it and merge it into main?"

**Your example:**
When we pushed your branch, GitHub said:
```
Create a pull request for 'claude/convert-to-telegram-bot-...' by visiting:
https://github.com/itsaaronngan/telegramtarot/pull/new/claude/...
```

**What happens in a PR:**

1. **You create the PR:**
   - Shows all your commits
   - Shows all files changed
   - You write a description of what you did

2. **Review happens:**
   - You (or others) review the changes
   - Can comment on specific lines
   - Can request changes
   - Can approve

3. **Merge happens:**
   - Once approved, you click "Merge"
   - Your branch changes get added to the main branch
   - Your work is now "official"

**Visual:**
```
Before PR:
  main:          A --- B --- C
                              \
  your-branch:                 D --- E --- F

After merging PR:
  main:          A --- B --- C --- D --- E --- F
```

---

### 5. Merge

**What it is:** Combining changes from one branch into another.

**Your example:**
When you merge your `claude/convert-to-telegram-bot...` branch into `main`:
- All your planning documents will appear in the main branch
- All your commits will become part of main's history
- The branches become unified

**Types of merges:**

**1. Fast-forward merge** (simple):
```
main:          A --- B --- C
                            \
your-branch:                 D --- E

After merge:
main:          A --- B --- C --- D --- E
```
Main just "catches up" to your branch.

**2. Merge commit** (creates a new commit):
```
main:          A --- B --- C ------- M
                            \       /
your-branch:                 D --- E
```
Creates a new merge commit (M) that combines both branches.

**3. Rebase** (rewrites history):
```
main:          A --- B --- C
your-branch:   D --- E

After rebase:
main:          A --- B --- C
                            \
your-branch:                 D' --- E'
```
Moves your commits to the tip of main (advanced, don't worry about this yet).

---

### 6. Push

**What it is:** Upload your local commits to GitHub (the cloud).

**Your example:**
```bash
git push -u origin claude/convert-to-telegram-bot-011CUSqAXyxkCZtA1oR6MhYV
```

Breaking this down:
- `git push` - Upload commits
- `-u` - Set up tracking (so future pushes are easier)
- `origin` - The remote repository (your GitHub repo)
- `claude/...` - The branch name to push

**Think of it as:** Syncing to the cloud (like Dropbox or iCloud).

---

### 7. Pull

**What it is:** Download changes from GitHub to your local computer.

**Example:**
```bash
git pull origin main
```

**Think of it as:** Downloading the latest version from the cloud.

**When you need it:**
- Someone else made changes
- You're working on multiple computers
- You want the latest version of a branch

---

## Your Current Situation Explained

### What We've Done So Far:

```
1. Started on branch: claude/convert-to-telegram-bot-011CUSqAXyxkCZtA1oR6MhYV
   (Claude Code created this automatically)

2. Created files:
   - PROJECT_SCOPE.md
   - TECHNICAL_OVERVIEW.md
   - IMPLEMENTATION_CHECKLIST.md
   - FEATURES_EXPLAINER.md

3. Made commits:
   - Commit 1: Added first 3 planning docs
   - Commit 2: Added features explainer

4. Pushed to GitHub:
   - Uploaded our branch to GitHub
   - Now accessible from anywhere

5. Main branch unchanged:
   - Still has the original tarot bot code
   - Our changes are separate (on our branch)
```

### Visualizing Your Repo:

```
main branch (on GitHub):
  ├── bot.py (tarot bot)
  ├── requirements.txt
  ├── README.md
  └── Notes.txt

claude/convert-to-telegram-bot-... branch (on GitHub):
  ├── bot.py (tarot bot - unchanged)
  ├── requirements.txt
  ├── README.md
  ├── Notes.txt
  ├── PROJECT_SCOPE.md ← NEW
  ├── TECHNICAL_OVERVIEW.md ← NEW
  ├── IMPLEMENTATION_CHECKLIST.md ← NEW
  └── FEATURES_EXPLAINER.md ← NEW
```

---

## Common Workflows

### Solo Developer Workflow (You):

```
1. Create/checkout a branch
   git checkout -b feature-new-thing

2. Make changes to files
   (edit code, create files, etc.)

3. Stage changes
   git add .

4. Commit changes
   git commit -m "Description of changes"

5. Push to GitHub
   git push -u origin feature-new-thing

6. Create Pull Request on GitHub
   (visit the URL GitHub provides)

7. Review your own changes

8. Merge the PR
   (click "Merge" button on GitHub)

9. Switch back to main
   git checkout main

10. Pull the merged changes
    git pull origin main
```

### Team Workflow:

Same as above, but:
- Step 7: Others review your code
- Step 8: Someone else (or you after approval) merges

---

## Practical Examples

### Example 1: Viewing Your Branches

```bash
# See all branches
git branch -a

# Output might show:
* claude/convert-to-telegram-bot-011CUSqAXyxkCZtA1oR6MhYV  ← (you're here)
  main
  remotes/origin/main
  remotes/origin/claude/convert-to-telegram-bot-...
```

The `*` shows which branch you're currently on.

### Example 2: Switching Branches

```bash
# Switch to main branch
git checkout main

# Switch back to your feature branch
git checkout claude/convert-to-telegram-bot-011CUSqAXyxkCZtA1oR6MhYV
```

### Example 3: Seeing Commit History

```bash
# View recent commits
git log

# Output shows:
commit f574d5b...
Author: You
Date: Oct 24 2025
    Add user-friendly features explainer for LifeOS bot

commit 9ea59e1...
Author: You
Date: Oct 24 2025
    Add comprehensive planning documentation for LifeOS bot conversion
```

### Example 4: Seeing What Changed

```bash
# See what files changed in last commit
git show

# See differences between your branch and main
git diff main
```

---

## What Should You Do Next?

### Option 1: Keep Working on Your Branch

**When to do this:** You're not ready to merge yet, want to add more changes.

```bash
# Just keep working
# Make changes, commit, push
# All changes stay on your branch
```

**This is what we're doing now** - building out the planning docs.

### Option 2: Create a Pull Request

**When to do this:** You want to review changes or merge into main.

```
1. Go to GitHub repo in browser
2. Click "Pull requests" tab
3. Click "New pull request"
4. Select your branch
5. Click "Create pull request"
6. Add description
7. Click "Create pull request" again
```

**When to do this for your bot:**
- After we finish all planning docs (done!)
- Or after we implement the new bot features
- Whenever you want to make these changes "official"

### Option 3: Merge Directly (Advanced)

**When to do this:** You're confident and want to merge without a PR.

```bash
# Switch to main
git checkout main

# Merge your branch into main
git merge claude/convert-to-telegram-bot-011CUSqAXyxkCZtA1oR6MhYV

# Push merged changes
git push origin main
```

**Note:** PRs are generally better because they give you a chance to review.

---

## GitHub Web Interface

### Viewing Your Repo on GitHub:

1. **Go to:** https://github.com/itsaaronngan/telegramtarot

2. **You'll see:**
   - Branch selector (default: main)
   - File browser
   - Recent commits
   - README.md displayed

3. **Switch to your branch:**
   - Click branch dropdown
   - Select `claude/convert-to-telegram-bot-...`
   - Now you'll see your new files!

4. **View commits:**
   - Click "Commits" link
   - See all changes over time

5. **View a specific file:**
   - Click filename
   - See contents in browser
   - Click "History" to see changes over time

---

## Common Commands Cheat Sheet

```bash
# Check status (what's changed, what branch you're on)
git status

# See branches
git branch -a

# Switch branches
git checkout branch-name

# Create new branch and switch to it
git checkout -b new-branch-name

# Stage all changes
git add .

# Stage specific file
git add filename.txt

# Commit staged changes
git commit -m "Your message here"

# Push to GitHub
git push origin branch-name

# Pull from GitHub
git pull origin branch-name

# See commit history
git log

# See what changed in files
git diff

# See what's in last commit
git show
```

---

## Understanding the Workflow We're Using

### Why Claude Code Created a Branch:

Claude Code automatically creates branches like:
```
claude/convert-to-telegram-bot-011CUSqAXyxkCZtA1oR6MhYV
```

This is because:
1. **Safety** - Won't accidentally change main branch
2. **Review** - You can review changes before merging
3. **Isolation** - Can experiment without breaking things
4. **Traceability** - Session ID in name shows what work was done when

### What Happens When We Commit:

```
You ask Claude to create files
     ↓
Claude creates/edits files on your computer
     ↓
Claude stages the files (git add)
     ↓
Claude commits with a message (git commit)
     ↓
Claude pushes to GitHub (git push)
     ↓
Your work is now backed up in the cloud!
```

---

## Best Practices

### 1. Commit Often
**Good:**
```
- Small, focused commits
- "Add task manager module"
- "Fix bug in date parsing"
- "Update README with new features"
```

**Bad:**
```
- One huge commit at end of day
- "Fixed stuff and added things"
```

### 2. Write Clear Commit Messages
**Good:**
```
"Add voice transcription using OpenAI Whisper API"
"Fix task completion not updating git"
"Update documentation with deployment instructions"
```

**Bad:**
```
"update"
"fix"
"asdf"
```

### 3. Use Branches for Features
**Good:**
```
main - stable code
feature/voice-notes - working on voice feature
feature/task-manager - working on tasks
bugfix/date-parsing - fixing a bug
```

**Bad:**
```
Doing everything directly on main
Random branch names like "test" or "stuff"
```

### 4. Pull Before You Push
If working with others (or from multiple computers):
```bash
# Before starting work
git pull origin main

# Make changes, commit

# Before pushing
git pull origin main  # Get any new changes
git push origin your-branch
```

---

## Troubleshooting Common Issues

### "Nothing to commit, working tree clean"
**Meaning:** No changes to save.
**Solution:** Make some changes first, then commit.

### "Your branch is behind 'origin/main'"
**Meaning:** GitHub has newer commits than you.
**Solution:** `git pull origin main`

### "Merge conflict"
**Meaning:** Same file edited in two places differently.
**Solution:** Open the file, manually resolve conflicts, then commit.

### "Permission denied"
**Meaning:** Can't push to GitHub.
**Solution:** Check your GitHub authentication (token, SSH key).

---

## Analogy Summary

If Git/GitHub were a **Google Docs** alternative:

| Git/GitHub | Google Docs Equivalent |
|------------|------------------------|
| **Repository** | The document |
| **Commit** | Saving a named version |
| **Branch** | Making a copy to work on |
| **Merge** | Accepting suggested edits |
| **Push** | Uploading changes |
| **Pull** | Downloading changes |
| **Pull Request** | Suggesting edits for review |
| **Conflict** | Two people editing same part |

---

## What's Next for Your Project?

### Current State:
```
✅ Branch created: claude/convert-to-telegram-bot-...
✅ Planning docs committed and pushed
✅ Everything backed up on GitHub
```

### Options:

**Option A: Continue working on this branch**
- When you're home, review LifeOS structure
- Start implementing the bot
- Make more commits as we build
- Eventually merge when done

**Option B: Create a Pull Request now**
- Review the planning docs on GitHub
- Merge them into main
- Start a new branch for actual implementation

**Option C: Keep as-is**
- Leave planning docs on this branch
- Reference them while building
- Merge everything when complete

**I recommend Option A** - keep working on this branch until the bot is fully implemented, then merge it all at once.

---

## Questions?

Now you understand:
- ✅ What Git and GitHub are
- ✅ What branches are (parallel versions)
- ✅ What commits are (snapshots)
- ✅ What pull requests are (merge proposals)
- ✅ What merging is (combining branches)
- ✅ How we're using them for your bot project

Any questions about specific concepts or workflows?
