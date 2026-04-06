---
command: "/deploy"
description: "Deploys the application to production. Uses MCP tools."
phase: "6"
agents: ["deployer"]
skills: ["publish"]
outputs: ["Live URL", "Updated STATE.md", "Deployment log"]
---

# /deploy

## Steps

1. Pre-deploy checklist:
   - [ ] L1–L4 all pass
   - [ ] `.env` variables correct (not test values)
   - [ ] Deploy target in REQUIREMENTS.md
   - [ ] No hardcoded localhost URLs
2. Read `projects/{name}/REQUIREMENTS.md` → identify deploy target.
3. Read `agents/deployer.md` → execute target-specific deploy:
   - **Vercel/Next.js**: `vercel --prod` or Vercel MCP, set env vars, verify URL
   - **Cloudflare Workers**: Cloudflare MCP, set KV/D1/R2 bindings, verify API
   - **Expo**: `eas build` + store submit or `eas update` for OTA
   - **Supabase**: run migrations via MCP, verify RLS + anon key
   - **Firebase**: Firebase MCP deploy hosting/functions, verify URL
4. Post-deploy: open live URL, run core user flow smoke test, confirm no 500 errors.
5. Update STATE.md — Phase 6 complete, add live URL.
6. Confirm:
```
🚀 Deployed!
🌐 Live URL: {url}
📅 Deployed: {date}
Run `/finish` to archive this project.
```

**Next**: `/finish`
