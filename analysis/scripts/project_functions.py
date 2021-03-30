import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns

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

def loadprocess_sortyear(path): #returns a processed dataframe similar to load_and_process, but sorted by year and no win streak column
    
    df = (
        pd.read_csv(path)
        .reset_index()
        .drop(columns='index')
        .rename(columns={'level_0':'Index','year':'Year','level':'Level','sport':'Sport','winner':'First Place','winner_metro':'First Place Hometown',
                         'runner_up':'Second Place','runner_up_metro':'Second Place Hometown','final_four3':'Third Place',
                         'final_four3_metro':'Third Place Hometown','final_four4':'Fourth Place','final_four4_metro':'Fourth Place Hometown'}) 
        .assign(Level=df1['Level'].str.capitalize())
    )
    
    return df

def general_info(df):
    
    print(df.shape)
    print(df.columns)
    print(df.describe())

def streaks(df): #gives information of counts of different win streaks, graphically and as numbers

    print(df['Win Streak'].value_counts())
    sns.countplot(x='Win Streak', data=df).set_title('Count of each Win Streak Length')
    
def placements(df,place,num): #gives top num teams that have placed First the most
    
    sns.countplot(y=place,data=df,order=df[place].value_counts().index[:num]).set_title('Top Teams Based on Placement')
    
def placements_and_streaks(df,place,num): #gives top num teams that have placed First the most, including Win Streaks
    
    sns.countplot(y=place,data=df,hue='Win Streak',order=df[place].value_counts().index[:num]).set_title('Top Teams Based on Placement and Their Win Streaks')
    
def topteam_sport(df): #gives the top 20 teams that have placed First the most, including the sport they win in

    sns.countplot(y='First Place',hue='Sport',data=df,order=df['First Place'].value_counts().index[:20]).set_title(' The Best Teams and the Sport They Play')
    
def winstreak_history(df,team,sport): #gives a visual history of all a team's wins in history
    
    df1 = df[(df['First Place']==team)&(df['Sport']==sport)]
    minyear = df1['Year'].min()
    maxyear = df1['Year'].max()
    sns.distplot(df1['Year'], kde=False, bins=(maxyear-minyear)).set_title('Win History')
    
def team_weakness(df,team,sport): #gives all the teams that have defeated a team in the finals, and the number of times they have beaten them
    
    df2 = df[(df['Second Place']==team)&(df['Sport']==sport)]
    sns.countplot(y='First Place',data=df2,order=df2['First Place'].value_counts().index[:5]).set_title("The New York Giant's Weaknesses")