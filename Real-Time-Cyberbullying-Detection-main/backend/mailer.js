// mailer.js
const fs = require("fs");
const path = require("path");
const { google } = require("googleapis");
const nodemailer = require("nodemailer");

// Load OAuth2 credentials
const CREDENTIALS_PATH = path.join(__dirname, "credentials.json");
const TOKEN_PATH = path.join(__dirname, "token.json");

async function authorize() {
  const { client_secret, client_id, redirect_uris } = JSON.parse(
    fs.readFileSync(CREDENTIALS_PATH)
  ).installed;

  const oAuth2Client = new google.auth.OAuth2(
    client_id,
    client_secret,
    redirect_uris[0]
  );

  // Check for existing token
  if (fs.existsSync(TOKEN_PATH)) {
    const token = fs.readFileSync(TOKEN_PATH);
    oAuth2Client.setCredentials(JSON.parse(token));
    return oAuth2Client;
  }

  // Generate new auth URL
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: "offline",
    scope: ["https://mail.google.com/"],
  });

  console.log("Authorize this app by visiting this URL:\n", authUrl);
  const readline = require("readline").createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise((resolve, reject) => {
    readline.question("Enter the code from that page here: ", (code) => {
      readline.close();
      oAuth2Client.getToken(code, (err, token) => {
        if (err) return reject(err);
        oAuth2Client.setCredentials(token);
        fs.writeFileSync(TOKEN_PATH, JSON.stringify(token));
        console.log("✅ Token stored to", TOKEN_PATH);
        resolve(oAuth2Client);
      });
    });
  });
}

async function sendEmail(to, subject, text) {
  const auth = await authorize();

  const transporter = nodemailer.createTransport({
    service: "gmail",
    auth: {
      type: "OAuth2",
      user: "dhana172022@gmail.com", // your Gmail
      clientId: auth._clientId,
      clientSecret: auth._clientSecret,
      refreshToken: auth.credentials.refresh_token,
      accessToken: auth.credentials.access_token,
    },
  });

  const mailOptions = {
    from: "dhana172022@gmail.com",
    to,
    subject,
    text,
  };

  await transporter.sendMail(mailOptions);
  console.log("✅ Email sent successfully to", to);
}

// Run from CLI: node mailer.js receiver@gmail.com "Subject" "Body"
const [,, to, subject, text] = process.argv;
if (to && subject && text) {
  sendEmail(to, subject, text).catch(console.error);
}

module.exports = { sendEmail };
