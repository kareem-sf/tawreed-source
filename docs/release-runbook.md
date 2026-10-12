# Release runbook (public source `kareem-sf/tawreed-source`)

Owner: release engineer. Applies to the clean public source only. The old private `kareem-sf/tawreed` history is never pushed here and its visibility is never changed automatically.

## What runs and when

| Workflow | Trigger | What it proves | Output |
|---|---|---|---|
| CI `Verify` | pull request, push to `main`, manual | bindings are current, `npm run verify` (service tests, UI tests, typecheck, lint, Clippy, release script tests), UI build, Linux deb compiles | none |
| CI `Linux clean-install smoke test` | after `Verify` | on a fresh Ubuntu 24.04 x86_64 runner: the deb installs with `apt`, the installed service starts with an empty environment and isolated `TAWREED_HOME`, `/health` is ok, a request without the token gets 401, `/about` reports the deb version, a synthetic BOQ (`service/tests/fixtures/boq-english.pdf`) starts a project, state stays in the isolated folder, the service exits when stdin closes, the package removes cleanly | artifact `linux-smoke-evidence` (`evidence.json`, `service.log`, `package-files.txt`), 3 days |
| CI `Windows Clippy`, `Release gate` | same | Windows Rust lint; gate fails unless all of the above pass | none |
| Release | tag push `v*` or manual dispatch with `tag` | tag and every source version agree; Linux deb; same smoke test on the built deb; Windows installer with silent install, `/health`, uninstall; `SHA256SUMS`; **draft** release | draft release with deb, exe, `SHA256SUMS`; smoke evidence artifact 7 days |

All jobs use GitHub-hosted standard runners on a public repository: no paid runners, no paid storage, no self-hosted machines. Artifacts are short-lived and hold no fonts, keys or customer data.

## Version and tag rule

The tag must be `v<version>` or `v<version>-rcN`, where `<version>` equals `package.json`, `desktop/tauri.conf.json`, `desktop/Cargo.toml`, `service/pyproject.toml` and `service/tawreed/__init__.py`. `scripts/check-release-version.mjs` enforces it as the first Release job; a mismatch stops the run before anything is built. Check locally: `node scripts/check-release-version.mjs v0.1.0-rc1`.

History: draft `v0.1.1-rc1` held `Tawreed_0.1.0_*` files. It is invalid under this rule and must not be published.

## Steps to release

1. Change the version in the five files above in one reviewed pull request (the UI test fixtures and `ui/src/api/openapi.json` carry it too; run `npm run bindings`).
2. The pull request needs a green CI run on its head, including the smoke test, and one Engineering Lead review.
3. Merge to `main`. Wait for the `main` push CI run to pass.
4. Run Release: `gh workflow run Release -R kareem-sf/tawreed-source -f tag=v<version>-rc1`.
5. Download the draft's files and `SHA256SUMS`; run `sha256sum -c SHA256SUMS`.
6. QA does native Desktop acceptance on a clean Ubuntu Desktop and Windows machine using `docs/2026-10-12-clean-install-and-signing.md`. The headless smoke test does not replace this: it never opens the window and does not check Arabic rendering, the launcher or the Settings screens.
7. Publish the draft only after QA records pass and the release owner approves. Publishing is a manual action on GitHub. For a non-candidate release, run Release again with `tag=v<version>`.

## Gates that stay closed

- Unsigned installers: no signing certificate exists. SmartScreen warns on Windows. Buying a certificate needs Kareem's approval.
- Updater: `desktop/tauri.release.conf.json` has an empty `pubkey` and `createUpdaterArtifacts: false`. No `latest.json` is produced, so no installed copy can update. Enable only with a signing key held in Actions secrets (needs Kareem to add it).
- Thmanyah Sans licence forbids uploading it, so hosted builds use the system Arabic font. A build that embeds the font must be made on a licensed machine and is not produced by CI.
- Branch protection on `main` is not claimed active until verified through the API.
- The Release workflow only creates drafts. It never publishes.

## Rollback

- A bad workflow change: revert the commit on `main`. Do not rewrite history.
- A bad draft: delete the draft release and its tag in GitHub. Nothing was published.
- A bad published release: mark it pre-release or delete it, and publish a fixed version. Never replace assets of a published tag in place.
- Nothing in this pipeline touches Production or the old private repository.

## Remaining managed-access needs

- Native Desktop acceptance: QA needs an Ubuntu Desktop and a Windows machine (not available to this pipeline).
- Signing certificate and updater private key: need Kareem.
- Publishing a release: needs the release owner's manual action and Kareem's decision if it becomes the public download page.
