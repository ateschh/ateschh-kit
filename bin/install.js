#!/usr/bin/env node

/**
 * ateschh-kit installer
 *
 * Usage:
 *   npx ateschh-kit                  fresh install in cwd
 *   npx ateschh-kit <dir>            fresh install in <dir>
 *   npx ateschh-kit --update         refresh system files in cwd, leave projects/ untouched
 *   npx ateschh-kit --force          overwrite everything in cwd (use with care)
 *   npx ateschh-kit doctor           diagnose integrations + Python + Node
 *   npx ateschh-kit --no-integrations skip auto-install of Graphify/MemPalace/Caveman
 *
 * By default (fresh install or --update), the installer attempts to set up
 * Graphify, MemPalace, Caveman, and Context7 automatically. Anything that
 * fails (missing Python, no internet, permission, etc.) is logged and the
 * install continues. Run `npx ateschh-kit doctor` afterwards to inspect.
 */

const fs = require('fs')
const path = require('path')
const { execSync, spawnSync } = require('child_process')

// ── Helpers ─────────────────────────────────────────────────────────────────

function log(msg) { console.log(msg) }
function success(msg) { console.log(`\x1b[32mok  ${msg}\x1b[0m`) }
function info(msg) { console.log(`\x1b[36m..  ${msg}\x1b[0m`) }
function warn(msg) { console.log(`\x1b[33m!!  ${msg}\x1b[0m`) }
function error(msg) { console.error(`\x1b[31m!!  ${msg}\x1b[0m`) }

function copyDir(src, dest) {
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true })
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name)
    const destPath = path.join(dest, entry.name)
    if (entry.isDirectory()) copyDir(srcPath, destPath)
    else fs.copyFileSync(srcPath, destPath)
  }
}

function copyFile(src, dest) {
  const destDir = path.dirname(dest)
  if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true })
  fs.copyFileSync(src, dest)
}

function which(cmd) {
  const r = spawnSync(process.platform === 'win32' ? 'where' : 'which', [cmd], { encoding: 'utf8' })
  if (r.status === 0) return r.stdout.trim().split(/\r?\n/)[0]
  return null
}

function tryRun(cmd, args, options = {}) {
  const r = spawnSync(cmd, args, { encoding: 'utf8', ...options })
  return { ok: r.status === 0, stdout: r.stdout || '', stderr: r.stderr || '' }
}

// ── System file sync ────────────────────────────────────────────────────────

const SYSTEM_DIRS = ['.claude', '.agent', '.opencode', 'templates', 'design-engine', 'scripts']
const SYSTEM_FILES = [
  'CLAUDE.md',
  'AGENTS.md',
  'ARCHITECTURE.md',
  'README.md',
  'CHANGELOG.md',
  'CONTRIBUTING.md',
  'design-search.py',
  'setup.py',
]

function copySystemFiles(kitDir, targetDir) {
  for (const dir of SYSTEM_DIRS) {
    const src = path.join(kitDir, dir)
    if (!fs.existsSync(src)) continue
    info(`copy ${dir}/`)
    copyDir(src, path.join(targetDir, dir))
  }
  for (const file of SYSTEM_FILES) {
    const src = path.join(kitDir, file)
    if (!fs.existsSync(src)) continue
    info(`copy ${file}`)
    copyFile(src, path.join(targetDir, file))
  }
}

// ── Doctor ──────────────────────────────────────────────────────────────────

function doctor(targetDir) {
  log('\x1b[1mateschh-kit doctor\x1b[0m')
  log('---------------------------')

  let okCount = 0
  let issueCount = 0

  function check(name, fn) {
    try {
      const result = fn()
      if (result.ok) { success(`${name}: ${result.detail}`); okCount++ }
      else { warn(`${name}: ${result.detail}`); issueCount++ }
    } catch (e) {
      warn(`${name}: ${e.message}`)
      issueCount++
    }
  }

  // Node
  check('node', () => ({ ok: true, detail: process.version }))

  // Python
  check('python', () => {
    for (const cand of ['python', 'py', 'python3']) {
      const w = which(cand)
      if (w) {
        const r = tryRun(cand, ['--version'])
        if (r.ok) return { ok: true, detail: `${cand} (${r.stdout.trim()})` }
      }
    }
    return { ok: false, detail: 'not found on PATH (Python 3.10+ recommended for Graphify)' }
  })

  // Git
  check('git', () => {
    const w = which('git')
    if (!w) return { ok: false, detail: 'not found on PATH' }
    const r = tryRun('git', ['--version'])
    return { ok: r.ok, detail: r.stdout.trim() }
  })

  // Kit version stamp on target
  check('kit', () => {
    const claudeMd = path.join(targetDir, 'CLAUDE.md')
    if (!fs.existsSync(claudeMd)) {
      return { ok: false, detail: 'kit not installed at this directory' }
    }
    const pkgPath = path.join(__dirname, '..', 'package.json')
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'))
    return { ok: true, detail: `${pkg.name} v${pkg.version}` }
  })

  // Graphify
  check('graphify', () => {
    const w = which('graphify')
    if (!w) return { ok: false, detail: 'not installed (uv tool install graphifyy or pipx install graphifyy)' }
    // graphify uses --help (no --version flag); just probe the entrypoint exists.
    const r = tryRun('graphify', ['--help'])
    return { ok: r.ok, detail: r.ok ? `reachable at ${w}` : r.stderr.trim() || 'invocation failed' }
  })

  // MemPalace
  check('mempalace', () => {
    const w = which('mempalace')
    if (!w) return { ok: false, detail: 'not installed (pip install mempalace; configure as MCP)' }
    return { ok: true, detail: 'reachable' }
  })

  // Caveman
  check('caveman', () => {
    // Caveman is a Claude Code plugin. Probe via the user's claude plugin dir
    // (default: ~/.claude/plugins/marketplaces/) to see if it's been installed.
    const home = process.env.USERPROFILE || process.env.HOME
    if (home) {
      const candidates = [
        path.join(home, '.claude', 'plugins', 'marketplaces', 'caveman'),
        path.join(home, '.claude', 'plugins', 'caveman'),
        path.join(home, '.claude', 'plugins', 'JuliusBrussee', 'caveman'),
      ]
      for (const p of candidates) {
        if (fs.existsSync(p)) return { ok: true, detail: `plugin installed at ${p}` }
      }
    }
    if (which('claude')) {
      const r = tryRun('claude', ['plugin', 'list'])
      if (r.ok && /caveman/i.test(r.stdout)) return { ok: true, detail: 'plugin listed by claude CLI' }
    }
    return { ok: false, detail: 'plugin not detected; run `claude plugin install caveman@caveman` inside Claude Code' }
  })

  // Context7
  check('context7-mcp', () => {
    const r = tryRun(process.platform === 'win32' ? 'where' : 'which', ['npx'])
    return { ok: r.ok, detail: r.ok ? 'install with: npx -y @upstash/context7-mcp' : 'npx missing' }
  })

  // Validator
  check('validator', () => {
    const validate = path.join(__dirname, '..', 'scripts', 'validate.ps1')
    if (!fs.existsSync(validate)) return { ok: false, detail: 'scripts/validate.ps1 missing' }
    return { ok: true, detail: 'present (run: npm run validate)' }
  })

  log('')
  log(`${okCount} ok, ${issueCount} issue(s)`)
  log('')
  if (issueCount > 0) {
    log('Some integrations are not yet installed. The kit functions in degraded mode without them:')
    log('  - graphify  -> /map-codebase falls back to multi-agent analysis; /build uses grep instead of code graph.')
    log('  - mempalace -> /save and /resume use sessions/*.md as fallback (not as token-cheap).')
    log('  - caveman   -> caveman compression is applied manually by agents (still works, just not enforced).')
    log('  - context7  -> /requirements runs in degraded mode without version verification.')
    log('')
    log('Install instructions in README.md.')
  }

  process.exit(issueCount > 0 ? 1 : 0)
}

// ── Auto-install of integrations ────────────────────────────────────────────

function pickPython() {
  for (const cand of ['python', 'py', 'python3']) {
    const w = which(cand)
    if (w) {
      const r = tryRun(cand, ['--version'])
      if (r.ok) {
        const m = r.stdout.match(/Python\s+(\d+)\.(\d+)/)
        if (m) {
          const major = parseInt(m[1], 10)
          const minor = parseInt(m[2], 10)
          if (major === 3 && minor >= 9) return cand
        }
      }
    }
  }
  return null
}

function pickPythonInstaller() {
  // Preference: uv > pipx > pip (uv is fastest, pipx isolates, pip works everywhere).
  if (which('uv')) return 'uv'
  if (which('pipx')) return 'pipx'
  if (pickPython()) return 'pip'
  return null
}

function installViaPython(installer, pythonExe, packageName, executableName) {
  if (which(executableName)) {
    return { ok: true, detail: 'already on PATH' }
  }
  if (!installer) {
    return { ok: false, detail: 'no Python installer found (need uv, pipx, or pip)' }
  }

  let r
  if (installer === 'uv') {
    r = tryRun('uv', ['tool', 'install', packageName])
  } else if (installer === 'pipx') {
    r = tryRun('pipx', ['install', packageName])
  } else {
    r = tryRun(pythonExe, ['-m', 'pip', 'install', '--user', packageName])
  }

  if (!r.ok) {
    return { ok: false, detail: (r.stderr || r.stdout).split('\n').find(Boolean) || 'install failed' }
  }
  return { ok: true, detail: `installed via ${installer}` }
}

function installGraphify(installer, pythonExe) {
  const result = installViaPython(installer, pythonExe, 'graphifyy', 'graphify')
  if (result.ok && which('graphify')) {
    // Run `graphify install` to wire Claude Code hooks (skill files etc.).
    const r = tryRun('graphify', ['install'])
    if (!r.ok) {
      return { ok: false, detail: `package installed but 'graphify install' failed: ${(r.stderr || '').split('\n')[0]}` }
    }
    return { ok: true, detail: 'package + claude hooks installed' }
  }
  return result
}

function installMempalace(installer, pythonExe) {
  return installViaPython(installer, pythonExe, 'mempalace', 'mempalace')
}

function installCaveman() {
  // Caveman is a Claude Code plugin. The CLI `claude` is not always on PATH
  // (Claude Code is usually launched from the GUI). If `claude` is missing,
  // we cannot install it from this script — print instructions instead.
  if (!which('claude')) {
    return { ok: false, detail: 'claude CLI not on PATH; run `claude plugin install caveman@caveman` inside Claude Code' }
  }
  let r = tryRun('claude', ['plugin', 'marketplace', 'add', 'JuliusBrussee/caveman'])
  if (!r.ok && !(r.stderr || r.stdout).match(/already/i)) {
    return { ok: false, detail: 'plugin marketplace add failed' }
  }
  r = tryRun('claude', ['plugin', 'install', 'caveman@caveman'])
  if (!r.ok && !(r.stderr || r.stdout).match(/already/i)) {
    return { ok: false, detail: 'plugin install failed' }
  }
  return { ok: true, detail: 'caveman plugin installed' }
}

function ensureMcpRegistration(targetDir) {
  // Make sure .claude/settings.local.json declares MCP servers we expect.
  // We are conservative: only ADD entries that aren't already present.
  const settingsPath = path.join(targetDir, '.claude', 'settings.local.json')
  if (!fs.existsSync(settingsPath)) return { ok: false, detail: 'settings.local.json missing' }

  let raw
  try {
    raw = JSON.parse(fs.readFileSync(settingsPath, 'utf8'))
  } catch (e) {
    return { ok: false, detail: `settings.local.json invalid JSON: ${e.message}` }
  }

  raw.mcp = raw.mcp || {}
  raw.mcp.allowlist = raw.mcp.allowlist || []
  for (const name of ['context7', 'graphify', 'mempalace']) {
    if (!raw.mcp.allowlist.includes(name)) raw.mcp.allowlist.push(name)
  }

  fs.writeFileSync(settingsPath, JSON.stringify(raw, null, 2) + '\n')
  return { ok: true, detail: 'MCP allowlist updated' }
}

function autoInstallIntegrations(targetDir) {
  log('')
  log('\x1b[1mintegrations\x1b[0m')
  log('---------------------------')

  const pythonExe = pickPython()
  const pyInstaller = pickPythonInstaller()

  if (!pythonExe) {
    warn('Python 3.9+ not found. Skipping graphify + mempalace auto-install.')
    warn('Install Python 3.10+ then re-run: npx ateschh-kit --update')
  } else {
    info(`python: ${pythonExe}`)
    info(`installer: ${pyInstaller}`)

    const g = installGraphify(pyInstaller, pythonExe)
    if (g.ok) success(`graphify: ${g.detail}`)
    else warn(`graphify: ${g.detail}`)

    const m = installMempalace(pyInstaller, pythonExe)
    if (m.ok) success(`mempalace: ${m.detail}`)
    else warn(`mempalace: ${m.detail}`)
  }

  const c = installCaveman()
  if (c.ok) success(`caveman: ${c.detail}`)
  else warn(`caveman: ${c.detail}`)

  // Context7 is npx-driven; we don't pre-install. Just record the MCP entry.
  const mcp = ensureMcpRegistration(targetDir)
  if (mcp.ok) success(`mcp allowlist: ${mcp.detail}`)
  else warn(`mcp allowlist: ${mcp.detail}`)

  log('')
  log('Run `npx ateschh-kit doctor` to verify each integration.')
}

// ── Update / Install ─────────────────────────────────────────────────────────

function ensureRuntimeScaffold(targetDir) {
  const dirs = ['.state', 'projects', 'archive', 'mission']
  for (const dir of dirs) {
    const dirPath = path.join(targetDir, dir)
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true })
      info(`created ${dir}/`)
    }
  }

  const gitignorePath = path.join(targetDir, '.gitignore')
  const additions = `\n# ateschh-kit runtime files\n.state/\nprojects/\narchive/\nmission/\n`
  if (fs.existsSync(gitignorePath)) {
    const existing = fs.readFileSync(gitignorePath, 'utf8')
    if (!existing.includes('.state/')) {
      fs.appendFileSync(gitignorePath, additions)
      info('updated .gitignore')
    }
  } else {
    fs.writeFileSync(gitignorePath, additions.trim() + '\n')
    info('created .gitignore')
  }

  const activeProject = path.join(targetDir, '.state', 'ACTIVE-PROJECT.md')
  if (!fs.existsSync(activeProject)) {
    fs.writeFileSync(
      activeProject,
      `# Active Project\n\n(No active project)\n\nRun \`/new-project\` to get started.\n`
    )
  }
}

function reportLegacyProjects(targetDir) {
  const projectsDir = path.join(targetDir, 'projects')
  if (!fs.existsSync(projectsDir)) return
  const legacy = []
  for (const entry of fs.readdirSync(projectsDir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue
    const stamp = path.join(projectsDir, entry.name, '.kit-version')
    if (!fs.existsSync(stamp)) {
      legacy.push(entry.name)
      continue
    }
    const v = fs.readFileSync(stamp, 'utf8').trim()
    if (v && v !== '2.0.0') legacy.push(`${entry.name} (kit ${v})`)
  }
  if (legacy.length === 0) return

  log('')
  warn(`${legacy.length} project(s) on legacy kit version:`)
  for (const p of legacy) log(`  - ${p}`)
  log('')
  log('Run /migrate inside each project to upgrade. /rollback reverts if needed.')
}

async function main() {
  const args = process.argv.slice(2)

  if (args[0] === 'doctor') {
    return doctor(process.cwd())
  }

  const isUpdate = args.includes('--update')
  const isForce = args.includes('--force')
  const skipIntegrations = args.includes('--no-integrations')
  const positional = args.filter((a) => !a.startsWith('--'))[0]
  const targetDir = positional ? path.resolve(positional) : process.cwd()
  const kitDir = path.resolve(__dirname, '..')

  log('')

  if (isUpdate) {
    log('\x1b[1mateschh-kit updater\x1b[0m')
    log(`updating: ${targetDir}`)
    log('---------------------------')

    if (!fs.existsSync(path.join(targetDir, 'CLAUDE.md'))) {
      error('ateschh-kit is not installed here. Run without --update for fresh install.')
      process.exit(1)
    }

    copySystemFiles(kitDir, targetDir)
    log('')
    success('system files refreshed.')
    log('Your projects/ and .state/ are untouched.')
    if (!skipIntegrations) autoInstallIntegrations(targetDir)
    reportLegacyProjects(targetDir)
    return
  }

  log('\x1b[1mateschh-kit installer\x1b[0m')
  log(`target: ${targetDir}`)
  log('---------------------------')

  if (fs.existsSync(path.join(targetDir, 'CLAUDE.md'))) {
    warn('ateschh-kit already installed here.')
    warn('Refresh system files only:  npx ateschh-kit --update')
    warn('Overwrite everything:        npx ateschh-kit --force')
    if (!isForce) process.exit(0)
  }

  copySystemFiles(kitDir, targetDir)
  ensureRuntimeScaffold(targetDir)
  if (!skipIntegrations) autoInstallIntegrations(targetDir)
  reportLegacyProjects(targetDir)

  log('')
  success('ateschh-kit installed.')
  log('')
  log('Next steps:')
  log('  1. Open this directory in Claude Code, Antigravity, or OpenCode.')
  log('  2. Run /new-project (or /workspace for multi-app).')
  log('  3. Run `npx ateschh-kit doctor` to verify integrations.')
  log('')
  log('Anything that failed during auto-install can be retried with:')
  log('  npx ateschh-kit --update')
  log('Or installed manually — README.md has the commands.')
  log('')
}

main()
