#!/usr/bin/env bash
# Quick install: clone, set up Python env, and install Claude Code skill
set -e

INSTALL_DIR="${HOME}/.claude/skills/video-analyst"

echo "Installing video-analyst..."

# Clone or update
if [ -d "$INSTALL_DIR/.git" ]; then
  echo "Updating existing installation..."
  (cd "$INSTALL_DIR" && git pull --ff-only)
else
  echo "Cloning repository..."
  mkdir -p "$(dirname "$INSTALL_DIR")"
  git clone https://github.com/getvrex/video-analyst.git "$INSTALL_DIR"
fi

# Set up Python environment
cd "$INSTALL_DIR"
if command -v uv &>/dev/null; then
  uv venv && uv pip install -e .
else
  python3 -m venv .venv && .venv/bin/pip install -e .
fi

echo ""
echo "Done! video-analyst installed to $INSTALL_DIR"
echo ""
echo "Setup:"
echo "  export GEMINI_API_KEY=your_key_here"
echo ""
echo "Usage:"
echo "  CLI:        source $INSTALL_DIR/.venv/bin/activate && video-analyst analyze <URL>"
echo "  Claude Code: /video-analyst <URL>"
