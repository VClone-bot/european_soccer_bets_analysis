#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[ ]:


def preprocess(df):
    tmp = []
    for team in set(df.home_team.values).union(set(df.away_team.values)):
        nb_played = len(df[(df.home_team == team)]) + len(df[(df.away_team == team)])
        nb_played_home = len(df[(df.home_team == team)])
        nb_played_away = len(df[(df.away_team == team)])

        nb_goals = df[(df.home_team == team)].home_score.sum() + df[(df.away_team == team)].away_score.sum()
        nb_goals_home = df[(df.home_team == team)].home_score.sum()
        nb_goals_away = df[(df.away_team == team)].away_score.sum()

        nb_taken = df[(df.home_team == team)].away_score.sum() + df[(df.away_team == team)].home_score.sum()
        nb_taken_home = df[(df.home_team == team)].away_score.sum()
        nb_taken_away = df[(df.away_team == team)].home_score.sum()

        df_wins_home = df[(df.home_team == team) & (df.home_score > df.away_score)]
        df_wins_away = df[(df.away_team == team) & (df.home_score < df.away_score)]

        df_even_home = df[(df.home_team == team) & (df.home_score == df.away_score)]
        df_even_away = df[(df.away_team == team) & (df.home_score == df.away_score)]

        df_lose_home = df[(df.home_team == team) & (df.home_score < df.away_score)]
        df_lose_away = df[(df.away_team == team) & (df.home_score > df.away_score)]

        nb_wins = len(df_wins_home) + len(df_wins_away)
        nb_even = len(df_even_home) + len(df_even_away)
        nb_lose = len(df_lose_home) + len(df_lose_away)

        nb_wins_home = len(df_wins_home)
        nb_even_home = len(df_even_home)
        nb_lose_home = len(df_lose_home)

        nb_wins_away = len(df_wins_away)
        nb_even_away = len(df_even_away)
        nb_lose_away = len(df_lose_away)

        goals_ratio = np.round(nb_goals/nb_taken)*100 if nb_taken > 0 else 0
        goal_diff = nb_goals - nb_taken

        tmp.append((
            team,

            nb_played,
            nb_played_home,
            nb_played_away,

            nb_goals,
            nb_taken,
            np.round(nb_goals/nb_played, 2) if nb_played > 0 else 0,
            np.round(nb_taken/nb_played, 2) if nb_played > 0 else 0,

            nb_goals_home,
            nb_goals_away,
            np.round(nb_goals_home/nb_played_home, 2) if nb_played_home > 0 else 0,
            np.round(nb_goals_away/nb_played_away, 2) if nb_played_away > 0 else 0,

            nb_taken_home,
            nb_taken_away,
            np.round(nb_taken_home/nb_played_home, 2) if nb_played_home > 0 else 0,
            np.round(nb_taken_away/nb_played_away, 2) if nb_played_away > 0 else 0,

            nb_wins,
            nb_even,
            nb_lose,
            np.round(nb_wins/nb_played, 2) if nb_played > 0 else 0,
            np.round(nb_even/nb_played, 2) if nb_played > 0 else 0,
            np.round(nb_lose/nb_played, 2) if nb_played > 0 else 0,

            nb_wins_home,
            nb_even_home,
            nb_lose_home,
            np.round(nb_wins_home/nb_played_home, 2) if nb_played_home > 0 else 0,
            np.round(nb_even_home/nb_played_home, 2) if nb_played_home > 0 else 0,
            np.round(nb_lose_home/nb_played_home, 2) if nb_played_home > 0 else 0,

            nb_wins_away,
            nb_even_away,
            nb_lose_away,
            np.round(nb_wins_away/nb_played_away, 2) if nb_played_away > 0 else 0,
            np.round(nb_even_away/nb_played_away, 2) if nb_played_away > 0 else 0,
            np.round(nb_lose_away/nb_played_away, 2) if nb_played_away > 0 else 0
        ))

    df_team_stats = pd.DataFrame(tmp, columns=['team', 
                                               'nb_played', 'nb_played_home', 'nb_played_away',
                                               'nb_goals', 'nb_taken', 'avg_goals', 'avg_taken',
                                               'nb_goals_home', 'nb_goals_away', 'avg_goals_home', 'avg_goals_away',
                                               'nb_taken_home', 'nb_taken_away', 'avg_taken_home', 'avg_taken_away',
                                               'nb_wins', 'nb_even', 'nb_lose',
                                               'avg_wins', 'avg_even', 'avg_lose',
                                               'nb_wins_home', 'nb_even_home', 'nb_lose_home',
                                               'avg_wins_home', 'avg_even_home', 'avg_lose_home',
                                               'nb_wins_away', 'nb_even_away', 'nb_lose_away',
                                               'avg_wins_away', 'avg_even_away', 'avg_lose_away'])

    df_team_stats['offensive_strength'] = df_team_stats.apply(lambda x: np.round(x.avg_goals/df_team_stats.avg_goals.mean(), 2), axis=1)
    df_team_stats['defensive_strength'] = df_team_stats.apply(lambda x: np.round(1/x.avg_taken/df_team_stats.avg_taken.mean(), 2), axis=1)

    df_team_stats['offensive_strength_home'] = df_team_stats.apply(lambda x: np.round(x.avg_goals_home/df_team_stats.avg_goals_home.mean(), 2), axis=1)
    df_team_stats['defensive_strength_home'] = df_team_stats.apply(lambda x: np.round(1/x.avg_taken_home/df_team_stats.avg_taken_home.mean(), 2), axis=1)

    df_team_stats['offensive_strength_away'] = df_team_stats.apply(lambda x: np.round(x.avg_goals_away/df_team_stats.avg_goals_away.mean(), 2), axis=1)
    df_team_stats['defensive_strength_away'] = df_team_stats.apply(lambda x: np.round(1/x.avg_taken_away/df_team_stats.avg_taken_away.mean(), 2), axis=1)

    return df_team_stats

