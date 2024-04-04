// background.js
chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    if (details.url.startsWith("https://www.example.com/")) {
      // Redirigir a otro dominio
      return { redirectUrl: "https://www.another-site.com/" };
    }
  },
  { urls: ["*://*.example.com/*"] },
  ["blocking"]
);