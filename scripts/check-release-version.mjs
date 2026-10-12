// Fail unless the release tag and every version in the source agree: v<version> or v<version>-rcN.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = (file) => readFileSync(path.join(root, file), "utf8");

export function versions(read) {
  return {
    "package.json": JSON.parse(read("package.json")).version,
    "desktop/tauri.conf.json": JSON.parse(read("desktop/tauri.conf.json")).version,
    "desktop/Cargo.toml": /^version = "([^"]+)"/m.exec(read("desktop/Cargo.toml"))?.[1],
    "service/pyproject.toml": /^version = "([^"]+)"/m.exec(read("service/pyproject.toml"))?.[1],
    "service/tawreed/__init__.py": /__version__ = "([^"]+)"/.exec(read("service/tawreed/__init__.py"))?.[1],
  };
}

export function checkRelease(tag, found) {
  const match = /^v(\d+\.\d+\.\d+)(-rc\d+)?$/.exec(tag);
  if (!match) throw new Error(`Tag ${tag} must look like v0.1.0 or v0.1.0-rc1.`);
  const wrong = Object.entries(found).filter(([, version]) => version !== match[1]);
  if (wrong.length) throw new Error(`Tag ${tag} needs version ${match[1]}, but ${wrong.map(([file, version]) => `${file} is ${version}`).join(", ")}.`);
  return match[1];
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  try {
    const tag = process.argv[2];
    console.log(`${tag}: all versions are ${checkRelease(tag, versions(read))}`);
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
