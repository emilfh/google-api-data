#dates_funcs.py

import os
import pandas as pd
import datetime
from IPython.display import display, HTML

def appendDFToCSV(df, csvFilePath, fileName, sep):
    
            fileNameFull = csvFilePath + fileName
            print(fileNameFull)
            if not os.path.isfile(fileNameFull):
                df.to_csv(fileNameFull, mode='a', index=0, sep=sep)
            elif len(df.columns) != len(pd.read_csv(fileNameFull, nrows=1, sep=sep).columns):
                raise Exception("Columns do not match!! Dataframe has " + str(len(df.columns)) + " columns. CSV file has " + str(len(pd.read_csv(fileNameFull, nrows=1, sep=sep).columns)) + " columns.")
            #elif not (df.columns == pd.read_csv(fileNameFull, nrows=1, sep=sep).columns).all():
            #    raise Exception("Columns and column order of dataframe and csv file do not match!!")
            else:
                df.to_csv(fileNameFull, mode='a', index=0, sep=sep, header=False)

def sortOut_date(df):
    # Convert datecolumns (str)) to datetime object
    df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')

    # Create new columns using datetime
    df["dateFull"] = df["date"].dt.date
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter
    df["month"] = df["date"].dt.month
    df["monthName"] = df["date"].dt.month_name()
    df["week"] = df["date"].dt.isocalendar().week
    df["weekday"] = df["date"].dt.isocalendar().day
    df['weekdayName'] = df["date"].dt.strftime("%A")

    # Drop date column
    df.drop(columns=['date'],inplace=True)

    # Rearrange columns so all columms with date-info comes first (8 last columns)
    df = pd.concat([df.iloc[:,-8:], df.iloc[:,0:-8]], axis="columns")

    # Sort df according to sortOrder
    sortOrder = True
    df = df.sort_values(list(df.columns.values), ascending=sortOrder)

    return df

def sortOut_dateHour(df):
    # Convert datecolumns (str)) to datetime object
    df['dateHour'] = pd.to_datetime(df['dateHour'],format='%Y%m%d%H')

    # Create new columns using datetime
    df["dateTime"] = df["dateHour"]
    df["dateFull"] = df["dateHour"].dt.date
    df["year"] = df["dateHour"].dt.year
    df["quarter"] = df["dateHour"].dt.quarter
    df["month"] = df["dateHour"].dt.month
    df["monthName"] = df["dateHour"].dt.month_name()
    df["week"] = df["dateHour"].dt.isocalendar().week
    df["weekday"] = df["dateHour"].dt.isocalendar().day
    df['weekdayName'] = df["dateHour"].dt.strftime("%A")
    df["time"] = df["dateHour"].dt.time
    df["hour"] = df["dateHour"].dt.hour

    # Drop datehour column
    df.drop(columns=['dateHour'],inplace=True)

    # Rearrange columns so all columms with date-info comes first (11 last columns)
    df = pd.concat([df.iloc[:,-11:], df.iloc[:,0:-11]], axis="columns")

    # Sort df according to sortOrder
    sortOrder = True
    df = df.sort_values(list(df.columns.values), ascending=sortOrder)

    return df

def sortOut_date_short(df):
    # Convert datecolumns (str)) to datetime object
    df['date'] = pd.to_datetime(df['date'],format='%Y%m%d')

    # Create new columns using datetime
    df["dateFull"] = df["date"].dt.date

    # Drop date column
    df.drop(columns=['date'],inplace=True)

    # Rearrange columns so all columms with date-info comes first (1 last columns)
    df = pd.concat([df.iloc[:,-1:], df.iloc[:,0:-1]], axis="columns")

    # Sort df according to sortOrder
    sortOrder = True
    df = df.sort_values(list(df.columns.values), ascending=sortOrder)

    return df

def sortOut_dateHour_short(df):
    # Convert datecolumns (str)) to datetime object
    df['dateHour'] = pd.to_datetime(df['dateHour'],format='%Y%m%d%H')

    # Create new columns using datetime
    df["dateTime"] = df["dateHour"]
    df["dateFull"] = df["dateHour"].dt.date
    df["time"] = df["dateHour"].dt.time

    # Drop datehour column
    df.drop(columns=['dateHour'],inplace=True)

    # Rearrange columns so all columms with date-info comes first (3 last columns)
    df = pd.concat([df.iloc[:,-3:], df.iloc[:,0:-3]], axis="columns")

    # Sort df according to sortOrder
    sortOrder = True
    df = df.sort_values(list(df.columns.values), ascending=sortOrder)

    return df

# Function to fully display dataframe
def force_show_all(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
        display(HTML(df.to_html()))
# ... now when you're ready to fully display df:
#force_show_all(df)

def sortOut_date_searchFormat(df):
    # Convert datecolumns (str)) to datetime object
    df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')

    # Create new columns using datetime
    df["dateFull"] = df["date"].dt.date
    df["year"] = df["date"].dt.year
    #df["quarter"] = df["date"].dt.quarter
    df["month"] = df["date"].dt.month
    #df["monthName"] = df["date"].dt.month_name()
    #df["week"] = df["date"].dt.isocalendar().week
    #df["weekday"] = df["date"].dt.isocalendar().day
    #df['weekdayName'] = df["date"].dt.strftime("%A")

    # Drop date column
    df.drop(columns=['date'],inplace=True)

    # Rearrange columns so all columms with date-info comes first (8 last columns)
    df = pd.concat([df.iloc[:,-3:], df.iloc[:,0:-3]], axis="columns")

    # Sort df according to sortOrder
    sortOrder = True
    df = df.sort_values(list(df.columns.values), ascending=sortOrder)

    return df

def split_years(dt):
    dt['dateFull'] = pd.to_datetime(dt['dateFull'])
    dt['year'] = dt['dateFull'].dt.year
    return [dt[dt['year'] == y] for y in dt['year'].unique()]

def split_months(dt):
    dt['dateFull'] = pd.to_datetime(dt['dateFull'])
    dt['month'] = dt['dateFull'].dt.month
    return [dt[dt['month'] == y] for y in dt['month'].unique()]