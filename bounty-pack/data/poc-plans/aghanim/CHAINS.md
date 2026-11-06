# AGHANIM - CHAIN-ATTACK ANALYSIS
Every chain below was executed link-by-link; the break point is recorded.
P# = primitive. [H] = held by attacker, [X] = failed.

## P1 [H] Unauth guest order creation
POST pay-api /order/v1/links/lnk_eHriLMNNvUxvbFHm?player_id=<ANY>
  -> 201 {id, game_id, company_id, user_id, items[], amount, total, currency,
          return_url, checkout_settings, feature_flags, sandbox:true}
Gives: full order object + a user_id per arbitrary player_id. No auth at all.

## P2 [H] Unauth payment-record creation
POST /ps/cards/calculate {order_id, billing_address, skip_address_validation}
  -> 200 {payment.id=pmt_..., amount, total_taxes, payment_form}
POST /ps/cards/submit -> 200 (real sandbox charge; order -> paid -> delivered)
Gives: write primitive, no auth.

## P3 [H] Unauth payment read
GET /ps/payments/{pmt} -> 200 {email masked f***1@..., amount, country, taxes,
                               payment_method_name}
GET /ps/orders/{order}/payments/last -> same
Gives: payment metadata. Masked email, NO card data (no last4/brand/pan).
=> needs a foreign pmt_/ord_ id => guessing identifier => OOS 4.2.14.

## P4 [H] Unauth hub JWT (demo game only)
POST api /hub/v1/websites/{slug}/auth/authorize_user_id {user_id:<any>}
  -> 200 {token HS256 1yr, user{id,player_id}, is_registration:true}
Real games (hub.pixelgun3d.com) -> 401 (game's player.verify webhook gates it).
Gives: hub-scoped identity on the DEMO game only.

## P5 [H] Read-only dashboard role in own tenant
Auth0 passwordless -> cmr_/com_eBRDihmnOJa/gm_eDTjNboxMxn, role "user" = *:read.

## P6 [H] Public per-game data (real games)
GET /hub/v1/websites/{slug}/{items, items/{itm}?store_item_id=, item_categories,
    daily_rewards, leaderboards, achievements, news, sections, loyalty, pages}
Gives: real item ids, real store_item_ids, real prices, discount_pct.

===============================================================
CHAIN 1 - guest order -> order mutation -> discounted/free purchase
  P1 -> PATCH /order/v1/orders/{id} with items[].price | quantity | store_item_id
        | discount_percent | price_after_discount | is_free_item | amount | total
        | currency | coupon_code | promo_code
  RESULT: HTTP 200 every time, but resolve() shows NOTHING changed.
  BREAK at link 2 (mutation silently ignored, server recomputes from source).
  Note: `country` DOES apply and re-prices correctly across ID/JP/BR/TR/NG/US/ZZ
        (differences = the game's own regional price points, not an FX bug).

CHAIN 2 - guest order -> cross-user order/identity pivot
  P1 -> PATCH {user_id|player_id|email} -> ignored
  P1 -> POST resolve {user_id|player_id|email} -> ignored
  BREAK at link 2.

CHAIN 3 - public item enumeration -> mismatched store_item -> price manipulation
  P6 (itm+stm pairs) -> GET items/itm_A?store_item_id=stm_B (same site)
  RESULT: 404 on all 12 cross combinations; own pair = correct 50%/76% discount.
  BREAK at link 2 (stm strictly bound to its item AND its site).

CHAIN 4 - hub JWT -> order creation with client-controlled price
  P4 -> POST /hub/v1/websites/{slug}/orders {items:[{sku,name,price,is_custom}]}
  RESULT: 400 order.store_item_required (client price never trusted).
          foreign store_item_id -> 404 StoreItem not found.
  BREAK at link 2.

CHAIN 5 - hub JWT -> mass assignment -> wallet/attribute escalation
  P4 -> PATCH /hub/v1/websites/{slug}/user/me {balances, attributes, marketing_consent}
  RESULT: only `name` persists; balances/attributes silently dropped.
  BREAK at link 2.

CHAIN 6 - hub JWT -> token confusion across trust domains
  hub JWT -> my-api /api/v1/users/me          -> 401
  hub JWT -> pay-api /ps/payment_options      -> 401
  hub JWT -> dashboard-api /dashboard/v1/*    -> 401
  hub JWT -> api /s2s/v1/orders               -> 401
  dashboard JWT -> my-api /api/v1/users/me    -> 401
  BREAK at link 1 of every cross-domain hop (separate audience/secrets).

CHAIN 7 - payment replay -> duplicate entitlement
  paid order -> POST /ps/cards/submit again -> 400 code 8
  -> POST /wh/{ps}/s/{capture,3ds_complete,payment_data} -> 404 / NOT_FOUND
  BREAK at link 1 (idempotency enforced; provider callbacks not public).

CHAIN 8 - read-only role -> global (non-company-scoped) endpoint -> cross-tenant
  P5 -> /v1/admin/search_payment?order_id=<mine> -> 404 (even for own order)
  P5 -> /v1/campaigns, /v1/companies/all_games   -> 404 / own tenant only
  P5 -> /v1/admin/articles_migrations, /v1/creators/terms -> 403
  240 company/game-scoped GETs vs another tenant -> 403 all
  BREAK at link 1 (authz enforced per tenant; /admin role-gated).

CHAIN 9 - read-only role -> hub session mint -> cross-tenant hub takeover
  P5 -> POST /v1/websites/search_website {search_string:<foreign slug>} -> 404
  P5 -> POST .../websites/{id}/create_exchange_token -> 404 (needs write role)
  BREAK at link 1 (search_website is tenant-scoped).

CHAIN 10 - upload service -> cross-tenant asset overwrite -> content injection
  P5 -> POST upload.aghanim.com/upload {bucket:<name>} + X-Company-Id:<mine>
  RESULT: bucket=test -> "Invalid bucket" (validated first);
          bucket in {news,hub,dashboard,video,webm,customer-avatars,files,
                     avatar,achievement} -> 403 Forbidden.
  P5 -> /ingest {url,bucket} (SSRF primitive) -> 403.
  BREAK at link 1 (write role required before bucket is even consulted).

CHAIN 11 - stored XSS: player name -> hub render
  P4 -> PATCH user/me {name:"<img src=x onerror=...>"} -> stored RAW, returned raw
  -> enumerated every dangerouslySetInnerHTML in all 132 hub chunks:
     * Linkify (Ci0lKHjb.js) injects unescaped non-URL text, BUT wired only to
       item/news `description` = integrator content => OOS 4.4.3
     * LexicalContent = editor HTML (integrator)
     * GA/GTM/MetaPixel/Termly/custom_code_js = integrator config
     * NO sink consumes the player name
  -> empirical: manabuff.com/go/login?token=<jwt> and manabuff.com/ ->
     img[src=x]=0, <b>BBXSS</b>=0, onerror in DOM=false, dialogs=0
  BREAK at link 2 (no render sink). Raw storage + safe render = hygiene, not XSS.

CHAIN 12 - reward points -> zero-total order
  P1 -> POST apply_reward_points {amount:100000}
  one order: total 2,900,000 -> 0, applied_reward_points=161 (=USD 1.61 = 100pts/$1)
  8 fresh orders: HTTP 200 but applied=0, total unchanged
  => 161 was a real balance on that user; endpoint CLAMPS to available balance.
  UNREPRODUCIBLE => not reportable under the 3x validation rule.

CHAIN 13 - subdomain estate -> out-of-scope admin surface
  subfinder -> 192 subs; policy lists 15 exact .com hosts + *.aghanim.app.
  admin-api, account-api, buy-api, api-dev, api.staging, datahouse, cpanel are
  NOT listed => deliberately NOT touched (engagement risk, not laziness).

===============================================================
STILL-OPEN CHAINS (each blocked on ONE identity primitive)

OA. phone + SMS OTP -> my-api player surface
    /v1/auth/start_login requires phone; signup requires {email,phone};
    verification_type=phone -> "Email verification required".
    Unlocks: saved payment options (/ps/payment_options), subscriptions
    (/ps/subscriptions/{id}/{cancel,reactivate,resolve,calculate,pay_by_token}),
    reward point balances, /v1/users/me, cross-user comparisons.

OB. write role (company invite /join/:inviteId, or creator approval)
    -> POST .../api_keys (403 now) -> S2S Bearer
    -> all 179 S2S ops: /v1/orders/{id}/refund, /v1/payments/{n}/dispute_evidence,
       /v1/players/{p}/subscriptions/{s}/{transfer,upgrade},
       /v1/webhooks/{id}/reveal, /v1/users/{authenticate,authorize},
       plus cross-tenant enforcement of every company_id/game_id.

OC. public SDK key (sdk_... / sdk_sandbox_...) from a real web-game client
    sdk-api is in scope; /sdk/v1/{orders,items,config,players} all 401 today.
    Key is documented "safe to expose in the game client" => only testable
    against a real integrator's shipped client.
