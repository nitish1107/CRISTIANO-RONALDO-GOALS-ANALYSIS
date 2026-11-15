# Build the dashboard in Power BI Desktop

The CSV files in `../data` are ready to import. The numbers match the web dashboard (`../index.html`) exactly.

## 1. Import the data
Home > Get data > Text/CSV, then load all six files from the `data` folder:
`goals_by_team`, `goals_by_competition`, `goals_by_body_part`, `goals_by_finish_type`, `free_kicks_by_team`, `career_summary`.
There is nothing to join: each table answers one question, so each visual uses one table.

## 2. Measures (Modeling > New measure)
```DAX
Total Goals    = SUM ( goals_by_team[Goals] )
Club Goals     = CALCULATE ( [Total Goals], goals_by_team[Type] = "Club" )
Portugal Goals = CALCULATE ( [Total Goals], goals_by_team[Type] = "Country" )
Share of Career % = DIVIDE ( [Total Goals], CALCULATE ( [Total Goals], ALL ( goals_by_team ) ) )
Assists        = CALCULATE ( MAX ( career_summary[Value] ), career_summary[Metric] = "Career assists" )
Right Foot %   = DIVIDE ( CALCULATE ( SUM ( goals_by_body_part[Goals] ), goals_by_body_part[BodyPart] = "Right foot" ), SUM ( goals_by_body_part[Goals] ) )
```

## 3. Visuals (same layout as the web version)
| Area | Visual | Fields |
|---|---|---|
| Top strip | 4 Card visuals | Total Goals, Club Goals, Portugal Goals, Assists (985 / 839 / 146 / 291) |
| Goals by club | Table or Multi-row card | Team, Goals, Share of Career %, LogoURL (see step 4) |
| Goals by body part | Donut | Legend = BodyPart, Values = Goals |
| Goals by finish | Clustered bar | Axis = FinishType, Values = Goals |
| Free kicks | Clustered bar | Axis = Team, Values = FreeKicks |
| Competitions | Clustered bar + Slicer | Axis = Competition, Values = Goals, Slicer = Scope (Club / Country) |
| Portugal | Clustered bar | Filter Scope = Country |

Sort every bar chart by Goals, descending. Add a Slicer on `Scope` to switch between club and country competitions.

## 4. Club logos
`goals_by_team.csv` has an empty `LogoURL` column. Paste a link to each club's official crest image (for example one you host yourself), then select the column and set Column tools > Data category > **Image URL**. Table and Multi-row card visuals then show the crest next to each team.

## 5. Look
Use View > Themes, a dark background (`#0d1210`), and these colors for the series: Sporting `#3987e5`, Manchester United `#d95926`, Real Madrid `#199e70`, Juventus `#c98500`, Al Nassr `#d55181`, Portugal `#0ca30c`.

## Data notes
Figures are compiled from public goal trackers and are as of 30 Oct 2026. Body part and finish splits are career totals; no per-club split is published. Refresh the CSVs when his count changes.
