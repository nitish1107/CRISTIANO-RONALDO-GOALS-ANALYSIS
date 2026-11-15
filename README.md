# Cristiano Ronaldo Club Career Analysis

A career-goals dashboard for Cristiano Ronaldo: 985 goals (839 for clubs, 146 for Portugal), as of 30 Oct 2026.

## What's inside
| Path | What it is |
|---|---|
| `index.html` | The interactive dashboard. Open it in any browser, no install needed. |
| `data/` | Six CSV tables, ready to import into Power BI or Excel. |
| `powerbi/POWERBI_GUIDE.md` | DAX measures and visual-by-visual steps to rebuild it in Power BI Desktop. |
| `logos/` | Put club crests here (see `logos/README.txt`). |
| `images/` | Put your background photo here (see `images/README.txt`). |
| `data/stats.json` | The numbers the page shows. The auto-update job changes this file. |
| `scripts/update_stats.py`, `.github/workflows/update-goals.yml` | Hourly auto-update from API-Football (needs the secrets `API_FOOTBALL_KEY` and `PLAYER_ID` in your GitHub repository). |

## Features
- Total goals so far, split into club goals and Portugal goals
- Goals for each club separately: Sporting CP 5, Manchester United 145, Real Madrid 450, Juventus 101, Al Nassr 138
- Goals for Portugal (146), broken down by competition
- Goals by body part: right foot 635, left foot 187, header 160, other 3
- Goals by finish: open play 735, penalties 184, direct free kicks 66
- Goals by competition, with a Club / Country switch

## Sources and limits
Compiled from public goal trackers (ronaldostats.app, cross-checked with theroadto1000goals.com and World Soccer Talk). Trackers differ by a goal or two on body part. Body part and finish are career totals; per-club splits are not published.
