#!/usr/bin/env python3
# ==============================================================================
# Brave Free Origin GUI for macOS
# Standalone local GUI with live checkboxes, presets, and 1-click apply
# ==============================================================================

import os
import sys
import json
import subprocess
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import urllib.parse

PORT = 45678

POLICIES = [
    # AI & Bloat
    {"key": "BraveAIChatEnabled", "type": "bool", "val": "false", "title": "Strip Leo AI Chat", "desc": "Removes Leo AI from sidebar, URL bar, and context menus", "category": "AI & Bloat", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "BraveSpeedreaderDisabled", "type": "bool", "val": "true", "title": "Disable Speedreader", "desc": "Disables Speedreader feature and its telemetry hooks", "category": "AI & Bloat", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": False},
    {"key": "BraveWaybackMachineDisabled", "type": "bool", "val": "true", "title": "Disable Wayback Machine", "desc": "Stops Wayback Machine prompt on 404 pages", "category": "AI & Bloat", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": False},
    {"key": "BravePlaylistDisabled", "type": "bool", "val": "true", "title": "Disable Media Playlist", "desc": "Disables Brave media playlist feature", "category": "AI & Bloat", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": False},

    # Crypto & Web3
    {"key": "BraveWalletDisabled", "type": "bool", "val": "true", "title": "Disable Crypto Wallet", "desc": "Disables Web3 crypto wallet integration entirely", "category": "Crypto & Web3", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "BraveRewardsDisabled", "type": "bool", "val": "true", "title": "Disable Brave Rewards", "desc": "Turns off BAT rewards, sponsored ads, and wallet popups", "category": "Crypto & Web3", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},

    # Cloud Services
    {"key": "BraveVPNDisabled", "type": "bool", "val": "true", "title": "Disable Brave VPN", "desc": "Removes Brave VPN UI, service hooks, and prompts", "category": "Services", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "BraveNewsDisabled", "type": "bool", "val": "true", "title": "Disable Brave News", "desc": "Removes Brave News / Today feeds from new tab pages", "category": "Services", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "BraveTalkDisabled", "type": "bool", "val": "true", "title": "Disable Brave Talk", "desc": "Disables built-in Brave Talk video calling", "category": "Services", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": False},
    {"key": "TorDisabled", "type": "bool", "val": "true", "title": "Disable Tor Windows", "desc": "Disables built-in Tor routing private windows", "category": "Services", "risk": "Low", "origin": True, "boost": True, "max": True, "quick": True},

    # Telemetry & Analytics
    {"key": "BraveP3AEnabled", "type": "bool", "val": "false", "title": "Kill P3A Analytics", "desc": "Disables Privacy-Preserving Product Analytics completely", "category": "Telemetry", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "BraveStatsPingEnabled", "type": "bool", "val": "false", "title": "Kill Usage Stats Ping", "desc": "Stops periodic telemetry usage pings to Brave servers", "category": "Telemetry", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "MetricsReportingEnabled", "type": "bool", "val": "false", "title": "Kill Crash & Metrics", "desc": "Stops Chromium crash and metric telemetry reports", "category": "Telemetry", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "BraveWebDiscoveryEnabled", "type": "bool", "val": "false", "title": "Kill Web Discovery Project", "desc": "Disables Web Discovery Project browsing data collection", "category": "Telemetry", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "UrlKeyedAnonymizedDataCollectionEnabled", "type": "bool", "val": "false", "title": "Kill URL History Telemetry", "desc": "Stops URL-keyed browsing history data collection", "category": "Telemetry", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "UserFeedbackAllowed", "type": "bool", "val": "false", "title": "Disable Feedback Surveys", "desc": "Prevents in-browser feedback surveys and prompts", "category": "Telemetry", "risk": "Safe", "origin": False, "boost": True, "max": True, "quick": False},
    {"key": "WebRtcEventLogCollectionAllowed", "type": "bool", "val": "false", "title": "Disable WebRTC Event Logs", "desc": "Prevents WebRTC diagnostic log collection", "category": "Telemetry", "risk": "Safe", "origin": False, "boost": True, "max": True, "quick": False},

    # Shields & Privacy Hardening
    {"key": "DefaultBraveAdblockSetting", "type": "integer", "val": "2", "title": "Aggressive Ad Blocking", "desc": "Enforces Aggressive Ad & Tracker blocking in Brave Shields", "category": "Shields", "risk": "Low", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "DefaultBraveFingerprintingV2Setting", "type": "integer", "val": "3", "title": "Strict Fingerprinting Protection", "desc": "Enforces Strict Fingerprinting Protection in Shields", "category": "Shields", "risk": "Low", "origin": False, "boost": True, "max": True, "quick": False},
    {"key": "DefaultBraveReferrersSetting", "type": "integer", "val": "2", "title": "Strict Referrer Stripping", "desc": "Strips cross-origin referrer headers", "category": "Shields", "risk": "Low", "origin": False, "boost": True, "max": True, "quick": False},
    {"key": "BraveTrackingQueryParametersFilteringEnabled", "type": "bool", "val": "true", "title": "Strip Tracking Query Params", "desc": "Strips fbclid, gclid, and other tracking tags from URLs", "category": "Shields", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "BraveDeAmpEnabled", "type": "bool", "val": "true", "title": "Auto De-AMP Google Pages", "desc": "Automatically redirects Google AMP pages to real URLs", "category": "Shields", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "BraveDebouncingEnabled", "type": "bool", "val": "true", "title": "Skip Bounce Tracking Redirects", "desc": "Skips intermediate bounce-tracking redirect pages", "category": "Shields", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "BraveGlobalPrivacyControlEnabled", "type": "bool", "val": "true", "title": "Send GPC Header", "desc": "Sends Global Privacy Control signal to all sites", "category": "Shields", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": True},
    {"key": "BraveReduceLanguageEnabled", "type": "bool", "val": "true", "title": "Reduce Language Fingerprinting", "desc": "Reduces language header fingerprinting surface", "category": "Shields", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": False},
    {"key": "BackgroundModeEnabled", "type": "bool", "val": "false", "title": "Disable Background Processes", "desc": "Prevents background browser processes when closed", "category": "Shields", "risk": "Safe", "origin": True, "boost": True, "max": True, "quick": False},

    # Credentials & Networking
    {"key": "AutofillAddressEnabled", "type": "bool", "val": "false", "title": "Disable Address Autofill", "desc": "Disables address form saving and autofill", "category": "Credentials", "risk": "Medium", "origin": False, "boost": True, "max": True, "quick": False},
    {"key": "AutofillCreditCardEnabled", "type": "bool", "val": "false", "title": "Disable Card Autofill", "desc": "Disables payment card saving and autofill", "category": "Credentials", "risk": "Medium", "origin": False, "boost": True, "max": True, "quick": False},
    {"key": "PasswordManagerEnabled", "type": "bool", "val": "false", "title": "Disable Password Saving Prompt", "desc": "Disables browser password manager prompts", "category": "Credentials", "risk": "Medium", "origin": False, "boost": False, "max": True, "quick": False},
    {"key": "NetworkPredictionOptions", "type": "integer", "val": "2", "title": "Disable Network Prediction", "desc": "Disables DNS prefetching and speculative link connections", "category": "Networking", "risk": "Low", "origin": False, "boost": True, "max": True, "quick": False}
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Brave Free Origin — macOS GUI</title>
<style>
  :root {
    --bg: #0f1013;
    --card: #18191e;
    --border: #2a2d36;
    --text: #f3f4f6;
    --sub: #9ca3af;
    --accent: #ff5500;
    --accent-hover: #e04b00;
    --green: #10b981;
    --yellow: #f59e0b;
    --red: #ef4444;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    margin: 0;
    padding: 24px;
  }
  .container { max-width: 1040px; margin: 0 auto; }
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding-bottom: 16px;
    margin-bottom: 20px;
  }
  h1 { margin: 0; font-size: 22px; display: flex; align-items: center; gap: 10px; }
  .badge { font-size: 11px; background: var(--accent); color: white; padding: 3px 8px; border-radius: 12px; font-weight: 600; }
  .controls-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }
  .presets { display: flex; gap: 8px; flex-wrap: wrap; }
  button {
    background: var(--card);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 8px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    font-size: 13px;
    transition: all 0.15s;
  }
  button:hover { border-color: var(--accent); color: white; }
  button.active { background: var(--accent); border-color: var(--accent); color: white; }
  .search-input {
    background: var(--card);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 13px;
    width: 220px;
    outline: none;
  }
  .search-input:focus { border-color: var(--accent); }
  .table-box {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    max-height: 580px;
    overflow-y: auto;
  }
  table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }
  th, td { padding: 11px 14px; border-bottom: 1px solid var(--border); }
  th {
    background: rgba(255,255,255,0.03);
    color: var(--sub);
    font-weight: 600;
    position: sticky;
    top: 0;
    backdrop-filter: blur(8px);
    z-index: 10;
  }
  tr:hover { background: rgba(255,255,255,0.02); }
  .tag { padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: bold; }
  .tag-safe { background: rgba(16, 185, 129, 0.15); color: var(--green); }
  .tag-low { background: rgba(245, 158, 11, 0.15); color: var(--yellow); }
  .tag-medium { background: rgba(239, 68, 68, 0.15); color: var(--red); }
  .code { font-family: ui-monospace, Menlo, monospace; font-size: 12px; background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; }
  .footer-actions {
    margin-top: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--card);
    padding: 16px 20px;
    border-radius: 8px;
    border: 1px solid var(--border);
  }
  .btn-primary { background: var(--accent); color: white; border: none; padding: 10px 20px; font-size: 14px; font-weight: 600; }
  .btn-primary:hover { background: var(--accent-hover); }
  .btn-danger { background: rgba(239, 68, 68, 0.15); border: 1px solid var(--red); color: var(--red); }
  .btn-danger:hover { background: var(--red); color: white; }
  #status-msg {
    margin-top: 14px;
    padding: 12px;
    border-radius: 6px;
    display: none;
    font-size: 14px;
    font-weight: 500;
  }
  .status-success { background: rgba(16, 185, 129, 0.15); border: 1px solid var(--green); color: var(--green); }
  .status-error { background: rgba(239, 68, 68, 0.15); border: 1px solid var(--red); color: var(--red); }
</style>
</head>
<body>
<div class="container">
  <header>
    <div>
      <h1>🦁 Brave Free Origin <span class="badge">macOS GUI</span></h1>
      <p style="color:var(--sub);margin:4px 0 0 0;font-size:13px;">Enterprise policy hardening, debloat, and telemetry kill switch.</p>
    </div>
    <div>
      <button class="btn-danger" onclick="restoreStock()">🔄 Restore Stock Brave</button>
    </div>
  </header>

  <div class="controls-bar">
    <div class="presets">
      <button class="active" onclick="setPreset('max')">⚡ Max Privacy (All 30)</button>
      <button onclick="setPreset('boost')">🚀 Privacy + Boost (26)</button>
      <button onclick="setPreset('origin')">🛡️ Origin Mode (16 Core)</button>
      <button onclick="setPreset('quick')">⚡ Quick Debloat (10)</button>
      <button onclick="selectAll(false)">Clear All</button>
    </div>
    <div>
      <input type="text" id="search" class="search-input" placeholder="🔍 Filter policies..." onkeyup="filterRows()">
    </div>
  </div>

  <div class="table-box">
    <table>
      <thead>
        <tr>
          <th style="width: 32px;"><input type="checkbox" id="check-master" checked onchange="toggleMaster(this)"></th>
          <th>Feature</th>
          <th>Category</th>
          <th>Policy Key</th>
          <th>What It Changes</th>
          <th>Risk</th>
        </tr>
      </thead>
      <tbody id="policy-rows"></tbody>
    </table>
  </div>

  <div class="footer-actions">
    <div>
      <span id="selected-count" style="font-weight:bold;color:var(--accent);font-size:16px;">0</span> policies selected.
    </div>
    <div style="display:flex;gap:12px;">
      <button onclick="copyCommand()">📋 Copy Sudo Command</button>
      <button class="btn-primary" onclick="applyPolicies()">🚀 Apply Selected to Brave</button>
    </div>
  </div>

  <div id="status-msg"></div>
</div>

<script>
const POLICIES = __POLICIES_JSON__;

function renderRows() {
  const tbody = document.getElementById("policy-rows");
  tbody.innerHTML = POLICIES.map((p, i) => `
    <tr id="row-${i}">
      <td><input type="checkbox" id="p-${i}" checked onchange="updateCount()"></td>
      <td style="font-weight:600;">${p.title}</td>
      <td style="color:var(--sub);font-size:12px;">${p.category}</td>
      <td><span class="code">${p.key}</span></td>
      <td style="color:var(--sub);">${p.desc}</td>
      <td><span class="tag tag-${p.risk.toLowerCase()}">${p.risk}</span></td>
    </tr>
  `).join("");
  updateCount();
}

function updateCount() {
  const count = POLICIES.filter((_, i) => document.getElementById(`p-${i}`).checked).length;
  document.getElementById("selected-count").innerText = count;
}

function selectAll(val) {
  POLICIES.forEach((_, i) => {
    document.getElementById(`p-${i}`).checked = val;
  });
  updateCount();
}

function toggleMaster(el) {
  selectAll(el.checked);
}

function setPreset(name) {
  document.querySelectorAll(".presets button").forEach(b => b.classList.remove("active"));
  event.target.classList.add("active");
  POLICIES.forEach((p, i) => {
    document.getElementById(`p-${i}`).checked = !!p[name];
  });
  updateCount();
}

function filterRows() {
  const q = document.getElementById("search").value.toLowerCase();
  POLICIES.forEach((p, i) => {
    const row = document.getElementById(`row-${i}`);
    const match = p.title.toLowerCase().includes(q) || p.key.toLowerCase().includes(q) || p.category.toLowerCase().includes(q) || p.desc.toLowerCase().includes(q);
    row.style.display = match ? "" : "none";
  });
}

function getSelectedKeys() {
  return POLICIES.filter((_, i) => document.getElementById(`p-${i}`).checked).map(p => p.key);
}

function showStatus(text, isError) {
  const el = document.getElementById("status-msg");
  el.style.display = "block";
  el.className = isError ? "status-error" : "status-success";
  el.innerText = text;
}

function applyPolicies() {
  const keys = getSelectedKeys();
  if (keys.length === 0) {
    alert("Please select at least one policy.");
    return;
  }
  showStatus("Applying policies... Enter your macOS admin password when prompted.", false);

  fetch("/apply", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ keys: keys })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      showStatus("✔ Success! " + data.applied + " policies written to /Library/Managed Preferences/com.brave.Browser.plist. Please restart Brave and check brave://policy.", false);
    } else {
      showStatus("✘ Error: " + (data.error || "Permission denied or cancelled."), true);
    }
  })
  .catch(err => {
    showStatus("✘ Network error: " + err, true);
  });
}

function restoreStock() {
  if (!confirm("Are you sure you want to restore Brave to factory stock? This removes all debloat policies.")) return;
  showStatus("Restoring stock settings... Enter your macOS password if prompted.", false);

  fetch("/restore", { method: "POST" })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      showStatus("✔ Success! All policies removed. Brave is back to stock factory settings. Please restart Brave.", false);
    } else {
      showStatus("✘ Error: " + data.error, true);
    }
  })
  .catch(err => showStatus("✘ Error: " + err, true));
}

function copyCommand() {
  const keys = getSelectedKeys();
  const selected = POLICIES.filter(p => keys.includes(p.key));
  let cmd = "sudo mkdir -p '/Library/Managed Preferences' && ";
  selected.forEach(p => {
    cmd += `sudo /usr/libexec/PlistBuddy -c 'Delete :${p.key}' '/Library/Managed Preferences/com.brave.Browser.plist' 2>/dev/null || true; `;
    cmd += `sudo /usr/libexec/PlistBuddy -c 'Add :${p.key} ${p.type} ${p.val}' '/Library/Managed Preferences/com.brave.Browser.plist'; `;
  });
  cmd += "sudo killall cfprefsd 2>/dev/null || true; echo 'Done! Restart Brave.'";
  navigator.clipboard.writeText(cmd).then(() => alert("Copied terminal command to clipboard!"));
}

renderRows();
</script>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            rendered = HTML_TEMPLATE.replace("__POLICIES_JSON__", json.dumps(POLICIES))
            self.wfile.write(rendered.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else ""

        if self.path == "/apply":
            data = json.loads(body) if body else {}
            keys = data.get("keys", [])

            plist = "/Library/Managed Preferences/com.brave.Browser.plist"
            cmds = [
                "mkdir -p '/Library/Managed Preferences'",
                f"[ ! -f '{plist}' ] && /usr/libexec/PlistBuddy -c 'Save' '{plist}' 2>/dev/null || true"
            ]
            for p in POLICIES:
                if p["key"] in keys:
                    cmds.append(f"/usr/libexec/PlistBuddy -c 'Delete :{p['key']}' '{plist}' 2>/dev/null || true")
                    cmds.append(f"/usr/libexec/PlistBuddy -c 'Add :{p['key']} {p['type']} {p['val']}' '{plist}'")
            cmds.append(f"chmod 644 '{plist}'")
            cmds.append("killall cfprefsd 2>/dev/null || true")

            full_script = "; ".join(cmds)
            apple_cmd = f'do shell script "{full_script}" with administrator privileges'
            res = subprocess.run(["osascript", "-e", apple_cmd], capture_output=True, text=True)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            if res.returncode == 0:
                self.wfile.write(json.dumps({"success": True, "applied": len(keys)}).encode("utf-8"))
            else:
                self.wfile.write(json.dumps({"success": False, "error": res.stderr.strip()}).encode("utf-8"))

        elif self.path == "/restore":
            plist = "/Library/Managed Preferences/com.brave.Browser.plist"
            cmd = f"rm -f '{plist}'; defaults delete com.brave.Browser 2>/dev/null || true; killall cfprefsd 2>/dev/null || true"
            apple_cmd = f'do shell script "{cmd}" with administrator privileges'
            res = subprocess.run(["osascript", "-e", apple_cmd], capture_output=True, text=True)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            if res.returncode == 0:
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            else:
                self.wfile.write(json.dumps({"success": False, "error": res.stderr.strip()}).encode("utf-8"))

    def log_message(self, format, *args):
        return # suppress console logging

def main():
    server_address = ("127.0.0.1", PORT)
    try:
        httpd = HTTPServer(server_address, RequestHandler)
    except OSError:
        # Port in use, find random port
        httpd = HTTPServer(("127.0.0.1", 0), RequestHandler)
        actual_port = httpd.server_address[1]
    else:
        actual_port = PORT

    url = f"http://127.0.0.1:{actual_port}"
    print(f"\n==============================================")
    print(f"  🦁 Brave Free Origin — macOS GUI Running!  ")
    print(f"  Opening {url} in your browser...          ")
    print(f"  (Press Ctrl+C in Terminal to close GUI)   ")
    print(f"==============================================\n")
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nGUI closed.")

if __name__ == "__main__":
    main()
