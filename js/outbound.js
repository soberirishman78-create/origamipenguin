/*
 * Outbound Amazon affiliate click tracking for OrigamiPenguin.com
 *
 * Sends a tiny beacon (page path + link ASIN) to a Cloudflare Worker
 * endpoint so we can measure: landing page -> Amazon clicks.
 *
 * PRIVACY: no cookies, no user identifiers, no personal data.
 * Only the current page path and the clicked product link are recorded.
 *
 * SETUP: deploy the click-counter Worker (see docs in repo owner notes),
 * then set CLICK_ENDPOINT to its URL. While CLICK_ENDPOINT is empty,
 * this script does nothing.
 */
(function () {
  var CLICK_ENDPOINT = ''; // e.g. 'https://clicks.origamipenguin.workers.dev'
  if (!CLICK_ENDPOINT) return;

  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href*="amazon.com"]') : null;
    if (!a) return;
    try {
      var payload = JSON.stringify({
        page: location.pathname,
        href: a.getAttribute('href')
      });
      if (navigator.sendBeacon) {
        navigator.sendBeacon(CLICK_ENDPOINT, payload);
      }
    } catch (err) { /* never block the navigation */ }
  }, true);
})();
