# GitHub CI

The public source is `kareem-sf/tawreed-source`. Only reviewed files from the clean snapshot are used; the old private repository history must not be pushed here.

CI runs on pull requests, main pushes and manual dispatch. Its read-only Ubuntu 24.04 job checks generated bindings, runs the full local verification, builds the UI and compiles a Linux deb for verification. Actions are pinned to commit SHAs. npm, pip and Cargo caches contain public dependencies and build output only. No fonts, credentials or customer data are supplied. No package artifact is uploaded by CI, so artifact retention is not applicable. The deb is not a user-accepted installer. The existing Windows Clippy check is preserved in a separate hosted job.

Concurrent runs on the same ref cancel older runs. Verification has a 30-minute limit; the two-minute Release gate fails unless Linux verification and Windows Clippy succeed. No self-hosted runners or paid runner types are used.

Release automation is owned separately by the release engineer. This change does not alter the release workflow, app ID, updater keys, signing configuration or existing v0.1.0 release. It does not prove installation on Windows or macOS.

Before merging, require a successful CI run for the PR head and Engineering Lead review. Rollback is a revert of this CI-only commit; do not import old history or replace published release assets. Branch protection and other repository settings must be verified through the API before claiming they are active.

References: [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [billing and usage](https://docs.github.com/en/actions/concepts/billing-and-usage).
