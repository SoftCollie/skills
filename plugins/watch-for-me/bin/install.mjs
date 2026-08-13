#!/usr/bin/env node
// Installer for the "watch-for-me" Claude Code skill.
// Copies the skill's contents into ~/.claude/skills/watch-for-me.
import { cpSync, existsSync, mkdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, '..', 'skills', 'watch-for-me');
const destRoot = join(homedir(), '.claude', 'skills');
const dest = join(destRoot, 'watch-for-me');

if (!existsSync(src)) {
  console.error('✗ Could not find the skill contents at:', src);
  process.exit(1);
}

mkdirSync(destRoot, { recursive: true });
cpSync(src, dest, { recursive: true });

console.log('✓ Skill "watch-for-me" installed at:', dest);
console.log('  Restart Claude Code and use it with: /watch-for-me <path-or-URL>');
