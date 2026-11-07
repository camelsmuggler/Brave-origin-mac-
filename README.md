




Select a Preset:
⚡ Max Privacy (Applies all 30 debloat & privacy policies)
🚀 Privacy + Boost (Maximum shields, keeps autofill)
🛡️ Origin Mode (The 16 core debloat toggles)
Deploy:
Click Apply Selected to Brave, enter your macOS password once, and restart your browser.
Verify:
Navigate to brave://policy in your URL bar. Your policies should read Status: OK.
🛡️ What It Does
Brave Free Origin works by writing to /Library/Managed Preferences/com.brave.Browser.plist. Because it uses native Apple administration paths, these settings become Mandatory Machine Policies. They cannot be bypassed by standard user preferences or extensions.
Core Terminations
Leo AI – Removed from URL bar, sidebar, and context menus.
Web3 & Crypto – Disables Brave Wallet and Web3 prompts.
BAT Rewards – Turns off the Brave Rewards advertising engine.
Telemetry – Kills P3A analytics, usage pings, crash reporting, and the Web Discovery Project.
Bloatware – Disables Brave News, VPN, Brave Talk, Speedreader, and Wayback Machine popups.
Hardened Privacy Shields
Enforces Aggressive Ad & Tracker Blocking.
Enforces Strict Fingerprinting Protection.
Strips tracking URL parameters (fbclid, gclid).
Automatically redirects Google AMP pages.
Skips bounce-tracking redirects.
🔄 Reverting to Stock
You can undo everything at any time:
Run python3 brave-gui.py
Click Restore Stock Brave in the top right corner.
Restart Brave.
This deletes the plist file and resets the browser back to factory defaults.
🛠️ Requirements & Compatibility
macOS 11+ (Tested on macOS Monterey through Sequoia)
Python 3 (Pre-installed on macOS or easily accessible via Xcode Command Line Tools)
No third-party Python modules required (uses standard library http.server and tkinter).
Does not break Brave updates or trigger AMFI/Gatekeeper crashes, because it does not modify the signed .app bundle.
