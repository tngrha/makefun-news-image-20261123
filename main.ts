// Entry point for news-image-20261123.
// Copies the pre-rendered front page (entry.png, drawn by render.py)
// to the grader's output directory. Deterministic: same input bytes,
// same output bytes. No network, standard library only.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
console.log("wrote", join(outDir, "entry.png"));
