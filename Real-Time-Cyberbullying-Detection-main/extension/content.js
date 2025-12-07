// content.js
const DEBUG = true;
function log(...args) { if (DEBUG) console.log("[CB Ext]", ...args); }
// ======= Try to get Google Meet organiser email =======
function getMeetOrganizerEmail() {
  // Try from visible DOM (People list or host chip)
  const emailElement = document.querySelector('[aria-label*="@gmail.com"]');
  if (emailElement) {
    const match = emailElement.getAttribute("aria-label").match(/[\w.-]+@[\w.-]+/);
    if (match) return match[0];
  }

  // Fallback: scan page text for any Gmail addresses (usually includes organiser)
  const allText = document.body.innerText;
  const match = allText.match(/[\w.-]+@[\w.-]+/);
  if (match) return match[0];

  return null;
}

function sendOrganizerEmailToBackend() {
  const email = getMeetOrganizerEmail();
  if (!email) {
    log("❌ Organiser email not found yet");
    return;
  }
  log("📧 Sending organiser email to backend:", email);
  fetch("http://127.0.0.1:5000/update-organiser", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email })
  })
  .then(res => res.json())
  .then(data => log("✅ Organiser email updated:", data))
  .catch(err => log("❌ Failed to send organiser email:", err));
}

// ======= De-duplication + Throttle =======
let lastSentAt = 0;
const recentTexts = new Map();

function shouldSend(text) {
  if (!text || text.length < 2) return false;
  const now = Date.now();
  if (now - lastSentAt < 800) return false; // throttle requests (<1/sec)
  lastSentAt = now;
  const last = recentTexts.get(text);
  if (last && now - last < 5000) return false; // ignore repeat within 5 s
  recentTexts.set(text, now);
  if (recentTexts.size > 300) recentTexts.delete(recentTexts.keys().next().value);
  return true;
}

// ======= Banner =======
function showBanner(text, score) {
  const id = "cb-detector-banner";
  document.getElementById(id)?.remove();

  const banner = document.createElement("div");
  banner.id = id;
  banner.innerText = `⚠️ Toxic message detected: "${text}" (score: ${Number(score).toFixed(2)})`;
  Object.assign(banner.style, {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    background: "red",
    color: "#fff",
    padding: "10px",
    zIndex: 2147483647,
    fontSize: "14px",
    textAlign: "center",
    fontFamily: "Arial, sans-serif"
  });
  document.body.prepend(banner);
  setTimeout(() => banner.remove(), 5000);
}

// ======= Send to backend =======
function sendForAnalysis(text, source) {
  if (!shouldSend(text)) return;
  log(`→ Sending (${source}):`, text);
  chrome.runtime.sendMessage({
    action: "analyzeText",
    data: text,
    meta: { source }
  });
}

// ======= Hook outgoing messages =======
function hookOutgoing() {
  const chatBox = document.querySelector("textarea");
  if (!chatBox || chatBox.dataset.hooked) return;
  chatBox.dataset.hooked = "true";
  chatBox.addEventListener("keydown", e => {
    if (e.key === "Enter" && !e.shiftKey) {
      const text = chatBox.value.trim();
      sendForAnalysis(text, "self");
    }
  });
}

// ======= Hook incoming messages =======
function hookIncoming() {
  const chatPanel = document.querySelector('[aria-live="polite"]');
  if (!chatPanel || chatPanel.dataset.hooked) return;
  chatPanel.dataset.hooked = "true";

  const observer = new MutationObserver(muts => {
    for (const m of muts) {
      for (const node of m.addedNodes) {
        const text = node.innerText?.trim();
        if (text) sendForAnalysis(text, "other");
      }
    }
  });


  
//   const observer = new MutationObserver(muts => {
//   for (const m of muts) {
//     for (const node of m.addedNodes) {
//       const text = node.innerText?.trim();
//       if (!text) continue;

//       // Try to get the sender email or name
//       const senderEl = node.closest('[data-sender-name]') || node.querySelector('[data-sender-name]');
//       const senderName = senderEl ? senderEl.getAttribute('data-sender-name') : "unknown";

//       // Send both message and sender info to background
//       sendForAnalysis(JSON.stringify({ text, senderName }), "other");
//     }
//   }
// });











  observer.observe(chatPanel, { childList: true, subtree: true });
  log("Incoming observer attached.");
}

// ======= Listen for backend alerts =======
chrome.runtime.onMessage.addListener(msg => {
  if (msg.action === "showAlert") {
    showBanner(msg.text || "", msg.score ?? 0);
  }
});

// ======= Periodically retry hooks =======
setInterval(() => {
  hookOutgoing();
  hookIncoming();
}, 2000);

log("[CB Ext] content.js active ✅");
// Try sending organiser email once page fully loads


setTimeout(sendOrganizerEmailToBackend, 5000);



