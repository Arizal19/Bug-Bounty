# AGHANIM - CHAIN TABLE v2 (every lead, with HOLDS/DIES + verbatim fact)

Method: `chain-to-impact` + `exploit-chain-graph`. Each lead walked link by link.
Each HOLDS has an artefact. Each DIES quotes the server string that killed it.
A chain ending at "server validates it" = UNPROVEN, not a negative.

===============================================================
NEW THIS ROUND (sibling API generation discovery)

## SIB - the sibling generation api.aghanim.com/checkout/v1
The checkout SPA is built with `Ew=new Tb({baseUrl: x1?PAY_API/order:HUB_API/checkout})`.
Both bases exist. pay-api is the hardened current gen; api.aghanim.com/checkout is the
sibling. chain-to-impact predicts legacy siblings lack the ACL the rewrite added.

CHAIN S1 - unauth order read (sibling) -> third-party PII
  Step 1 sibling reachable, order readable unauth?      HOLDS
           GET api.aghanim.com/checkout/v1/orders/ord_eLmDsjBSFCNjqgbY -> 200 full JSON
           (pay-api.aghanim.com/order/v1/orders/{id} -> 405 Method Not Allowed)
  Step 2 does it carry PII?                             HOLDS
           fields present: /ip_address (real IPv6 of creator), /user_agent,
           /player_id, /user_id, /receipt_number, /email (null unless set)
  Step 3 obtain a FOREIGN order id legitimately?         DIES
           gau/wayback gave archived ids ord_eJFSsftBTfhVeQSO, ord_eLdKMYAbaDyJbDGi
           -> 410 {"code":"order.expired"}  (orders TTL 24h)
           no listing route: /v1/orders?limit -> 404, /v1/orders/search -> 404,
           ?receipt_number= -> 404, ?payment_id= -> 404, ?player_id= -> 404
  => DIES AT STEP 3. Live ids are 15-char base62 (unguessable) and policy 4.2.14
     excludes identifier-guessing. Recorded as the single UNPROVEN/OOS-capped hop.

CHAIN S2 - sibling PATCH accepts what current gen rejects?  DIES
  PATCH /checkout/v1/orders/{id} {amount|total|items[].price|quantity|
        price_after_discount|currency|player_id|user_id|email} -> 200 each time
  re-read shows NOTHING changed except country.
  => DIES AT STEP 2. Same recompute guard as pay-api despite answering 200.

CHAIN S3 - sibling method matrix  DIES
  GET 200 | PATCH 200 | PUT 405 | DELETE 405 | OPTIONS 405 | HEAD 405
  no destructive verb exposed.

===============================================================
RETIRED-IDENTIFIER / STORE-ITEM SUBSTITUTION (gau harvest)

CHAIN R1 - public item id + foreign store_item -> inherit a discount
  Step 1 real pairs public?            HOLDS  gau: items/itm_X?store_item_id=stm_Y
  Step 2 cross-item stm accepted?      DIES   404 {"detail":"Store item not found"}
         all 12 permutations on hub.pixelgun3d.com AND 2 on 1945.falcongames.com
  Step 3 cross-site stm accepted?      DIES   404 Store item not found
  => DIES AT STEP 2. stm bound to (item, site).

CHAIN R2 - fallback_item_id / fallback_store_item_id substitution
  Step 1 params accepted?              HOLDS  200, params consumed
  Step 2 does fallback change price?   DIES   expensive item 1,750,000,000 IDR stays
         1,750,000,000 with pad=1,750,000,000; cheap item keeps its own 80% (pad 3,380,000)
  => DIES AT STEP 2. fallback is a display fallback, not a price override.

CHAIN R3 - store_id (special-offer store) applied to normal catalogue
  Step 1 archived store ids work?      HOLDS  ?store_id=str_eKfnxjsSXHI -> 200, n=10
  ("Welcome Pack" 80% off = the real special-offer store)
  Step 2 cross-game store id?          DIES   hub.pixelgun3d.com?store_id=str_eKfnxjsSXHI -> []
  Step 3 does it reprice unrelated items? DIES  store_id only filters to that store's own
         items; it cannot be attached to items/itm_* (no store_id param there)
  => DIES AT STEP 2/3. store_id is a filter, scoped to its site.

CHAIN R4 - archived order ids  -> 410 order.expired (see S1 step 3)

===============================================================
MONEY / SUBSCRIPTION

CHAIN M1 - subscription plan confusion (yearly for monthly price)
  Step 1 live subscription SKUs public?  HOLDS  type=subscription on demo (LIVE game):
           dsub_eItWksIeLmw Premium Pass  plans: monthly-plan 999 USD / yearly-plan 9999 USD
           dsub_eIxIZowizUz Fire Premium  plans: monthly-plan 1999 / yearly-plan 20000
  Step 2 orderable?                      DIES   POST /hub/v1/websites/demo/orders
           {items:[{store_item_id:stm_eItWlDRJxjY}]} -> 404 {"detail":"StoreItem not found"}
           same for stm_eIvAaEMtLfw / stm_eIxJbwOLuNd / item id / sku
  => DIES AT STEP 2. Cannot create a subscription order at all without a live checkout
     link or a store context; select_subscription_plan therefore unreachable.

CHAIN M2 - /v1/orders/{id}/pay (client marks it secure:!0)
  Step 1 locate base                     DIES  404 on /order, /hub, /checkout bases;
         405 on /order/v1/orders/x and 422 on /checkout/v1/links/x only
  => DIES AT STEP 1. No reachable pay route for a guest order.

CHAIN M3 - /ps/subscriptions (player PII + cancel/reactivate)
  Step 1 any auth bypass?                DIES 401 {"error":{"code":4}} for every param:
         (none),(order_id),(user_id),(email),(player_id),(paylink_user_id),(order)
         /ps/subscriptions/x/cancel -> 401 ; /reactivate -> 401 ; /{id}/resolve -> 404
  => DIES AT STEP 1. Auth enforced (client JS omission of `secure` is cosmetic).

CHAIN M4 - reward points -> zero/negative total
  Step 1 apply accepted?                 HOLDS 200
  Step 2 does it exceed balance?         DIES  fresh users -> applied=0;
         my user with 161 pts -> applied=161, total 2,900,000 -> 0 (1pt = 1 US cent)
         negative amount -> applied 0. CLAMPS TO AVAILABLE BALANCE.
  => DIES AT STEP 2. Legitimate redemption, not a bypass.

CHAIN M5 - daily reward accrual loop (live demo game)
  Step 1 visit_page callable repeatedly? HOLDS 204 x5
  Step 2 does it credit points?          DIES  user/reward_points -> [] before and after;
         user/virtual_currencies -> []; balances null. Granting is the integrator's
         webhook job, not the hub's.
  => DIES AT STEP 2.

CHAIN M6 - activity endpoint as grant primitive
  POST /v1/orders/{id}/activity/{r} on pay-api -> 404 page not found (all bases)

===============================================================
IDENTITY / AUTH

CHAIN I1 - hub authorize_user_id as auth bypass
  Step 1 mintable with no credential?    HOLDS demo -> 200 JWT (1y), is_registration true
  Step 2 real game?                      DIES   hub.pixelgun3d.com -> 401 Not Authenticated
  Step 3 demo game's configured methods? DIES   login_methods = ["user_id","game_link","apple"]
         -> player-id login IS enabled for that game => policy 4.4.6 carve-out
  => DIES AT STEP 2/3.

CHAIN I2 - cross-game identity merge (player_id global?)
  same player_id on demo vs wikipedia -> usr_eLmGDFcUsXn vs usr_eLmGDGacCfU
  => DIES AT STEP 1. Users are per-game.

CHAIN I3 - token confusion across trust domains
  hub JWT -> my-api 401 | pay-api 401 | dashboard-api 401 | s2s 401
  dashboard JWT -> my-api 401
  => DIES AT STEP 1 of every hop.

CHAIN I4 - JWT forgery
  HS256; alg:none rejected; weak secrets rejected; bound to game_id.

CHAIN I5 - dashboard -> hub session mint (cross-tenant SSO)
  POST /dashboard/v1/websites/search_website {search_string:<foreign>} -> 404 (all slugs)
  POST .../websites/{id}/create_exchange_token -> 404 (needs write role)
  => DIES AT STEP 1. Tenant-scoped.

CHAIN I6 - login identifier enumeration / OTP
  /v1/users/lookup -> {exists,email_verified,has_passkey} (by design, 4.2.10)
  start_login -> 429 after a few; confirm_email/confirm_login_via_ott reject junk tokens (403/401)

===============================================================
STORED XSS
CHAIN X1 - player name -> hub render
  Step 1 stored raw?                     HOLDS PATCH user/me name -> <img src=x onerror=...>,
         returned raw, persisted
  Step 2 any render sink?                DIES  all 132 hub chunks enumerated; the only
         unescaped-HTML sinks are Linkify (wired to item/news description = integrator
         content, OOS 4.4.3), LexicalContent, and GA/GTM/pixel/custom_code_js.
         No sink consumes player name.
  Step 3 empirical render on live hub?   DIES  manabuff.com/go/login?token=JWT and
         manabuff.com/ -> img[src=x]=0, <b>BBXSS</b>=0, onerror in DOM=false, dialogs=0
  => DIES AT STEP 2. Storage hygiene, not XSS.

===============================================================
UPLOAD / SSRF
CHAIN U1 - upload:any bucket -> cross-tenant asset overwrite -> content injection
  Step 1 bucket accepted with my X-Company-Id?  DIES
         bucket=test -> 400 "Invalid bucket" (validated first)
         bucket in {news,hub,dashboard,video,webm,customer-avatars,files,avatar,
         achievement} -> 403 Forbidden
  Step 2 /ingest SSRF (url param)?              DIES 403 Forbidden
  => DIES AT STEP 1. Write role required before bucket is consulted.

===============================================================
SDK / ESTATE
CHAIN K1 - public hub -> sdk_key -> sdk-api (in scope, untested)
  Step 1 sweep 17 public hub websites for non-null sdk_key   DIES all null
  Step 2 sdk-api unauth?  /sdk/v1/{orders,items,config,players} -> 401
  => DIES AT STEP 1. Needs a real integrator's shipped web client.

CHAIN Z1 - subdomain estate
  subfinder 192 subs; policy lists 15 exact .com hosts + *.aghanim.app.
  admin-api, account-api, buy-api, api-dev, api.staging, datahouse, cpanel NOT listed
  => deliberately untouched (engagement risk).

CHAIN Z2 - Next.js RSC (_rsc= x28 in archive)
  hub.pixelgun3d.com/?_rsc=1ardl -> 200, identical static HTML (278906 bytes) for
  any token => no flight-data leak.

CHAIN Z3 - pagination/limit abuse
  /hub/v1/websites/demo/items?limit=1000|-1|0 -> always n=54, archived=0
  => limit ignored; no hidden/archived SKU dump.

===============================================================
VERDICT
Reachable surface (guest + read-only tenant + demo hub identity) is exhausted.
13 chain families, ~40 individual links tested this round. One asymmetry found
(SIB-01 unauth order read incl. creator IP/UA on the sibling generation, where
current gen returns 405) and it is capped by policy 4.2.14 plus a 24h TTL that
turns archived ids into 410. Recorded as UNPROVEN/OOS-capped, NOT as a finding.

Three hops remain unproven, each on exactly one credential:
  OA phone+SMS OTP      -> my-api player surface (payment_options, subscriptions,
                           rewards, /v1/users/me)
  OB write role         -> api_keys -> S2S -> 179 ops incl. webhooks/{id}/reveal
                           (webhook secret => forge item.add => free entitlements)
  OC real sdk_ key      -> sdk-api /sdk/v1/*
