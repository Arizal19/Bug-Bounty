<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#FFFFFF" />

    <meta
      name="description"
      content="Aghanim is an integrated commerce, liveops automation, community engagement, and payments platform for mobile games."
    />
    <meta property="og:title" content="Direct-to-consumer enablement for mobile games | Aghanim" />
    <meta
      property="og:description"
      content="Aghanim is an integrated commerce, liveops automation, community engagement, and payments platform for mobile games."
    />
    <meta property="og:url" content="https://aghanim.com" />
    <meta property="og:site_name" content="aghanim.com" />
    <meta property="og:locale" content="en_US" />
    <meta property="og:image:type" content="website" />
    <meta property="og:image" content="https://static-corp.aghanim.com/og_193da66018.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Aghanim" />
    <meta property="og:type" content="website" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Direct-to-consumer enablement for mobile games | Aghanim" />
    <meta
      name="twitter:description"
      content="Aghanim is an integrated commerce, liveops automation, community engagement, and payments platform for mobile games."
    />
    <meta name="twitter:image:type" content="website" />
    <meta name="twitter:image" content="https://static-corp.aghanim.com/og_193da66018.png" />
    <meta name="twitter:image:width" content="1200" />
    <meta name="twitter:image:height" content="630" />
    <meta name="twitter:image:alt" content="Aghanim" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
    />

    <meta http-equiv="cache-control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="pragma" content="no-cache" />
    <meta http-equiv="expires" content="0" />

    
    

    <title>Dashboard | Aghanim</title>

    <style>
      html,
      body,
      #root {
        min-height: 100%;
      }

      body {
        margin: 0;
        background: #fff;
      }

      #root:empty {
        display: flex;
        min-height: 100svh;
        background: #fff;
      }

      #boot-sidebar {
        display: none;
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
        width: 240px;
        box-sizing: border-box;
        padding: 8px 12px;
        background: #f1f5f9;
      }

      @media (min-width: 768px) {
        #root:empty + #boot-sidebar {
          display: block;
        }
      }

      #boot-sidebar .sk {
        background: #e6ebf0;
        border-radius: 4px;
      }

      #boot-sidebar .sk-switcher {
        display: flex;
        align-items: center;
        gap: 8px;
        height: 32px;
        margin-bottom: 12px;
      }

      #boot-sidebar .sk-logo {
        width: 32px;
        height: 32px;
        flex-shrink: 0;
        border-radius: 8px;
      }

      #boot-sidebar .sk-item {
        display: flex;
        align-items: center;
        gap: 12px;
        height: 30px;
        padding: 0 8px;
        box-sizing: border-box;
      }

      #boot-sidebar .sk-item + .sk-item {
        margin-top: 2px;
      }

      #boot-sidebar .sk-icon {
        width: 18px;
        height: 18px;
        border-radius: 5px;
        flex-shrink: 0;
      }

      #boot-sidebar .sk-bar {
        height: 20px;
      }

      #boot-sidebar .sk-footer {
        position: absolute;
        right: 12px;
        bottom: 8px;
        left: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        height: 32px;
        padding: 2px;
        box-sizing: border-box;
      }

      #boot-sidebar .sk-company {
        width: 28px;
        height: 28px;
        flex-shrink: 0;
        border-radius: 6px;
      }

      #boot-navbar {
        display: none;
        position: fixed;
        top: 0;
        right: 0;
        left: 240px;
        max-width: 1400px;
        margin: 0 auto;
        height: 48px;
        box-sizing: border-box;
        padding: 0 24px;
        align-items: center;
        justify-content: flex-end;
        gap: 4px;
      }

      @media (min-width: 768px) {
        #root:empty ~ #boot-navbar {
          display: flex;
        }
      }

      #boot-navbar .sk {
        background: rgba(0, 0, 0, 0.04);
        border-radius: 4px;
      }

      #boot-navbar .sk-tbar {
        display: none;
        height: 20px;
        margin-right: 12px;
      }

      @media (min-width: 1024px) {
        #boot-navbar .sk-tbar {
          display: block;
        }
      }

      #boot-navbar .sk-btn {
        width: 28px;
        height: 28px;
        flex-shrink: 0;
        border-radius: 8px;
      }

      #boot-navbar .sk-avatar {
        width: 28px;
        height: 28px;
        flex-shrink: 0;
        margin-left: 8px;
        border-radius: 9999px;
      }

    </style>

    
    <script>
      window.TERMLY_CUSTOM_BLOCKING_MAP = {
        'auth0.aghanim.com': 'essential',
        'auth.aghanim.com': 'essential',
        'static.aghanim.com': 'essential',
        'https://dashboard-api.aghanim.com': 'essential',
        'https://newton-api.aghanim.com': 'essential',
        'gravatar.com': 'essential',
        'algolia.net': 'essential',
        'aghanim.app': 'essential',
        'static-platform.aghanim.com': 'essential',
        'static-platform.aghanim.com': 'essential',
      };
    </script>

    <script>
      if (location.href.indexOf('http://localhost') == -1) {
        !(function (t, e) {
          var o, n, p, r;
          e.__SV ||
            ((window.posthog = e),
            (e._i = []),
            (e.init = function (i, s, a) {
              function g(t, e) {
                var o = e.split('.');
                (2 == o.length && ((t = t[o[0]]), (e = o[1])),
                  (t[e] = function () {
                    t.push([e].concat(Array.prototype.slice.call(arguments, 0)));
                  }));
              }

              (((p = t.createElement('script')).type = 'text/javascript'),
                (p.async = !0),
                (p.src = s.api_host + '/static/array.js'),
                (r = t.getElementsByTagName('script')[0]).parentNode.insertBefore(p, r));
              var u = e;
              for (
                void 0 !== a ? (u = e[a] = []) : (a = 'posthog'),
                  u.people = u.people || [],
                  u.toString = function (t) {
                    var e = 'posthog';
                    return ('posthog' !== a && (e += '.' + a), t || (e += ' (stub)'), e);
                  },
                  u.people.toString = function () {
                    return u.toString(1) + '.people (stub)';
                  },
                  o =
                    'capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys'.split(
                      ' ',
                    ),
                  n = 0;
                n < o.length;
                n++
              ) {
                g(u, o[n]);
              }
              e._i.push([i, s, a]);
            }),
            (e.__SV = 1));
        })(document, window.posthog || []);
        posthog.init('phc_IM8qNhwep8GecDOu3yJbFhSdU5gnXH7KQdPFDU9gR7', {
          api_host: 'https://us.i.posthog.com',
          person_profiles: 'always',
        });
      }
    </script>

    <script
      defer
      type="text/javascript"
      src="https://app.termly.io/resource-blocker/b17bd80f-e340-4bde-980b-21391cc6f94d?autoBlock=on"
    ></script>
    
    <script type="module" crossorigin src="/assets/index-mrM4ppFe.js"></script>
    <link rel="modulepreload" crossorigin href="/assets/rolldown-runtime-CoyOC2v3.js">
    <link rel="stylesheet" crossorigin href="/assets/index-CvglY6Io.css">
  <link rel="manifest" href="/manifest.webmanifest"></head>
  <body>
    <div id="root"></div>
    <div id="boot-sidebar" aria-hidden="true">
      <div class="sk-switcher">
        <span class="sk sk-logo"></span>
        <span class="sk sk-bar" style="width: 120px"></span>
      </div>
      <div class="sk-item">
        <span class="sk sk-icon"></span><span class="sk sk-bar" style="width: 64%"></span>
      </div>
      <div class="sk-item">
        <span class="sk sk-icon"></span><span class="sk sk-bar" style="width: 78%"></span>
      </div>
      <div class="sk-item">
        <span class="sk sk-icon"></span><span class="sk sk-bar" style="width: 55%"></span>
      </div>
      <div class="sk-item">
        <span class="sk sk-icon"></span><span class="sk sk-bar" style="width: 70%"></span>
      </div>
      <div class="sk-item">
        <span class="sk sk-icon"></span><span class="sk sk-bar" style="width: 50%"></span>
      </div>
      <div class="sk-item">
        <span class="sk sk-icon"></span><span class="sk sk-bar" style="width: 55%"></span>
      </div>
      <div class="sk-item">
        <span class="sk sk-icon"></span><span class="sk sk-bar" style="width: 70%"></span>
      </div>
      <div class="sk-item">
        <span class="sk sk-icon"></span><span class="sk sk-bar" style="width: 50%"></span>
      </div>
      <div class="sk-footer">
        <span class="sk sk-company"></span>
        <span class="sk sk-bar" style="width: 96px"></span>
      </div>
    </div>
    <div id="boot-navbar" aria-hidden="true">
      <span class="sk sk-tbar" style="width: 80px"></span>
      <span class="sk sk-btn"></span>
      <span class="sk sk-avatar"></span>
    </div>
  </body>
</html>
