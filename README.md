# 🦁 Brave Free Origin for macOS

A native, zero-dependency debloater and privacy hardening tool for Brave Browser on macOS[span_0](start_span)[span_0](end_span). Ported from [TahaHydra/Brave-Free-Origin](https://github.com/TahaHydra/Brave-Free-Origin)[span_1](start_span)[span_1](end_span).

Removes Leo AI, crypto wallets, rewards popups, background bloat, and telemetry while locking Brave Shields to maximum protection[span_2](start_span)[span_2](end_span).

---

## ✨ Features

* **Native System Enforcement**: Configures policies at `/Library/Managed Preferences/com.brave.Browser.plist` as machine-level rules that cannot be silently overridden by site scripts or default updates[span_3](start_span)[span_3](end_span).
* **Preserves Code Integrity**: Does not patch or modify `/Applications/Brave Browser.app`, ensuring Apple Gatekeeper, AMFI, and automatic updates remain intact[span_4](start_span)[span_4](end_span).
* **Zero External Dependencies**: Operates entirely with the default Python 3 standard library (`http.server` & standard APIs)—no `pip install` or third-party packages required[span_5](start_span)[span_5](end_span).
* **Visual Dashboard**: Live filterable checklist with presets and a one-click apply button.
* **Instant Rollback**: Completely reversible to out-of-the-box factory defaults at any time[span_6](start_span)[span_6](end_span).

---

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Brave-Free-Origin-macOS.git](https://github.com/YOUR_USERNAME/Brave-Free-Origin-macOS.git)
   cd Brave-Free-Origin-macOS
Launch the GUI:
python3 brave-gui.py

(A local dashboard opens automatically in your browser).
Select your preset or toggle custom items:
⚡ Max Privacy: Applies all debloat, telemetry kill-switches, and maximum shields.
🚀 Privacy + Boost: Shields and debloat while preserving autofill.
🛡️ Origin Mode: The core 16 baseline switches matching the original project.
⚡ Quick Debloat: Basic removal of AI, Wallet, Rewards, and VPN.
Apply and Restart:
Click 🚀 Apply Selected to Brave and approve the macOS authorization prompt.
Completely quit Brave (Cmd + Q) and relaunch it.
🔍 Verification
Navigate to brave://policy in Brave. Every configured item will display with Level: Mandatory and Status: OK.
Note: A badge reading "Managed by your organization" will appear inside Brave's Settings. This is standard Chromium behavior whenever system-level policies are active.


🔄 Restoring Stock Defaults
To remove all policies and return Brave to default settings:
Run python3 brave-gui.py and click 🔄 Restore Stock Brave in the top-right corner.

Alternatively, run the following in Terminal:
sudo rm -f "/Library/Managed Preferences/com.brave.Browser.plist"
defaults delete com.brave.Browser 2>/dev/null || true
sudo killall cfprefsd
