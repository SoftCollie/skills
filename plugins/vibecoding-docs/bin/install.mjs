#!/usr/bin/env node
// Instalador de la skill «vibecoding-docs» para Claude Code.
// Copia el contenido de la skill a ~/.claude/skills/vibecoding-docs.
import { cpSync, existsSync, mkdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, '..', 'skills', 'vibecoding-docs');
const destRoot = join(homedir(), '.claude', 'skills');
const dest = join(destRoot, 'vibecoding-docs');

if (!existsSync(src)) {
  console.error('✗ No se encontró el contenido de la skill en:', src);
  process.exit(1);
}

mkdirSync(destRoot, { recursive: true });
cpSync(src, dest, { recursive: true });

console.log('✓ Skill «vibecoding-docs» instalada en:', dest);
console.log('  Reinicia Claude Code y úsala escribiendo: /vibecoding-docs');
