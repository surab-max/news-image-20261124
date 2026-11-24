# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/surab-max/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/surab-max/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

**Tuesday 24 November 2026 — the world in one day, in one image.** A newspaper front page drawn entirely in code: three oil tankers ablaze in the Strait of Hormuz after hitting naval mines as the lead, UN talks on lethal autonomous weapons ending with no deal, Trump halting the Army's planned detonation of bomb-making chemicals in Iowa, the US sanctioning two dozen-plus Iranian exchange houses, and Russia telling the UN Security Council there will be no new grain deal — plus a briefs strip with the school bomb threats in Germany and Denmark, India's €1.4bn pledge to Nepal, China's 2030 care targets, Colombia's post-peace-deal violence, and Erdoğan's Libya visit. Every story is a verified event of 24 November 2026; `SOURCES.md` lists each one with the outlets that reported it. The image is a 1024×1024 PNG inside the competition's 1 MiB / 1024 px caps, and its masthead names the day it sums up.

The front page is built for the judge's ~300 px view: few stories, huge headlines, one dominant lead, no small print.

**How it is built.** `tools/generate.py` renders the front page with Pillow (dated masthead, a drawn dusk scene of the burning tankers, lead headline, four story panels, briefs strip) and writes `entry.png`. The graded program, `main.ts` (Node 22, standard library only), copies `entry.png` to `/output/entry.png`, verifying the PNG's dimensions against the competition caps and the copy's SHA-256 against the source, so both grader runs produce byte-identical output with no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# then view out/entry.png — the front page of 24 November 2026
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ys1ka8r4&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
