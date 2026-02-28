#!/usr/bin/env node

const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const pkgDir = path.resolve(__dirname, "..");
const skillSrc = path.join(pkgDir, "SKILL.md");
const skillDir = path.join(
  process.env.HOME || process.env.USERPROFILE,
  ".claude",
  "skills",
  "video-analyst"
);

console.log("@getvrex/video-analyst: setting up...");

// Create skill directory
try {
  fs.mkdirSync(skillDir, { recursive: true });
} catch (e) {
  // directory exists
}

// Copy SKILL.md to Claude skills directory
try {
  fs.copyFileSync(skillSrc, path.join(skillDir, "SKILL.md"));
  console.log(`  Skill installed to ${skillDir}/SKILL.md`);
} catch (e) {
  console.warn(`  Warning: Could not install Claude skill: ${e.message}`);
}

// Check for Python
let pythonCmd = null;
for (const cmd of ["python3", "python"]) {
  try {
    const version = execSync(`${cmd} --version 2>&1`, { encoding: "utf-8" }).trim();
    pythonCmd = cmd;
    console.log(`  Found ${version}`);
    break;
  } catch (e) {
    // try next
  }
}

if (!pythonCmd) {
  console.warn(
    "  Warning: Python 3.11+ not found. Install Python and run:\n" +
    `    cd ${pkgDir} && ${pythonCmd || "python3"} -m venv .venv && .venv/bin/pip install -e .`
  );
  process.exit(0);
}

// Set up venv and install
try {
  // Try uv first (faster)
  try {
    execSync("uv --version 2>&1", { encoding: "utf-8" });
    console.log("  Setting up with uv...");
    execSync(`cd "${pkgDir}" && uv venv && uv pip install -e .`, {
      stdio: "inherit",
    });
  } catch (e) {
    // Fall back to pip
    console.log("  Setting up with pip...");
    execSync(
      `cd "${pkgDir}" && ${pythonCmd} -m venv .venv && .venv/bin/pip install -e .`,
      { stdio: "inherit" }
    );
  }
  console.log("  Python environment ready.");
} catch (e) {
  console.warn(
    `  Warning: Auto-setup failed. Run manually:\n` +
    `    cd ${pkgDir} && ${pythonCmd} -m venv .venv && .venv/bin/pip install -e .`
  );
}

console.log("\n@getvrex/video-analyst installed!");
console.log("  Set your API key: export GEMINI_API_KEY=your_key");
console.log("  Run: video-analyst analyze <URL>");
