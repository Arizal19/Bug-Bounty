# Context Budget Update — 2026-09-19

## Updated Config
- `context_length: 512000` (was 256000)
- `threshold: 0.80` (was 0.65)
- `compression trigger: 409K tokens` (was 166K)

## Updated Budget Allocation
```
0A = 20KB
0B = 30KB
0C = 80KB (was 60KB — more room for tool output)
0D = 40KB
Peak WITH eviction = 170KB < 409KB ✅
```

## bb-audit-launcher SKILL.md Needs Patch
Line references to update:
- Line ~34: `Budget: 0A=20KB, 0B=30KB, 0C=60KB, 0D=40KB. Peak WITH eviction=120KB < 162KB ✅`
  → Change to: `Budget: 0A=20KB, 0B=30KB, 0C=80KB, 0D=40KB. Peak WITH eviction=170KB < 409KB ✅`
- Line ~39: `Peak WITH eviction = 120KB < 162KB threshold ✅`
  → Change to: `Peak WITH eviction = 170KB < 409KB threshold ✅`

## Reload Checkpoint Cleanup Needed
The reload checkpoints (A, B, C) in bb-audit-launcher contradict execution discipline Rule 1:
- Checkpoint A: `read_file + skill_view + skill_view` → loads 3 skills at once (VIOLATION)
- Should be: Load 1 skill → execute 3 tools → then load next if needed

## Execution Discipline Integration (DONE)
- `execution-discipline-protocol.md` created at `exploit-cookbook/references/`
- Wired to bb-audit-launcher SKILL.md (bottom section)
- Wired to reference-loader.md
- 6 rules: Load≠Execute, Timeout=Retry, Reload After Compression, Verification Gate, Diversification, Self-Check
