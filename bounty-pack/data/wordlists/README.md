# Wordlist Index — Bug Bounty Audit Pipeline
# Auto-reference: bb-audit-launcher + exploit-cookbook

## Phase 0B: Recon
| File | Purpose | Tool |
|------|---------|------|
| 0B-recon/subdomains/subdomains-top1million-5000.txt | Subdomain enumeration | subfinder, amass |
| 0B-recon/subdomains/subdomains-top1million-20000.txt | Extended subdomain list | subfinder, amass |
| 0B-recon/directories/common.txt | Directory discovery | ffuf, gobuster, nuclei |
| 0B-recon/directories/raft-medium-directories.txt | Medium directory brute | ffuf, gobuster |
| 0B-recon/directories/raft-large-directories.txt | Large directory brute | ffuf, gobuster |
| 0B-recon/files/raft-large-files.txt | File discovery | ffuf, gobuster |
| 0B-recon/files/raft-medium-files.txt | Medium file discovery | ffuf, gobuster |
| 0B-recon/params/params.txt | Parameter discovery | arjun, paramspider |

## Phase 0C: Testing — SQL Injection
| File | Purpose | Tool |
|------|---------|------|
| 0C-sqli/sqli-auth-bypass.txt | Auth bypass payloads | sqlmap, manual |
| 0C-sqli/sqli-payloads-big.txt | Extended SQLi payloads | sqlmap, bbqsql |

## Phase 0C: Testing — XSS
| File | Purpose | Tool |
|------|---------|------|
| 0C-xss/xss-polyglots.txt | XSS detection + bypass | dalfox, kxss, manual |

## Phase 0C: Testing — SSRF
| File | Purpose | Tool |
|------|---------|------|
| 0C-ssrf/ssrf-payloads.txt | SSRF cloud metadata + internal | manual, curl |

## Phase 0C: Testing — NoSQLi
| File | Purpose | Tool |
|------|---------|------|
| 0C-nosqli/nosqli-injection.txt | MongoDB/NoSQL injection | nosqlmap, manual |

## Phase 0C: Testing — Command Injection
| File | Purpose | Tool |
|------|---------|------|
| 0C-cmdi/cmdi-payloads.txt | CMDi + reverse shell | commix, manual |

## Phase 0C: Testing — Path Traversal
| File | Purpose | Tool |
|------|---------|------|
| 0C-path-traversal/path-traversal-payloads.txt | LFI/RFI payloads | ffuf, manual |

## Phase 0C: Testing — XXE
| File | Purpose | Tool |
|------|---------|------|
| 0C-xxe/xxe-payloads.txt | XXE injection payloads | manual |

## Phase 0C: Testing — JWT
| File | Purpose | Tool |
|------|---------|------|
| 0C-jwt/jwt-attack-payloads.txt | JWT none/algorithm confusion | jwt_tool, manual |

## Phase 0C: Testing — GraphQL
| File | Purpose | Tool |
|------|---------|------|
| 0C-graphql/graphql-attack-payloads.txt | Introspection + BOLA + batching | graphcrawl, inql, manual |

## Phase 0C: Testing — WAF Bypass
| File | Purpose | Tool |
|------|---------|------|
| 0C-waf-bypass/waf-bypass-payloads.txt | WAF evasion techniques | sqlmap tamper, manual |

## Phase 0C: Testing — Sensitive Files
| File | Purpose | Tool |
|------|---------|------|
| 0C-sensitive-files/sensitive-files-wordlist.txt | Config/env/backup discovery | ffuf, nuclei, manual |

## Phase 0C: Testing — Auth Bypass
| File | Purpose | Tool |
|------|---------|------|
| 0C-auth-bypass/ | Auth testing payloads | manual |

## Phase 0C: Testing — Web3
| File | Purpose | Tool |
|------|---------|------|
| 0C-web3/web3-attack-patterns.txt | Smart contract attack patterns | slither, manual |

## Phase 0C: Testing — Passwords
| File | Purpose | Tool |
|------|---------|------|
| 0C-passwords/common-passwords.txt | Credential testing | medusa, manual |

## References
| File | Purpose |
|------|---------|
| references/ | Audit methodology + reporting templates |

## Auto-Load
These wordlists are referenced by:
- exploit-cookbook/SKILL.md
- bb-audit-launcher/SKILL.md
- bug-bounty-exhaustive-testing/SKILL.md
- reference-loader.md

Location: D:/data hermes/wordlists/
