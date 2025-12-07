// background.js
const DEBUG = true;
const API_URL = "http://127.0.0.1:5000/analyze";  // Flask backend route

function log(...args) { if (DEBUG) console.log("[CB Ext BG]", ...args); }

chrome.runtime.onMessage.addListener((msg, sender) => {
  if (msg.action === "analyzeText") {
    const text = msg.data;
    if (!text) return;

    log("Analyze request:", text);

    (async () => {
      try {
        const resp = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: "chrome-user",
            message: text,
            timestamp: new Date().toISOString()
          })
        });

        const result = await resp.json();
        log("Backend result:", result);

        const riskScore = result.score ?? result.risk_score ?? 0;
        const flagged = result.flagged ?? (riskScore > 0.5);

        if (flagged) {
          chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
            for (const tab of tabs) {
              chrome.tabs.sendMessage(tab.id, {
                action: "showAlert",
                text: result.text || text,
                score: riskScore
              }, () => {
                if (chrome.runtime.lastError) {
                  log("sendMessage error:", chrome.runtime.lastError.message);
                }
              });
            }
          });
        }
      } catch (e) {
        log("Error contacting backend:", e);
      }
    })();

    return true; // keep async channel open
  }
});












// // background.js
// const DEBUG = true;
// const API_URL = "http://127.0.0.1:5000/analyze";  // Flask backend route

// function log(...args) { if (DEBUG) console.log("[CB Ext BG]", ...args); }

// chrome.runtime.onMessage.addListener((msg, sender) => {
//   if (msg.action === "analyzeText") {
//     let payload;
//     try {
//       payload = JSON.parse(msg.data);
//     } catch {
//       // if msg.data is plain text
//       payload = { text: msg.data, senderName: "chrome-user" };
//     }

//     const { text, senderName } = payload;
//     if (!text) return;

//     log("Analyze request:", text, "from:", senderName);

//     (async () => {
//       try {
//         const resp = await fetch(API_URL, {
//           method: "POST",
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify({
//             user_id: senderName || "chrome-user",
//             message: text,
//             timestamp: new Date().toISOString()
//           })
//         });

//         const result = await resp.json();
//         log("Backend result:", result);

//         const riskScore = result.score ?? result.risk_score ?? 0;
//         const flagged = result.flagged ?? (riskScore > 0.5);

//         if (flagged) {
//           chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
//             for (const tab of tabs) {
//               chrome.tabs.sendMessage(tab.id, {
//                 action: "showAlert",
//                 text: result.text || text,
//                 score: riskScore
//               }, () => {
//                 if (chrome.runtime.lastError) {
//                   log("sendMessage error:", chrome.runtime.lastError.message);
//                 }
//               });
//             }
//           });
//         }
//       } catch (e) {
//         log("Error contacting backend:", e);
//       }
//     })();

//     return true; // keep async channel open
//   }
// });













