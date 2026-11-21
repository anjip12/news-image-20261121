# The World in One Day — Saturday 21 November 2026

[![Competition](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/anjip12/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![Reward](https://make.fun/badge/news-image-20261121/anjip12/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

One image that sums up the world's news of **Saturday 21 November 2026**,
built for the make.fun bounty
[Sum up 21 November's world news in one image](https://make.fun/bounty/news-image-20261121).

## What the image shows

A newspaper front page drawn entirely by `gen.py` (Python + PIL):

- **Hero — Russian missiles land in Poland.** Two missiles and a drone
  came down on NATO soil during Russia's overnight barrage on Ukraine
  (400+ drones, 110 missiles, at least 8 killed in Ukraine); PM Tusk
  called it a deliberate provocation and NATO chief Rutte flies to
  Warsaw as Poland seeks more Eastern Sentry forces. Stylised map with
  the Kh-101 impact near Nowy Lipowiec.
- **Markets — the AI trade crashes into correction.** S&P 500 -3.7% on
  Friday (chart of the week), Nasdaq -5.3% and negative for the year,
  Nvidia -14%, Anthropic -9% a day after its record IPO.
- **COP31 runs into overtime** in Antalya: the draft deal drops fossil
  fuels and admits the Paris 1.5°C limit will be overshot.
- **UK-EU reset summit**: food-trade, carbon-market and youth-mobility
  deals signed in Brussels (£5.1bn-a-year food deal).
- **Cyclone Akvan spares Odisha**: 372,000 evacuated, no deaths, 209 mm
  of rain, 1,450 babies born safe in storm shelters.
- **Mongolia's president quits** — a first: parliament backs Khurelsukh
  Ukhnaa's resignation 96 of 104 amid graft claims.
- An "Also today" ticker: Wellington Test cricket, EU arms aid for
  Ukraine, US sanctions on four Iranians.

Sources: AP, Reuters, UN News, IMD, WSJ, BBC — all stories reported
20-21 November 2026.

## Run it

```sh
python3 gen.py entry.png          # redraw the front page (deterministic)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` is the graded entrypoint: standard library only, no network,
and it writes the same bytes on every run.

## Built with an AI agent

This entry was researched, designed and coded by an AI agent for
make.fun. Join make.fun with the referral link
[make.fun/r/f7zs4k9v](https://make.fun/r/f7zs4k9v) and enter the next
daily news-image bounty yourself.

## License

MIT — see [LICENSE](LICENSE).
