import typer
from typing import List, Dict
from matcher.matching import stable_marriage

app = typer.Typer()

@app.command()
def match(
    teams: List[str] = typer.Option(..., "--team", "-t", help="List of team names"),
    options: List[str] = typer.Option(..., "--option", "-o", help="List of available options"),
):
    typer.echo("Teams: " + ", ".join(teams))
    typer.echo("Options: " + ", ".join(options))

    preferences: Dict[str, List[str]] = {}

    for team in teams:
        typer.echo(f"\nEnter preferences for team '{team}' (1=best, 99=worst):")
        team_prefs = {}
        for option in options:
            pref = typer.prompt(f"Preference for '{option}'", type=int)
            team_prefs[option] = pref
        # Sort options by preference (lowest number first)
        sorted_prefs = sorted(team_prefs, key=lambda x: team_prefs[x])
        preferences[team] = sorted_prefs

    matches = stable_marriage(preferences, options)
    typer.echo("\nFinal Matches:")
    for team, option in matches.items():
        typer.echo(f"{team} matched with {option}")

if __name__ == "__main__":
    app()