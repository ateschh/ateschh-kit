#!/usr/bin/env node

/**
 * ateschh-kit installer
 * Usage: npx ateschh-kit [target-directory]
 */

const fs = require('fs')
const path = require('path')
const { execSync } = require('child_process')

// ── Helpers ─────────────────────────────────────────────────────────────────

function log(msg) { console.log(msg) }
function success(msg) { console.log(`\x1b[32m✅ ${msg}\x1b[0m`) }
function info(msg) { console.log(`\x1b[36mℹ  ${msg}\x1b[0m`) }
function warn(msg) { console.log(`\x1b[33m⚠  ${msg}\x1b[0m`) }
function error(msg) { console.error(`\x1b[31m✗  ${msg}\x1b[0m`) }

function copyDir(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true })
  }
  const entries = fs.readdirSync(src, { withFileTypes: true })
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name)
    const destPath = path.join(dest, entry.name)
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath)
    } else {
      fs.copyFileSync(srcPath, destPath)
    }
  }
}

function copyFile(src, dest) {
  const destDir = path.dirname(dest)
  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true })
  }
  fs.copyFileSync(src, dest)
}

// ── Main ─────────────────────────────────────────────────────────────────────

function copySystemFiles(kitDir, targetDir) {
  info('Copying CLAUDE.md...')
  copyFile(path.join(kitDir, 'CLAUDE.md'), path.join(targetDir, 'CLAUDE.md'))

  info('Copying .claude/ ...')
  copyDir(path.join(kitDir, '.claude'), path.join(targetDir, '.claude'))

  info('Copying agents/ ...')
  copyDir(path.join(kitDir, 'agents'), path.join(targetDir, 'agents'))

  info('Copying skills/ ...')
  copyDir(path.join(kitDir, 'skills'), path.join(targetDir, 'skills'))

  info('Copying templates/ ...')
  copyDir(path.join(kitDir, 'templates'), path.join(targetDir, 'templates'))

  info('Copying .agent/workflows/ (for Antigravity) ...')
  copyDir(path.join(kitDir, '.agent'), path.join(targetDir, '.agent'))
}

async function main() {
  const args = process.argv.slice(2)
  const isUpdate = args.includes('--update')
  const isForce = args.includes('--force')
  const targetDir = args.filter(a => !a.startsWith('--'))[0]
    ? path.resolve(args.filter(a => !a.startsWith('--'))[0])
    : process.cwd()
  const kitDir = path.resolve(__dirname, '..')

  log('')

  // ── UPDATE mode ─────────────────────────────────────────────────────────────
  if (isUpdate) {
    log('\x1b[1m🔄 ateschh-kit updater\x1b[0m')
    log('━━━━━━━━━━━━━━━━━━━━━━━━━')
    log(`Updating: ${targetDir}`)
    log('')

    if (!fs.existsSync(path.join(targetDir, 'CLAUDE.md'))) {
      error('ateschh-kit is not installed in this directory.')
      error('Run without --update to install fresh.')
      process.exit(1)
    }

    try {
      copySystemFiles(kitDir, targetDir)

      log('')
      log('━━━━━━━━━━━━━━━━━━━━━━━━━')
      success('ateschh-kit updated!')
      log('')
      log('Your projects and state are untouched.')
      log('Type /resume to continue where you left off.')
      log('')
    } catch (err) {
      error(`Update failed: ${err.message}`)
      process.exit(1)
    }
    return
  }

  // ── INSTALL mode ─────────────────────────────────────────────────────────────
  log('\x1b[1m🚀 ateschh-kit installer\x1b[0m')
  log('━━━━━━━━━━━━━━━━━━━━━━━━━')
  log(`Installing to: ${targetDir}`)
  log('')

  if (fs.existsSync(path.join(targetDir, 'CLAUDE.md'))) {
    warn('ateschh-kit is already installed in this directory.')
    warn('To update system files without touching your projects, run:')
    warn('  npx ateschh-kit --update')
    warn('To overwrite everything, run with --force.')
    if (!isForce) {
      process.exit(0)
    }
  }

  try {
    copySystemFiles(kitDir, targetDir)

    // Create runtime directories (never overwrite)
    const dirs = ['.state', 'projects', 'archive']
    for (const dir of dirs) {
      const dirPath = path.join(targetDir, dir)
      if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true })
        info(`Created ${dir}/`)
      }
    }

    // Create .gitignore additions
    const gitignorePath = path.join(targetDir, '.gitignore')
    const gitignoreAdditions = `
# ateschh-kit runtime files
.state/
projects/
archive/
`
    if (fs.existsSync(gitignorePath)) {
      const existing = fs.readFileSync(gitignorePath, 'utf8')
      if (!existing.includes('.state/')) {
        fs.appendFileSync(gitignorePath, gitignoreAdditions)
        info('Updated .gitignore')
      }
    } else {
      fs.writeFileSync(gitignorePath, gitignoreAdditions.trim() + '\n')
      info('Created .gitignore')
    }

    // Create initial ACTIVE-PROJECT.md
    const activeProjectPath = path.join(targetDir, '.state', 'ACTIVE-PROJECT.md')
    if (!fs.existsSync(activeProjectPath)) {
      fs.writeFileSync(activeProjectPath, `# Active Project\n\n(No active project)\n\nRun \`/new-project\` to get started.\n`)
    }

    log('')
    log('━━━━━━━━━━━━━━━━━━━━━━━━━')
    success('ateschh-kit installed!')
    log('')
    log('Next steps:')
    log('  1. Open this directory in Claude Code or Antigravity')
    log('  2. Type: /new-project')
    log('  3. Describe your idea')
    log('')
    log('Available commands:')
    log('  /new-project  /brainstorm  /requirements')
    log('  /design  /build  /test  /deploy')
    log('  /next  /quick  /status  /map-codebase')
    log('')

  } catch (err) {
    error(`Installation failed: ${err.message}`)
    process.exit(1)
  }
}

main()
