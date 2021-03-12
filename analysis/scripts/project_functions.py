import pandas as pd
import numpy as np

def load_and_process(path):

    # Method Chain 1 (Load data, rename columns, sort rows by Sport then Year so that we can add win streaks, fix index)

    df1 = (
        pd.read_csv(path)
        .rename(columns={'year':'Year','level':'Level','sport':'Sport','winner':'First Place','winner_metro':'First Place Hometown',
                         'runner_up':'Second Place','runner_up_metro':'Second Place Hometown','final_four3':'Third Place',
                         'final_four3_metro':'Third Place Hometown','final_four4':'Fourth Place','final_four4_metro':'Fourth Place Hometown'}) 
        .sort_values(by=['Sport','Year'])
        .reset_index()
        .drop(columns='index')
        .rename(columns={'level_0':'Index'})
    )
    # Create list of win streaks to add to dataset

    streak = []
    prev = ''
    i = 1
    for team in df1['First Place']:
        if(team == prev):
            i=i+1
        else:
            i=1
        streak.append(i)
        prev = team
    winstreak = pd.Series(streak)

    # Method Chain 2 (add Win Streak column to dataset, capitalize Level column)

    df2 = (
        df1
        .assign(WinStreak=winstreak)
        .rename(columns={'WinStreak':'Win Streak'})
        .assign(Level=df1['Level'].str.capitalize())

    )
    
    return df2