import pandas as pd
import time

def Make_Sqft_Int(df):
    df['sqft_low'] = df.sqft.str.split('-').str[0]
    df['sqft_high'] = df.sqft.str.split('-').str[1]
    df['sqft_low'] = df.sqft_low.str.replace('[^0-9]', '')
    df['sqft_high'] = df.sqft_high.str.replace('[^0-9]', '')

    # If there is not a '-' in df.sqft, assign df.sqft_low to df.sqft_high
    df.loc[df.sqft.str.find('-') == -1, 'sqft_high'] = df.sqft_low

    # Converts to float
    df.sqft_low = pd.to_numeric(df.sqft_low, downcast='float')
    df.sqft_high = pd.to_numeric(df.sqft_high, downcast='float')

    df.drop(['sqft'], axis=1)

    return df

def Make_Rent_Int(df):
    # Drops Call for Rent Observations
    df = df[df.rent != 'Call for Rent'].reset_index(drop=True)

    df['rent_low'] = df.rent.str.split('-').str[0]
    df['rent_high'] = df.rent.str.split('-').str[1]
    df['rent_low'] = df.rent_low.str.replace('[^0-9]', '')
    df['rent_high'] = df.rent_high.str.replace('[^0-9]', '')

    # If there is not a '-' in df.rent, assign df.rent_low to df.rent_high
    df.loc[df.rent.str.find('-') == -1, 'rent_high'] = df.rent_low

    # Converts to float
    df.rent_low = pd.to_numeric(df.rent_low, downcast='float')
    df.rent_high = pd.to_numeric(df.rent_high, downcast='float')

    df.drop(['rent'], axis=1)

    return df

def Clean_Outliers(df):
    # TODO Apply Clean_Outliers to all columns
    # Expand this to rent variable too
    # The commented code can be used to show the change in the data
    median_sqft = df['sqft'].median()
    median_rent_low = df['rent_low'].median()
    median_rent_high = df['rent_high'].median()
    #     mean = df['sqft'].mean()
    #     len_sqft = len(df['sqft'])
    #     print('Median_sqft: ' + str(median))
    #     print('Mean_sqft: ' + str(mean))
    #     print('len_sqft: ' + str(len_sqft))
    #     plt.boxplot(df['sqft'])
    #     plt.show()
    upperbound_sqft = median_sqft * 5
    df = df[df['sqft_low'].le(upperbound_sqft)]
    #     upperbound_rent_low = median_rent_low*5
    #     df = df[df['sqft'].le(upperbound_rent_low)]
    #     upperbound_rent_high = median_rent_high*5
    #     df = df[df['sqft'].le(upperbound_rent_high)]
    #     print('Median_sqft: ' + str(median))
    #     print('Mean_sqft: ' + str(mean))
    #     print('len_sqft: ' + str(len_sqft))
    #     plt.boxplot(df['sqft'])
    #     plt.show()
    return df

def Standardize_Type_Names(df):
    # If there is a '3' in df.type, assign '3 BRs' to df.type
    df.loc[df.type.str.find('3') != -1, 'df_type'] = '3 BRs'
    # "  "
    df.loc[df.type.str.find('2') != -1, 'df_type'] = '2 BRs'
    # "  "
    df.loc[df.type.str.find('1') != -1, 'df_type'] = '1 BRs'
    return df

# def Descriptive_Graphs
def Create_Price_Per(df):
    df['priceper_high_low'] = df['rent_high'] / df['sqft_low']
    df['priceper_low_low'] = df['rent_low'] / df['sqft_low']
    df['priceper_high_high'] = df['rent_high'] / df['sqft_high']
    df['priceper_low_high'] = df['rent_low'] / df['sqft_high']
    return df

def Make_Current_Time_String():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    return timestr

def DF_to_Csv(df, Hood_Name, timestr):
    import os
    try:
        path = '/Users/Reed/PycharmProjects/akara/apt_get/data/data_clean/' + Hood_Name + '/' + Hood_Name + "_clean" + timestr + '.csv'
        df.to_csv(path)
    except:
        os.mkdir(path='/Users/Reed/PycharmProjects/akara/apt_get/data/data_clean/' + Hood_Name)
        path = '/Users/Reed/PycharmProjects/akara/apt_get/data/data_clean/' + Hood_Name + '/' + Hood_Name + "_clean" + timestr + '.csv'
        df.to_csv(path)

    return path

def main(paths):

    paths_clean = []
    for path in paths:
        # Load
        df = pd.read_csv(path)

        # Process
        df = Make_Sqft_Int(df)
        df = Make_Rent_Int(df)
        # df = Clean_Outliers(df)
        df = Standardize_Type_Names(df)
        df = Create_Price_Per(df)

        # Save
        timestr = Make_Current_Time_String()
        Hood_Name = path.split('/')[8]
        # Exports to Excel, Time is current run time, not when the apartments are from
        path = DF_to_Csv(df, Hood_Name, timestr)
        paths_clean.append(path)

    return paths_clean


