# world-today-25-nov-2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/sadiomonro-boop/world-today-25-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/sadiomonro-boop/world-today-25-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

THE WORLD TODAY — Wednesday 25 November 2026: 38 stories from six continents, one front page. A new strike on a Russian warship in the Gulf of Finland leads; Shenzhou-24 lifts off with the first Pakistani in orbit; Asian markets plunge on tariff fears. A dot-matrix world map pins the 12 biggest stories, a KPI strip carries the day's figures, and a red DATE CHECK bar names the 24 November stories left out on purpose. Every story happened, or was first reported, on Wednesday 25 November 2026.

## Run it

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`render.py` draws `entry.png` (1024x1024) from the story list with Pillow — no network, fixed seed, byte-identical on every run. `main.ts` only validates the PNG (magic bytes, at most 1024x1024, at most 1 MiB, IEND chunk present) and copies it to the output directory.

Stories were verified against wire reports dated Wednesday 25 November 2026; the red DATE CHECK bar names four 24 November stories deliberately left out (Huawei verdict, Riyadh tower strike, Abu Dhabi talks, Real Madrid 5-1 PSV).

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
