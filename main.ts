// THE WORLD TODAY - Wednesday 25 November 2026.
// Entrypoint: validates the pre-built entry.png and copies it to the output
// directory. No network, no drawing at runtime, no environment reads.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const out = join(outDir, "entry.png");

const buf = readFileSync(src);

// PNG magic: 89 50 4E 47 0D 0A 1A 0A
const magic = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
for (let i = 0; i < magic.length; i++) {
  if (buf[i] !== magic[i]) {
    throw new Error("entry.png is not a PNG file");
  }
}
if (buf.length > 1048576) {
  throw new Error("entry.png is over the 1 MiB limit: " + buf.length);
}
// IHDR width/height are big-endian uint32 at offsets 16 and 20.
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error("entry.png is over 1024x1024: " + width + "x" + height);
}
// A whole PNG ends with the 12-byte IEND chunk.
const tail = buf.subarray(buf.length - 12);
const iend = [0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82];
for (let i = 0; i < iend.length; i++) {
  if (tail[i] !== iend[i]) {
    throw new Error("entry.png is truncated: no IEND chunk");
  }
}
if (!existsSync(outDir)) {
  mkdirSync(outDir, { recursive: true });
}
writeFileSync(out, buf);
console.log("wrote " + out + " (" + buf.length + " bytes, " + width + "x" + height + ")");
