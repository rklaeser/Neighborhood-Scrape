import pandas as pd
from pandas.api.types import is_numeric_dtype
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np


def two_scales(ax1, time, data1, data2, c1, c2):

    """

    Parameters
    ----------
    ax : axis
        Axis to put two scales on

    time : array-like
        x-axis values for both datasets

    data1: array-like
        Data for left hand scale

    data2 : array-like
        Data for right hand scale

    c1 : color
        Color for line 1

    c2 : color
        Color for line 2

    Returns
    -------
    ax : axis
        Original axis
    ax2 : axis
        New twin axis
    """
    x = np.arange(0.1, len(time), 1)
    ax2 = ax1.twinx()

    ax1.plot(x, data1, color=c1)
    ax1.set_xlabel('dates')
    plt.xticks(x, time)
    ax1.set_ylabel('percent')

    ax2.plot(x, data2, color=c2)
    ax2.set_ylabel('count')
    return ax1, ax2


# Change color of each axis
def color_y_axis(ax, color):
    """Color your axes."""
    for t in ax.get_yticklabels():
        t.set_color(color)
    return None

def Percent_Type(df):
    # TODO Go back and stop Month and Year from becoming numerics
    df.sort_values(['Year', 'Month'], ascending=[True, True], inplace=True)
    df['Month'] = df['Month'].astype(str)
    df['Year'] = df['Year'].astype(str)
    df['month_year'] = df['Month'] + '_' + df['Year']  # Convert to strings or '_' not numeric error
    count = df.groupby(['month_year', 'type'])['type'].count()  # Complex index print(count.type)
    sum = count.groupby(level=0).sum()

    date = []  # Make list of time
    for i in range(0, len(df['month_year'].unique())):
        cur_date = df['month_year'].unique()[i]
        date.append(cur_date)

    studio = []  # Make list of studio count
    for i in range(0, len(date)):
        try:
            cur_studio = count[date[i]]['Studio']
            studio.append(cur_studio)
        except:
            cur_studio = 0
            studio.append(cur_studio)
            continue

    fig, ax = plt.subplots()
    percent = (studio/sum) * 100
    ax1, ax2 = two_scales(ax, date, percent, studio, 'r', 'b')
    color_y_axis(ax1, 'r')
    color_y_axis(ax2, 'b')
    plt.show()

    # TODO Comment this code
    for i in range(0, len(df['month_year'].unique())):
        # Data to plot
        labels = count[df['month_year'].unique()[i]].keys()
        sizes = count[df['month_year'].unique()[i]]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
        # explode = (0.1, 0, 0, 0)  # explode 1st slice
        # Plot
        fig = plt.pie(sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
        plt.title(df['month_year'].unique()[i])
        plt.axis('equal')
        plt.show()
    return

def Description_Dictionary(df):
    # Loop through columns of df and describe them
    d = {}
    df['Month'] = df['Month'].astype(str)
    df['Year'] = df['Year'].astype(str)
    df['month_year'] = df['Month'] + '_' + df['Year']  # Convert to strings or '_' not numeric error
    # TODO Drop Unnamed from the df, find where it starts
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # print(df.head())
    #df['Unnamed'] = df['Unnamed'].astype(str)
    hey = df.select_dtypes(exclude=['object'])  # what is this doing??

    for column in df:
        # print(str(df[column].name))
        if is_numeric_dtype(df[column]) == False:
            continue
            # print(df[column].name + ' is String')
        # Performs a description of every numeric, will have to remember to define things as numeric
        if is_numeric_dtype(df[column]) == True:
            try:
                # print(df[column].name + ' is numeric')
                d['median_' + str(df[column].name)] = df.groupby('month_year')[column].median()
                d['mean_' + str(df[column].name)] = df.groupby('month_year')[column].mean()
                d['count_' + str(df[column].name)] = df.groupby('month_year')[column].count()
                # Use plt.show(d['boxplot_priceper_high']) to print boxplot
                d['boxplot_'+str(df[column].name)] = plt.boxplot(df.groupby('month_year')[column])
            except:
                continue
                # print(df[column].name + ' not working')

    # print(d)
    return d

def main():
    # Loading
    file = '/Users/Reed/PycharmProjects/akara/apt_get/data/data_clean/midtown-nashville-nashville-tn/midtown-nashville-nashville-tn_clean20180208-144404.csv'
    df = pd.read_csv(file)
    # Functions
    Percent_Type(df)
    # TODO Fix Description_Dictionary(df)
    d = Description_Dictionary(df)

    print(d)
    # #Saving
    # timestr = Make_Current_Time_String()
    # import re
    # Hood_Name = file.split('/')[8]
    # # Exports to Excel, Time is current run time, not when the apartments are from
    # import os
    # path = '/Users/Reed/PycharmProjects/akara/apt_get/data/data_clean/' + Hood_Name + '/' + Hood_Name + "_clean" + timestr + '.xlsx'
    # # + Hood_Name + '/' + Hood_Name + "_clean" + timestr + '.xlsx'
    # DF_to_Excel(df, path)

    return df

df = main()

