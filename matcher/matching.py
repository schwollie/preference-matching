# matching.py
from typing import Dict, List
import random

def stable_marriage(team_prefs: Dict[str, List[str]], options: List[str]) -> Dict[str, str]:
    free_teams = list(team_prefs.keys())
    proposals = {team: [] for team in team_prefs}
    option_matches = {}

    
    # Generate inverse preferences for options (random order to be indepent from input)
    keys_random = list(team_prefs.keys())
    random.seed(42)  # Use a fixed seed for reproducible results
    random.shuffle(keys_random)
    option_prefs = {option: keys_random for option in options}

    while free_teams:
        team = free_teams.pop(0)
        team_pref_list = team_prefs[team]

        for option in team_pref_list:
            if option not in proposals[team]:
                proposals[team].append(option)

                if option not in option_matches:
                    option_matches[option] = team
                    break
                else:
                    current_team = option_matches[option]
                    # Check if option prefers new team over current
                    if option_prefs[option].index(team) < option_prefs[option].index(current_team):
                        option_matches[option] = team
                        free_teams.append(current_team)
                        break
        else:
            # If team has proposed to all options, no match possible
            pass

    # Reverse mapping to team: option
    final_matches = {team: option for option, team in option_matches.items()}
    return final_matches