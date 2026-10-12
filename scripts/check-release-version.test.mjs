import assert from "node:assert/strict";
import { test } from "node:test";
import { checkRelease } from "./check-release-version.mjs";

const found = (version) => ({ "package.json": version, "desktop/Cargo.toml": version });

test("a tag matching every version passes, with or without a release candidate suffix", () => {
  assert.equal(checkRelease("v0.1.0", found("0.1.0")), "0.1.0");
  assert.equal(checkRelease("v0.1.0-rc1", found("0.1.0")), "0.1.0");
});

test("a tag that differs from any version fails and names the file", () => {
  assert.throws(() => checkRelease("v0.1.1-rc1", found("0.1.0")), /package\.json is 0\.1\.0/);
  assert.throws(() => checkRelease("v0.1.0", { ...found("0.1.0"), "desktop/Cargo.toml": "0.1.1" }), /Cargo\.toml is 0\.1\.1/);
});

test("a malformed tag fails", () => {
  assert.throws(() => checkRelease("0.1.0", found("0.1.0")), /must look like/);
});
