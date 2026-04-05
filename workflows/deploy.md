---
command: "/deploy"
description: "Deploys the application to production. Uses MCP tools."
phase: "6"
agents: ["deployer"]
skills: ["publish"]
outputs: ["Live URL", "Updated STATE.md", "Deployment log"]
---

# /deploy — Deploy to Production

## When to Use

After `/test` has passed L1–L4. The app is ready to go live.

## Steps

### Step 1: Pre-Deploy Checklist

Before spawning the deployer, verify:

- [ ] L1–L4 tests all pass
- [ ] `.env` variables are set correctly (not test values)
- [ ] REQUIREMENTS.md lists the deploy target (Vercel / Cloudflare / Firebase / Expo)
- [ ] No hardcoded localhost URLs in code

### Step 2: Read Requirements

Read `projects/{name}/REQUIREMENTS.md` to identify the deploy target.

### Step 3: Spawn Deployer Agent

Read `agents/deployer.md` and spawn the agent.

The deployer:

**Web (Vercel/Next.js)**:
- Runs `vercel --prod` or uses Vercel MCP
- Sets environment variables in Vercel dashboard
- Verifies deployment URL loads correctly

**Backend (Cloudflare Workers)**:
- Uses Cloudflare MCP to deploy Workers
- Sets KV / D1 / R2 bindings
- Verifies API endpoint responds

**Mobile (Expo)**:
- Runs `eas build` for production binary
- Submits to App Store / Play Store if configured
- Or creates OTA update via `eas update`

**Database (Supabase)**:
- Uses Supabase MCP to run migrations
- Verifies RLS policies are active
- Checks that anon key is restricted correctly

**Firebase**:
- Uses Firebase MCP to deploy hosting / functions
- Verifies hosting URL is live

### Step 4: Post-Deploy Verification

After the deploy command succeeds:
1. Open the live URL (or get a screenshot if Claude Preview available)
2. Run a quick smoke test: core user flow end-to-end
3. Confirm no 500 errors in logs

### Step 5: Update STATE.md

Mark Phase 6 complete. Add the live URL.

### Step 6: Confirm to User

```
🚀 Deployed!

🌐 Live URL: {url}
📅 Deployed: {date}

Run `/finish` to archive this project and close it out.
```

## Next Step

`/finish`
