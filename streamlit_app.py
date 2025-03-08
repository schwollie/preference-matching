import streamlit as st
import pandas as pd
from matcher.matching import stable_marriage

st.title("Preference Matching App")

# Sidebar for input
st.sidebar.header("Setup Teams and Options")

# Input teams
teams_input = st.sidebar.text_area("Enter Teams (one per line)", "Team A\nTeam B\nTeam C")
teams = [team.strip() for team in teams_input.strip().split("\n") if team.strip()]

# Input options
options_input = st.sidebar.text_area("Enter Options (one per line)", "Option 1\nOption 2\nOption 3")
options = [option.strip() for option in options_input.strip().split("\n") if option.strip()]

if teams and options:
    st.header("Set Preferences")

    # Initialize or load preferences DataFrame
    if 'prefs_df' not in st.session_state or st.session_state.prefs_df.shape != (len(teams), len(options)):
        st.session_state.prefs_df = pd.DataFrame(
            50,  # default preference value
            index=teams,
            columns=options
        )

    # Editable preference matrix
    edited_df = st.data_editor(
        st.session_state.prefs_df,
        num_rows="fixed",
        use_container_width=True
    )

    st.session_state.prefs_df = edited_df

    if st.button("Run Matching"):
        # Convert preferences DataFrame to sorted preference lists
        preferences = {}
        for team in teams:
            sorted_options = edited_df.loc[team].sort_values().index.tolist()
            preferences[team] = sorted_options

        # Run matching algorithm
        matches = stable_marriage(preferences, options)

        # Display results
        st.subheader("Matching Results")
        results_df = pd.DataFrame(matches.items(), columns=["Team", "Matched Option"])
        st.table(results_df)
else:
    st.warning("Please enter at least one team and one option.")