# ⚽ Cristiano Ronaldo Club Career Analysis

### 🔗 Live dashboard: https://nitish1107.github.io/CRISTIANO-RONALDO-GOALS-ANALYSIS/

An interactive dashboard of Cristiano Ronaldo's career goals: **985 goals** (839 for clubs, 146 for Portugal) and 291 assists, as of 30 Oct 2026. Built with HTML, CSS and JavaScript, with Power BI-ready data files for a matching Power BI report.

## ✨ Features
- **Totals:** career goals, club goals, Portugal goals and assists in one strip
- **Goals for each club separately**, with a crest slot for each: Sporting CP 5, Manchester United 145, Real Madrid 450, Juventus 101, Al Nassr 138
- **Goals for Portugal:** 146, broken down by competition
- **Goal features:** by body part (right foot 635, left foot 187, header 160, other 3) and by finish (open play 735, penalties 184, direct free kicks 66), plus free kicks per team
- **Goals by competition,** with a Club / Country switch
- Dark and light themes, hover tooltips, a data-table view, and a layout that works on phones

## 🛠️ Tech stack
HTML · CSS · JavaScript · Python · Power BI (DAX) · GitHub Pages · GitHub Actions

## 📁 Project structure
| Path | What it is |
|---|---|
| `index.html` | The dashboard page |
| `data/stats.json` | The numbers the page shows |
| `data/*.csv` | Six tables ready to import into Power BI or Excel |
| `powerbi/POWERBI_GUIDE.md` | DAX measures and visual-by-visual steps for Power BI Desktop |
| `logos/` | Club crests, named `sporting-cp`, `manchester-united`, `real-madrid`, `juventus`, `al-nassr`, `portugal` (png, svg, jpg or webp) |
| `images/` | Background photo, saved as `ronaldo-bg.jpeg` |
| `scripts/update_stats.py` | Optional auto-update script using API-Football |
| `.github/workflows/update-goals.yml` | Hourly GitHub Actions job that runs the script |

## 🚀 Run it on your computer
1. Open the folder in VS Code.
2. Install the **Live Server** extension.
3. Right-click `index.html` and choose **Open with Live Server**.

Opening `index.html` by double-click also works, but then it shows the numbers saved inside the file, not `data/stats.json`.

## 🌐 Publish with GitHub Pages
1. Push the project to a GitHub repository.
2. In **Settings > Pages**, set the source to **Deploy from a branch**, branch `main`, folder `/ (root)`.
3. The site goes live at the link at the top of this file.

## 📊 Power BI version
Import the six CSV files from `data/` and follow `powerbi/POWERBI_GUIDE.md` for the measures and visuals.

## 🔄 Updating the numbers
- **By hand:** edit `data/stats.json` (the team and competition goals, `total`, and `asof`), keeping the competition goals adding up to the total. Commit and push, and the site updates within a couple of minutes.
- **Automatically (optional):** the workflow in `.github/workflows` calls API-Football every hour. It needs the repository secrets `API_FOOTBALL_KEY` and `PLAYER_ID` (Ronaldo's ID is `874`), and a plan that covers the current season. **API-Football's free plan only covers 2022 to 2024, so this does not work on the free plan.** Disable the workflow in the Actions tab unless you have a paid plan.

Body part, finish and free-kick figures are career snapshots and are not updated automatically.

## 📌 Data sources and limits
Figures are compiled from public goal trackers (ronaldostats.app, theroadto1000goals.com, messixronaldo.com, World Soccer Talk) as of 30 Oct 2026. Trackers differ by a goal or two on body part, and no source splits body part or finish by club. Counts may have changed since this date.

## 🖼️ Credits
Club crests and the background photo belong to their owners. They are used for a portfolio project, not for commercial use. Check each owner's terms before using them publicly.

## 👤 Author
**Nitish Kumar** · [LinkedIn](https://www.linkedin.com/in/nitish-kumar-77575624b) · [GitHub](https://github.com/nitish1107)
