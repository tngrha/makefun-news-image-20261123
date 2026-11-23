# Monday 23 November 2026 — the world on one page

[![make.fun bounty](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/tngrha/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/tngrha/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

A serif broadsheet front page summing up Monday 23 November 2026 in one
image: 52 verified stories across 7 regions — four hero panels, twelve
illustrated panels with verification tags and named sources, a UTC
timeline, a world map with numbered pins, 36 one-line briefs, and a
date-check box listing stories deliberately left out as not 23 November
news. Every story happened, or was first reported, on 23 November 2026.

Built for the [make.fun](https://make.fun/bounty/news-image-20261123)
news-image-20261123 bounty. New to make.fun? Join with referral code
[px8mhdxd](https://make.fun/r/px8mhdxd).

## Run

The grader runs `main.ts`, which copies `entry.png` to `/output/entry.png`:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To redraw the page from scratch (needs Pillow and the DejaVu/Noto serif
fonts):

```sh
python3 render.py   # writes entry.png (1024×1024)
```

`stories.md` documents every story, its source, and the date-check
exclusions. All illustrations are original flat drawings in code.

## License

MIT — see `LICENSE`.
