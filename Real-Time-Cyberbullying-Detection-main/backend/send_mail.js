// send_mail.js
const sendMail = require("./mailer");

const [,, to, subject, message] = process.argv;

if (!to || !subject || !message) {
  console.error("❌ Missing arguments. Usage: node send_mail.js <to> <subject> <message>");
  process.exit(1);
}

sendMail(to, subject, message)
  .then(() => console.log("✅ Email sent successfully"))
  .catch(err => console.error("❌ Failed to send email:", err));
