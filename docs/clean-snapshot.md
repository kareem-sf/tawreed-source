# Private clean candidate — 12 October 2026

Source: remote main 5abb29ce0852d2c450ca475dcad1677ddc7ac40a, tree ef58c0e7331d3c11b5b7880225298822420827de. Exported tracked snapshot only; original workspace and history are untouched.

Quant decision saved on QSM-232 interaction 9ccdb3ad-a9f1-4873-8c57-01aa2d33c56f and task plan revision 0dedcf05-45fa-4260-9bbb-dbe007ffb690 authorises MIT for QS Mind code and neutral alternatives, private preparation only. Both source LICENSE files and first-party metadata use MIT. Third-party licences remain separate.

## Alternatives and rights

- No original sphere artwork, wordmark outlines, desktop icons, favicon or Logo component remains. A neutral slate package diagram was authored as SVG/React for this candidate under MIT; desktop icon files are generated with the locked Tauri CLI (`npm run tauri -- icon desktop/app-icon.svg`). This deliberately changes the visible brand mark; it is not a new brand master.
- No Thmanyah binary or derived outline is present. The loader is removed and Arabic uses the operating system font. English retains the source-head Figtree dependency (SIL OFL); its complete notice is docs/third-party/Figtree-OFL.txt. System fonts are referenced, not redistributed.
- Original Arial PDFs are excluded. Synthetic content remains defined entirely in service/tests/fixtures/make_pdfs.py. The replacement generator embeds the unmodified DejaVu Sans 2.37 font from https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.tar.bz2; full Bitstream/Arev redistribution notices accompany it in fixtures/fonts/DejaVu-LICENSE.txt. Official licence: https://dejavu-fonts.github.io/License.html. Embedded subsets are made by fpdf2; no proprietary font is used.
- Run `service/.venv/bin/python service/tests/fixtures/make_pdfs.py` from the root. Creation time is fixed to 2026-01-01 UTC. All three PDFs, including the deliberately password-protected fixture, reproduce byte for byte with the recorded installed fpdf2/fonttools/uharfbuzz versions. Passwords in this generator are synthetic test values. Existing English, Arabic, RTL/ligature and locked-PDF tests retain their assertions.
- No customer BOQs, local databases, keys, extracted customer content or font files from the shared workspace were imported. No dependency source or built third-party runtime is vendored except the licensed fixture font. Dependency manifests resolve external libraries under their own licences; a future distributed installer still needs its resolved-runtime notices, especially PDFium. This source-only preparation is not clearance for a compiled release.

## Immutable release contracts and review

App ID com.qsmind.tawreed, version 0.1.0, updater configuration/keys and CI destinations stay byte-identical to the source snapshot. No remote is configured and no push, tag, release or Public change is permitted. Public remains gated on MiniMax revocation evidence through Quant and Engineering review of the exact final head on QSM-232. Proposed private source destination remains kareem-sf/tawreed-source; existing tawreed-releases is not duplicated.

Rollback: delete this isolated candidate and recreate from the preserved immutable snapshot; the source repository needs no rollback.

Windows QA after Engineering acceptance: on a clean Windows machine use Python 3.12/Node 24/Rust prerequisites, create service/.venv, install service[dev], run npm ci and npm run verify/build, then npm run package locally without publication. Check app ID/version, neutral icon, English and Arabic About/RTL, synthetic PDF import and provenance, service stop on exit. Do not inject Thmanyah, make a release/tag, or alter updater/signing settings. Linux checks cannot prove clean Windows installation.
