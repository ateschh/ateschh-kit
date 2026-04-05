# sync-selective-skills.ps1
# Copies SKILL.md from a specific whitelist of global skills into ateschh-kit/skills/

$Source = "C:\Users\murat\.claude\skills"
$Dest   = "C:\GENERATOR\skills"

$whitelist = @(
    # A - Web & Frontend
    "nextjs-app-router-patterns",
    "nextjs-best-practices",
    "react-best-practices",
    "typescript-expert",
    "tailwind-design-system",
    "shadcn",
    
    # B - Mobile
    "react-native-architecture",
    "expo-deployment",
    "expo-api-routes",
    "flutter-expert",
    
    # C - Backend & DB
    "nodejs-backend-patterns",
    "fastapi-pro",
    "supabase-automation",
    "prisma-expert",
    "postgres-best-practices",
    
    # D - AI/ML
    "llm-app-patterns",
    "rag-implementation",
    "prompt-engineering",
    
    # E - DevOps & Deploy
    "docker-expert",
    "cloudflare-workers-expert",
    "vercel-deployment",
    "electron-development"
)

$copied = 0
$missing = 0

Write-Host "Starting selective skill sync... ($($whitelist.Count) skills requested)" -ForegroundColor Cyan

foreach ($skill in $whitelist) {
    $sourceDir = Join-Path $Source $skill
    $skillMd = Join-Path $sourceDir "SKILL.md"
    
    if (Test-Path $skillMd) {
        $targetDir = Join-Path $Dest $skill
        if (-not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir | Out-Null
        }
        Copy-Item -Path $skillMd -Destination (Join-Path $targetDir "SKILL.md") -Force
        $copied++
        Write-Host "✅ Copied: $skill" -ForegroundColor Green
    } else {
        $missing++
        Write-Host "❌ Missing or no SKILL.md: $skill" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Cyan
Write-Host "  Copied : $copied skills" -ForegroundColor Green
Write-Host "  Missing: $missing skills" -ForegroundColor Yellow
