// make.fun entry: "Sum up 24 November's world news in one image".
//
// The repository holds the finished front page in entry.png (drawn by
// tools/generate.py from the verified news of Tuesday 24 November 2026;
// see SOURCES.md). The grader runs this program twice with no network
// and both runs must write identical bytes, so the program does exactly
// one deterministic thing: copy entry.png to the output directory.
//
// Output directory: $MAKEFUN_OUTPUT_DIR when set (local runs), else
// /output (the grader's writable mount).

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const MAX_BYTES = 1048576; // the competition's 1 MiB image cap
const MAX_SIDE = 1024; // the competition's 1024 px side cap

const here = new URL('.', import.meta.url);
const source = new URL('./entry.png', here);
const bytes = readFileSync(source);
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}
if (bytes.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') {
  throw new Error('entry.png is not a PNG file');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (Math.max(width, height) > MAX_SIDE) {
  throw new Error(`image is ${width}x${height}, over the 1024 px cap`);
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'entry.png');
copyFileSync(source, target);
const copied = readFileSync(target);
const digest = createHash('sha256').update(bytes).digest('hex');
if (createHash('sha256').update(copied).digest('hex') !== digest) {
  throw new Error('copied image differs from the source');
}
console.log(`entry.png: ${width}x${height}, ${bytes.length} bytes, sha256 ${digest.slice(0, 16)}... -> ${target}`);
