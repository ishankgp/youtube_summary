# GitHub Workflow Guide

## Daily Development Workflow

### Basic Workflow
Every time you make code changes, follow these steps to update GitHub:

```powershell
# 1. Check what files you've changed
git status

# 2. Stage your changes (two options):
# Option A - Stage all changes:
git add .

# Option B - Stage specific files:
git add filename.tsx
git add frontend/my-app/components/

# 3. Commit your changes with a descriptive message:
git commit -m "type: brief description"

# 4. Pull any remote changes (using rebase)
git pull --rebase origin main

# 5. Push to GitHub
git push origin main
```

### Common Scenarios

1. **Made changes to multiple files**:
```powershell
git status                  # Check changes
git add .                   # Stage all
git commit -m "feat: ..."   # Commit
git pull --rebase origin main  # Get remote changes
git push origin main       # Push to GitHub
```

2. **Changed specific files only**:
```powershell
git status                    # Check changes
git add specific-file.tsx     # Stage specific file
git commit -m "fix: ..."      # Commit
git pull --rebase origin main # Get remote changes
git push origin main         # Push to GitHub
```

3. **Want to check what you're staging**:
```powershell
git status    # Before staging
git add .
git status    # After staging, before commit
```

## Working with Branches

Branches let you work on experimental features without affecting the main codebase.

### Creating and Using the Experimental Branch

1. **Create an experimental branch from main**:
```powershell
# Make sure you're on main first
git checkout main

# Create and switch to a new experimental branch
git checkout -b experimental

# Push the new branch to GitHub
git push -u origin experimental
```

2. **Switching between branches**:
```powershell
# Switch to main branch
git checkout main

# Switch to experimental branch
git checkout experimental
```

3. **Getting status of current branch**:
```powershell
# See what branch you're on and file status
git status

# See all branches (current branch marked with *)
git branch
```

4. **Committing changes on experimental branch**:
```powershell
# While on experimental branch
git add .
git commit -m "feat: experimental feature"
git push origin experimental
```

5. **Updating experimental with changes from main**:
```powershell
# First switch to experimental
git checkout experimental

# Pull changes from main into experimental
git merge main

# Or use rebase for cleaner history
git rebase main
```

6. **Bringing successful experiments to main**:
```powershell
# First switch to main
git checkout main

# Merge experimental changes into main
git merge experimental

# Push the updated main
git push origin main
```

### Branch Safety Tips

1. **Always know which branch you're on** before making changes:
```powershell
git status  # Shows current branch at the top
```

2. **Commit your changes** before switching branches to avoid losing work.

3. **Create a new branch** when trying risky changes:
```powershell
git checkout -b risky-idea
```

4. **Discard experimental changes** if needed:
```powershell
# Hard reset to remove unpushed commits (CAUTION: Destroys changes)
git reset --hard origin/experimental
```

## Commit Message Types

Use these prefixes for clear, consistent commit messages:

- `feat:` - New feature
  - Example: `feat: add summary refinement panel`
- `fix:` - Bug fix
  - Example: `fix: resolve transcript formatting`
- `style:` - Styling/UI changes
  - Example: `style: improve card layout`
- `refactor:` - Code restructuring
  - Example: `refactor: reorganize component structure`
- `docs:` - Documentation
  - Example: `docs: update README with new features`
- `chore:` - Maintenance tasks
  - Example: `chore: update dependencies`

## Understanding git pull --rebase

The command `git pull --rebase origin main` does the following:

```
Before Rebase:          After Rebase:
A → B → C               A → B → C → D → E
     ↘                  (Linear history)
       D → E
```

Benefits of using rebase:
1. Creates a linear, cleaner history
2. Avoids unnecessary merge commits
3. Easier to understand the sequence of changes
4. Better for code review

## Common Issues and Solutions

### Line Ending Issues (CRLF/LF)
If you see warnings about CRLF line endings:
```powershell
git config --global core.autocrlf true
```

### Timeout Issues
If push fails with timeout:
```powershell
# Increase buffer size
git config --global http.postBuffer 524288000

# Increase timeout limits
git config --global http.lowSpeedLimit 1000
git config --global http.lowSpeedTime 300
```

### Authentication Issues
- Ensure your GitHub credentials are correct
- Use a personal access token if required
- Check your remote URL:
  ```powershell
  git remote -v
  ```

## Best Practices

1. **Pull Before Push**
   - Always pull with rebase before pushing
   - Helps avoid conflicts

2. **Check Status Frequently**
   - Use `git status` before and after staging
   - Verify what you're about to commit

3. **Meaningful Commit Messages**
   - Use the correct type prefix
   - Write clear, concise descriptions
   - Reference issue numbers if applicable

4. **Regular Commits**
   - Commit related changes together
   - Keep commits focused and atomic
   - Push regularly to avoid large divergence