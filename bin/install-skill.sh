#!/usr/bin/env bash
# Install video-analyst as a Claude Code skill
set -e

SKILL_DIR="${HOME}/.claude/skills/video-analyst"
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Installing video-analyst Claude Code skill..."

# Create skill directory
mkdir -p "$SKILL_DIR"

# Copy SKILL.md
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"

# Create a symlink to the project for the CLI
if [ ! -L "$SKILL_DIR/project" ]; then
  ln -sf "$SCRIPT_DIR" "$SKILL_DIR/project"
fi

# Ensure Python environment is set up
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
  echo "Setting up Python environment..."
  if command -v uv &>/dev/null; then
    (cd "$SCRIPT_DIR" && uv venv && uv pip install -e .)
  else
    (cd "$SCRIPT_DIR" && python3 -m venv .venv && .venv/bin/pip install -e .)
  fi
fi

echo ""
echo "Done! Skill installed to $SKILL_DIR"
echo ""
echo "Make sure GEMINI_API_KEY is set in your environment."
echo "Use in Claude Code: /video-analyst <url>"
