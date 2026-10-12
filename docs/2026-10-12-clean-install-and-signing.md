# Tawreed: clean install steps and signing recommendation

Date: 2026-10-12. Task QSM-267 (under QSM-249). Nothing here was run: no workflow is triggered until the repository is public (QSM-232).

## 1. Unsigned first release: acceptable?

Yes, for a first release to named customers, if the download page says what to expect.
- Windows SmartScreen shows "Windows protected your PC" for an unsigned installer. The user clicks "More info", then "Run anyway". A new, unsigned, low-download file is also more likely to be flagged by Defender (PyInstaller folders often are). Extended Validation certificates no longer give instant reputation, so paying more does not remove the warning on day one.
- The Tauri updater signature (minisign key, QSM-3) is separate and still mandatory. It protects updates, not the first install.
- Mitigation for the first release: publish SHA256SUMS next to the file, give a 3-line "how to open" note, and submit the installer to Microsoft Defender for false-positive review.

## 2. Cheapest signing option (no purchase made)

Prices are from memory of public price lists, not quoted; verify before buying.
| Option | Cost | Note |
|---|---|---|
| No signing | 0 | SmartScreen warning; fine for first release |
| Azure Trusted Signing (Artifact Signing) | about USD 10 per month | Cheapest; needs identity validation of an organisation with 3+ years history, or an individual in supported regions. Egypt/Gulf eligibility must be checked |
| OV code-signing certificate (cloud HSM/token) | about USD 200-400 per year | Works anywhere; reputation builds slowly |
| EV certificate | about USD 300-600 per year | Same SmartScreen reputation path as OV now |

Recommendation: ship v0.1 unsigned. In parallel, check Azure Trusted Signing eligibility for QS Mind (zero cost to check). If not eligible, buy one OV certificate only when customers report the warning blocks them. The decision to spend is the founder's.

## 3. Clean install steps for the tester

Use a machine or VM that never had Tawreed or the build tools. Do not use the development machine.

### Windows 10/11 (64-bit)
1. Download `Tawreed_<version>_x64-setup.exe` and `SHA256SUMS` from the release.
2. `Get-FileHash .\Tawreed_*-setup.exe -Algorithm SHA256` and compare with SHA256SUMS. Stop if different.
3. Double-click the installer. Expect SmartScreen: More info, then Run anyway. Record whether Defender removed the file.
4. Expect no administrator (UAC) prompt: install is per user, in `%LOCALAPPDATA%\Tawreed`.
5. Start Tawreed from the Start menu. Expect the Arabic window; text must render (system font, no Thmanyah in hosted builds). Open About: the version matches.
6. Create a project and import one sample BOQ. Expect no "service" error. Check `%APPDATA%\com.qsmind.tawreed\logs\service.log` (or the app log dir) is empty of tracebacks.
7. Close the window. In Task Manager, `tawreed-service.exe` must disappear within 5 seconds.
8. Uninstall from Settings > Apps. Expect the folder removed; `~\.tawreed` data stays by design.
9. Repeat steps 1-8 a second time on a second clean machine (target: 2 of 2).
Record: Windows build number, whether WebView2 was already present, SmartScreen/Defender result.

### Linux (Ubuntu 24.04)
1. Download the `.deb` and `SHA256SUMS`; `sha256sum -c SHA256SUMS --ignore-missing`.
2. `sudo apt install ./Tawreed_<version>_amd64.deb` (pulls the WebKitGTK dependency).
3. Start Tawreed from the app menu. Expect the window; steps 5-7 from Windows apply (service log under `~/.local/share/com.qsmind.tawreed/logs/`).
4. `sudo apt remove tawreed`.
