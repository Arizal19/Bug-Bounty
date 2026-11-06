# Bug-Bounty SKILL.md Patches Needed — 2026-09-19

## Issue: Old Context Threshold References
The bug-bounty SKILL.md still references old context thresholds (162KB) which causes premature compression anxiety and wrong budget calculations.

## Patches Required

### Patch 1: Update Budget Line
**Old (line ~28):**
```
⚠️ BUDGET: peak cumulative WITH eviction = 120KB (under 162KB threshold)
⚠️ WITHOUT eviction = 249KB → compression fires → skills pruned → audit dies
```

**New:**
```
⚠️ BUDGET: peak cumulative WITH eviction = 170KB (under 409KB threshold)
⚠️ WITHOUT eviction = 249KB → still under 409KB → compression unlikely
⚠️ Config: context_length=512K, threshold=0.80 → trigger at 409K tokens
```

### Patch 2: Update Phase Budget
**Old:**
```
Budget: 0A=20KB, 0B=30KB, 0C=60KB, 0D=40KB
```

**New:**
```
Budget: 0A=20KB, 0B=30KB, 0C=80KB, 0D=40KB
```

### Patch 3: Execution Discipline Integration
Add at the end of SKILL.md:
```
## ⛔ EXECUTION DISCIPLINE (MANDATORY)
Load at audit start:
read_file('skills/security/exploit-cookbook/references/execution-discipline-protocol.md')
6 Rules: Load≠Execute, Timeout=Retry, Reload After Compression, Verification Gate, Diversification, Self-Check
```

### Patch 4: Reload Checkpoint Cleanup
The reload checkpoints (A, B, C) contradict execution discipline Rule 1:
- Checkpoint A loads 3 skills at once → VIOLATION
- Should be: Load 1 skill → execute 3 tools → then load next if needed
- Simplify to: "After compression, reload top 5 reference files before continuing"

### Patch 5: HTML Injection Rules
Add to reference-loader.md or bug-bounty-testing.md:
```
read_file('skills/security/exploit-cookbook/references/html-injection-rules.md')
```
Rule: HTML injection MUST chain to XSS or real impact. Basic payloads = OUT OF SCOPE.
