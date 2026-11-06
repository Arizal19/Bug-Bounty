# PLAYBOOK HUNTING v2 — UNIVERSAL (Web2 + Web3)

> Target-agnostic. Berlaku untuk target apa pun: aplikasi web, API, SaaS, mobile backend,
> smart contract (EVM/Solana/Move), protokol DeFi, atau kombinasi.
> Dikunci 13 Sep 2026. Menggantikan pola "recon luas → scan semua → 81 informational".

---

## §0. HUKUM DASAR

**1. Nilai temuan = dampak × pembuktian, bukan jumlah temuan.**
Banyak temuan informational = 0 payout. 1 temuan terbukti = 1 payout.

**2. Scanner output = hipotesis, BUKAN temuan.**
nuclei/ffuf/Slither/Aderyn/mythril mengeluarkan *pattern*. Pattern bukan exploit path.
Temuan sah hanya setelah ada **state change terverifikasi** (data terbaca, dana bergerak, akses didapat).

**3. Satu akun = mati untuk bug horizontal.**
IDOR/BOLA/privilege-cross/klaim-reward butuh ≥2 identitas berbeda kepemilikan.
Tanpa itu, semua temuan horizontal otomatis turun ke informational.
**Ini penyebab tunggal terbesar hasil nol.**

**4. Scope gate SEBELUM deep-dive.**
Urutan: in-scope? → dibayar? → by-design? → ada dampak nyata? → ada jalur uji?
Gagal salah satu → STOP. Jangan habiskan 3 hari di jalur mati.

**5. Severity inflation = omong kosong.**
Chain exploit yang mati = informational. Dilarang klaim HIGH/CRITICAL kalau chain-nya nggak jalan.

**6. Luas ≠ dalam.** Ratusan host itu noise. Nilai ada di sedikit aset yang pegang uang/data/identitas.

**7. Tools MENDUKUNG, bukan memutuskan.** Keputusan datang dari nalar soal invariant & alur data. Tool cuma konfirmasi.

---

## §1. STAGE 0 — GERBANG MASUK (20 menit, WAJIB, target apa pun)

| Gate | Pertanyaan | Gagal → |
|:--|:--|:--|
| **PAYOUT** | Program bayar? (bukan VDP-only / no-bounty) | SKIP target |
| **SCOPE** | Aset ini in-scope? | SKIP aset |
| **BY-DESIGN** | Ini perilaku yang disengaja/didokumentasi? | SKIP aset |
| **IMPACT** | Kalau dieksploit, dampaknya nyata & masuk kategori bayar? | Turunkan prioritas / SKIP |
| **AKSES** | Bisa dapat akses/akun/sandbox yang dibutuhkan? | Provision DULU, jangan jalan tanpa |
| **JALUR** | Ada cara menguji tanpa melanggar aturan program? | SKIP atau minta izin |

**Output Stage 0:** `scope.md` — daftar aset yang LOLOS semua gate. Sisanya diarsipkan, bukan dikejar.

---

## §2. KELAS BUG PRIORITAS (universal, urut nilai)

Hunt dari atas. Klas 1–4 = mayoritas payout. Klas 7–8 = informational, jangan dikejar.

| # | Kelas | Contoh generik | Syarat Uji | Nilai |
|:--|:--|:--|:--|:--|
| 1 | **IDOR/BOLA horizontal** | akses objek milik entitas lain by identifier | ≥2 akun | P1–P2 |
| 2 | **Authz di alur uang/nilai** | ubah payout, klaim milik orang, transfer, refund, mint | ≥2 akun | P1–P2 |
| 3 | **Auth bypass / sesi** | reset tanpa token, JWT alg, OAuth state, role escalation, MFA skip | 1–2 akun | P1–P2 |
| 4 | **Injeksi berdampak data** | SQLi baca tabel sensitif, SSRF ke internal, SSTI, RCE, deserialisasi | 1 akun | P1–P3 |
| 5 | **Logic/state (web2)** | race, kuota dobel, urutan aksi terbalik, nilai negatif/overflow | 1 akun | P2–P3 |
| 6 | **Logic/state (web3)** | invariant rusak, oracle/rounding, griefing, economic attack | 1 akun + RPC | P2–P3 |
| 7 | Misconfig infra | header, versi, CORS wildcard, open redirect, cookie flags | — | INFO |
| 8 | Info disclosure | stack trace, komentar, versi library, PII minim | — | INFO |

**Aturan:** temuan di klas 7–8 → catat 1 baris, lanjut. Jangan bikin laporan.

---

## §3. PILIH TARGET: 3–5 ASET, BUKAN SEMUA

### Web2 — pilih yang memenuhi ≥2 kriteria:
- [ ] Menangani **uang**: payment, payout, wallet, saldo, refund, reward, invoice
- [ ] Menangani **identitas**: login, reset, OTP, KYC, profil, token/sesi
- [ ] **Admin/panel internal** (authz biasanya lebih lemah)
- [ ] **Pre-prod/staging/dev** (hardening lebih tipis)
- [ ] **API yang dipanggil mobile/SPA** (sering lupa di-guard)
- [ ] **Integrasi pihak ketiga**: webhook, callback, import/export, SSO

### Web3 — pilih yang memenuhi ≥2 kriteria:
- [ ] **Megang dana/TVL** langsung (vault, pool, bridge, escrow, staking)
- [ ] **Kode custom** ≠ verbatim upstream (diff ≠ 0)
- [ ] **Kontrak baru/baru di-deploy/baru di-upgrade** (belum teruji waktu)
- [ ] **Verifikasi on-chain** ada (bisa baca source → bisa audit)
- [ ] **Kompleksitas**: proxy/upgrade, oracle eksternal, cross-contract, multi-chain
- [ ] **Titik kepercayaan eksplisit**: keeper, admin, relayer, off-chain signer

Buang semua host statis/marketing/redirector. Buang kontrak verbatim upstream tanpa modifikasi.
**Output:** `targets.md` — maksimal 5 baris, tiap baris ada alasan kenapa dipilih.

---

## §4. EKSEKUSI PER-VEKTOR (manual, bukan scanner)

Jalankan untuk SETIAP target di `targets.md`. Berhenti begitu ada state change berdampak.

### 4A. Petakan objek & identitas (30 mnt)
1. Login/provision ≥2 akun (A & B) berbeda kepemilikan. Simpan token/sesi/kredensial dua-duanya.
2. Picu semua aksi A yang menghasilkan objek: bikin order, simpan alamat, klaim, upload, deploy.
3. Catat SETIAP identifier: `id`, `uuid`, `ref`, `slug`, `token`, `tx_hash`, `invoice_no`, `address`.
4. Untuk web3: catat semua kontrak + alamat dari source/ABI/docs, roles, owner, proxy admin.

### 4B. Tukar identitas (uji horizontal) ← **INI YANG MENGHASILKAN UANG**
Untuk setiap endpoint/objek dari 4A:
```
A buat objek → catat id
B (identitas B) → akses/ubah/hapus objek id milik A
```
- 200 + data A → **IDOR terbukti** (screenshot + request dua arah)
- 403/404 → catat, lanjut
- 200 tapi kosong → cek field-level / partial response

**Varian wajib:**
- Ganti `id` angka → id tetangga; ganti uuid → uuid B
- Hapus header otorisasi; tukar token A↔B
- Tukar header identitas: `X-User-Id`, `X-Account`, `X-Org`, `tenant`, `sub`
- Ubah body: `user_id`, `owner`, `account_id`, `org_id`
- Coba versi API lama (`/v1` vs `/v2`), endpoint mobile vs web
- Coba tanpa trailing slash, dengan `.json`, dengan `?id=` dobel

### 4C. Naikkan hak (uji vertikal)
- Akun biasa → panggil endpoint admin yang ditemukan di JS bundle / docs / ABI
- **Method swap**: `GET`→`POST`/`PUT`/`PATCH`/`DELETE` (sering lupa di-guard per-method)
- Parameter tambahan: `role=admin`, `isAdmin=true`, `approved=1`, `verified=1`
- Web3: panggil fungsi `onlyOwner`/`onlyRole` dari akun non-owner; cek default role admin

### 4D. Rusak state (uji logic)
- Nilai ekstrem: negatif, nol, maks, desimal, overflow boundary
- Urutan aksi dibalik (klaim dulu → batalkan setelahnya)
- **Replay**: ulang request/transaksi — apakah efek dobel?
- **Race**: 2 request paralel untuk 1 kuota/saldo (web2), atau multi-tx dalam 1 blok (web3)
- Parameter tak terduga: `type`, `status`, `id[]` array, parameter duplikat
- Encoding: `%00`, unicode, double-encoding

### 4E. Chain (2 lemah → 1 kuat)
Contoh: open redirect + OAuth callback = token theft. Info disclosure + IDOR = full account read.
SSRF + metadata endpoint = credential access. Oracle stale + liquidation = bad debt.
**Jangan klaim chain yang belum ketemu ujungnya.**

### 4F. Bukti (WAJIB untuk setiap temuan)
(a) request/response HTTP asli **atau** tx hash/eth_call asli
(b) bukti ≥2 identitas kalau horizontal
(c) dampak nyata dalam 1 kalimat
Tidak ada ketiganya → bukan temuan.

---

## §5. JALUR WEB3 / ON-CHAIN

### 5A. Selalu lebih dulu: diff vs upstream
```
ambil source verified → diff vs upstream asli (compound/openzeppelin/uniswap fork)
```
Diff = permukaan serang. Verbatim = hampir pasti aman (kecuali bug upstream belum ketemu).
**Diff ≠ 0 → seluruh perhatian ke baris yang beda.**

### 5B. Invariant-first, bukan scanner-first
1. Tulis invariant yang HARUS selalu benar (contoh generik):
   - `Σ saldo user ≤ total supply`
   - `kas + reserve ≥ totalBorrow - totalReserve`
   - `exRate/shares tidak pernah naik diam-diam tanpa aksi user`
   - akun tanpa izin tidak bisa gerakkan dana/oracle/config
   - `totalPaid ≤ totalBudget`, `Σ reward dibayar = Σ yang tercatat`
   - nilai yang di-withdraw ≤ nilai yang di-deposit (per user & global)
2. Jalankan **Echidna / Medusa** untuk mecah invariant.
3. Jalankan **Halmos / Z3** untuk path simbolik yang tak tercakup fuzzer.
4. **Slither / Aderyn / mythril belakangan** — konfirmasi + cari yang terlewat.
5. Untuk arithmetic rawan: **Z3** model ulang formulanya, cari counterexample.

### 5C. Gate scope on-chain
- Butuh aksi admin/owner/keeper? → biasanya trusted → INFO
- Butuh kondisi mustahil (hash collision, konsensus rusak)? → mati
- Hanya jalan kalau protokol "salah set"? → biasanya by-design
- Butuh private key pihak lain? → out of scope

### 5D. Jalur campuran (paling sering terlewat)
Frontend ↔ kontrak: harga/alamat/signature dari API ke tx. Backend ↔ kontrak: keeper, relayer, signature off-chain.
**Signer/keeper dengan izin lebih dari yang seharusnya = temuan nyata.**

---

## §6. ANTI-POLA (yang bikin hasil nol)

| Anti-pola | Kenapa fatal | Ganti dengan |
|:--|:--|:--|
| Scan semua host dulu | ratusan info, 0 payout | Pilih ≤5 aset bernilai |
| Degradasi 2 akun → 1 akun | bug horizontal jadi untestable | Provision akun DULU |
| Scanner-first | output pattern, bukan exploit | invariant / per-vektor manual |
| Deep-dive sebelum scope gate | berhari-hari di jalur mati | gate 20 menit di depan |
| Kejar klas 7–8 | info semua | catat 1 baris, lanjut |
| Laporan tiap "temuan" | dilusi kredibilitas | 1 laporan kuat > 10 lemah |
| Anggap tool = keputusan | tool nggak tahu konteks bisnis | tool konfirmasi, otak memutuskan |

---

## §7. OUTPUT STANDAR

Per target, di `_progress/<target>/`:
- `scope.md` — hasil Stage 0
- `targets.md` — ≤5 aset terpilih + alasan
- `testlog.md` — 4A–4F, apa yang dicoba, hasilnya
- `findings.md` — HANYA yang lolos ambang bukti
- `poc/` — request/tx asli, screenshot

**Definisi selesai:** semua vektor di 4A–4F dicoba di semua target — ADA atau TIDAK ADA temuan, dua-duanya sah.
"Belum sempat coba" bukan hasil.

---

*Aturan tunggal: kalau sebuah aktivitas tidak bisa menghasilkan temuan ber-bayar, hentikan dan ganti aktivitas.*
