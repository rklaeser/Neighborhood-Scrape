import pandas as pd
from pandas.api.types import is_numeric_dtype
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import seaborn as sns


def two_scales(ax1, time, data1, data2, c1, c2):
    from matplotlib.ticker import FuncFormatter
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

def year_month(df):
    df.sort_values(['Year', 'Month'], ascending=[True, True], inplace=True)
    df['Month'] = df['Month'].astype(str)
    # Adds a leading zero so that months are in the correct order
    df['Month'] = df['Month'].apply(lambda x: x.zfill(2))
    df['Year'] = df['Year'].astype(str)
    df['year_month'] = df['Year'] + '_' + df['Month']  # Convert to strings -r '_' not numeric error

    return df

def Line_Plot(df, Hood_Name):
    # TODO Go back and stop Month and Year from becoming numerics
    count = df.groupby(['year_month', 'type'])['type'].count()  # Complex index print(count.type)
    # count.sort_values(['year_month'], ascending=[True, True], inplace=True)
    total_apts = count.groupby(level=0).sum()

    date = []  # Make list of time
    for i in range(0, len(df['year_month'].unique())):
        cur_date = df['year_month'].unique()[i]
        date.append(cur_date)

    studio, b1, b2, b3, b4 = [], [], [], [], []  # Make list of studio count
    for i in range(0, len(date)):
        try:
            cur_studio = count[date[i]]['Studio']
            studio.append(cur_studio)
        except:
            cur_studio = 0
            studio.append(cur_studio)
        try:
            cur_b1 = count[date[i]]['1 BR']
            b1.append(cur_b1)
        except:
            cur_b1 = 0
            b1.append(cur_b1)
        try:
            cur_b2 = count[date[i]]['2 BRs']
            b2.append(cur_b2)
        except:
            cur_b2 = 0
            b2.append(cur_b2)
        try:
            cur_b3 = count[date[i]]['3 BRs']
            b3.append(cur_b3)
        except:
            cur_b3 = 0
            b3.append(cur_b3)
        try:
            cur_b4 = count[date[i]]['4 BR']
            b4.append(cur_b4)
        except:
            cur_b4 = 0
            b4.append(cur_b4)
    dict = {'studio': studio, 'b1': b1, 'b2': b2, 'b3': b3, 'b4':b4}
    for key, value in dict.items():
        fig, ax = plt.subplots()
        percent = (value/total_apts) * 100
        ax1, ax2 = two_scales(ax, date, percent, value, 'r', 'b')
        color_y_axis(ax1, 'r')
        color_y_axis(ax2, 'b')
        ax.set_title(key)

        try:
            path = '/Users/Reed/PycharmProjects/akara/apt_get/data/analysis/' + Hood_Name + '/'
            plt.savefig(path + Hood_Name + '_' + key + '_line_chart.png')
            plt.clf()
        except:
            os.mkdir(path='/Users/Reed/PycharmProjects/akara/apt_get/data/analysis/' + Hood_Name)
            path = '/Users/Reed/PycharmProjects/akara/apt_get/data/analysis/' + Hood_Name + '/'
            plt.savefig(path + Hood_Name + '_' + key + '_line_chart.png')
            plt.clf()
    return

def mypie(slices, labels, title):

    colordict = {}
    if '1 BR' in labels:
        colordict['1 BR'] = 'gold'
    if '2 BRs' in labels:
        colordict['2 BRs'] = 'yellowgreen'
    if '3 BRs' in labels:
        colordict['3 BRs'] = 'lightcoral'
    if 'Studio' in labels:
        colordict['Studio'] = 'lightskyblue'
    if '4 BRs' in labels:
        colordict['4 BRs'] = 'red'
    fig = plt.figure(figsize=[5, 5])
    ax = fig.add_subplot(111)

    pie_wedge_collection = ax.pie(slices, labels=labels, labeldistance=1.05, autopct='%1.1f%%')  # , autopct=make_autopct(slices))

    for pie_wedge in pie_wedge_collection[0]:
        pie_wedge.set_edgecolor('white')
        pie_wedge.set_facecolor(colordict[pie_wedge.get_label()])

    ax.set_title(title)

    return fig, ax, pie_wedge_collection

    # TODO Comment this code
def Pie_Plot(df, Hood_Name):
    # fig = plt.subplots() #  Not sure this is needed
    count = df.groupby(['year_month', 'type'])['type'].count()  # Complex index print(count.type)
    for i in range(0, len(df['year_month'].unique())):
        # Data to plot
        sizes = count[df['year_month'].unique()[i]]
        labels = sizes.keys()
        title = df['year_month'].unique()[i]
        # mypie() creates dictionary that fixes color to each label
        fig, ax, pie_wedge_collection = mypie(sizes, labels, title)
        fig = plt.gcf()
        fig.savefig('/Users/Reed/PycharmProjects/akara/apt_get/data/analysis/' + Hood_Name + '/' + Hood_Name + df['year_month'].unique()[i] + '_type_pie.png')
        plt.clf()

    return

def Description_Dictionary(df):
    df.sort_values(['Year', 'Month'], ascending=[True, True], inplace=True)
    # Loop through columns of df and describe them
    d = {}
    # TODO Drop Unnamed from the df, find where it starts
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # print(df.head())
    # df['Unnamed'] = df['Unnamed'].astype(str)
    hey = df.select_dtypes(exclude=['object'])  # TODO Find out what this is doing

    for column in df:
        # print(str(df[column].name))
        if df[column].name == 'type':
            print('Type here')
            # count = df.groupby(['year_month', 'type'])['type'].mean()
        if is_numeric_dtype(df[column]) == False:
            continue
            # print(df[column].name + ' is String')
        # Performs a description of every numeric, will have to remember to define things as numeric
        if is_numeric_dtype(df[column]) == True:
            try:

                # print(df[column].name + ' is numeric')
                d['median_' + str(df[column].name)] = df.groupby('year_month')[column].median()
                d['mean_' + str(df[column].name)] = df.groupby('year_month')[column].mean()
                d['count_' + str(df[column].name)] = df.groupby('year_month')[column].count()
                # Use plt.show(d['boxplot_priceper_high']) to print boxplot
                d['boxplot_'+str(df[column].name)] = plt.boxplot(df.groupby('year_month')[column])
            except:
                continue
                # print(df[column].name + ' not working')

    # print(d)
    return d

def Make_Current_Time_String():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    return timestr

def DF_to_Csv(df, Hood_Name):

    # Deletes old analysis csv files
    dir_name = '/Users/Reed/PycharmProjects/akara/apt_get/data/analysis/' + Hood_Name + '/'
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".csv"):
            os.remove(os.path.join(dir_name, item))

    # Saves new CSV
    try:
        path = '/Users/Reed/PycharmProjects/akara/apt_get/data/analysis/' + Hood_Name + '/' + Hood_Name + '_analysis.csv'
        df.to_csv(path)
    except:
        os.mkdir(path='/Users/Reed/PycharmProjects/akara/apt_get/data/analysis/' + Hood_Name)
        path = '/Users/Reed/PycharmProjects/akara/apt_get/data/analysis/' + Hood_Name + '/' + Hood_Name + '_analysis..csv'
        df.to_csv(path)

    return

def main(paths):

    for path in paths:
        Hood_Name = path.split('/')[8]
        df = pd.read_csv(path)
        df = year_month(df)
        Line_Plot(df, Hood_Name)
        Pie_Plot(df, Hood_Name)

        d = Description_Dictionary(df)
        dict_frame = pd.DataFrame.from_dict(d)

        DF_to_Csv(dict_frame, Hood_Name)
    return
