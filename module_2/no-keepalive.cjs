// Work around node-fetch 2.x "Premature close" errors on Node 20, whose default
// https agent reuses connections (keepAlive), by restoring a non-keepalive agent.
const http = require("http");
const https = require("https");
http.globalAgent = new http.Agent({ keepAlive: false });
https.globalAgent = new https.Agent({ keepAlive: false });
