#!/usr/bin/env python
# coding: utf-8

# In[7]:


get_ipython().run_cell_magic('time', '', '\n# Import Modules\nimport pandas as pd\nimport numpy as np\n\nimport datetime\nimport dateparser\nfrom datetime import date, timedelta\n\n# Import Modules\nimport os.path\nfrom googleapiclient.discovery import build\nfrom google_auth_oauthlib.flow import InstalledAppFlow\nfrom google.auth.transport.requests import Request\nfrom google.oauth2.credentials import Credentials\n\nimport itertools\n\nimport sys\n# adding Notebooksfolder to the system path\nsys.path.insert(0, \'/Users/emil/miniforge3/envs/googleapi/Notebooks\')\n\\\nimport importlib\nimport dates_funcs\nimportlib.reload(dates_funcs)\nfrom dates_funcs import appendDFToCSV\n\n# ---------------------------------------------------------------------------------------------------------------------\n\n#FRAN https://www.shortautomaton.com/connecting-to-google-search-console-api-with-python/ \n\n# ---------------------------------------------------------------------------------------------------------------------\n\n# Now to print to log when program running \nnowDT = datetime.datetime.now()\nnow = datetime.datetime.strftime(nowDT,\'%Y-%m-%d_%H:%M:%S\')\nprint("Script started: "+now)\nprint("\\n")\n\n# Check of latest Date already fetched data for\nf = open("latestDate.txt")\nmaxSavedDate = f.read()\nf.close()\n# print("Previously fetched data up to and including: "+ maxSavedDate)\nmaxSavedDateDT = datetime.datetime.strptime(maxSavedDate,\'%Y-%m-%d\').date()\nprint("Last date saved: "+maxSavedDate)\nprint("\\n")\n\n# Todays date\ntodayDT = date.today()\ntoday = datetime.datetime.strftime(todayDT,\'%Y-%m-%d\')\n\n# Two days ago to use as end date, since search console is not updated daily\nthree_days_agoDT = todayDT + datetime.timedelta(days=-2)\nthree_days_ago = datetime.datetime.strftime(three_days_agoDT,\'%Y-%m-%d\')\n\n# start_date as the next day as maxSavedDate\nstart_dateDT = maxSavedDateDT + datetime.timedelta(days=1)\nstart_date = datetime.datetime.strftime(start_dateDT,\'%Y-%m-%d\')\nprint("Fetching new data, starting: "+start_date)\n\n# test_end_dateDT = three days ago\nend_dateDT = three_days_agoDT\nend_date = datetime.datetime.strftime(end_dateDT,\'%Y-%m-%d\')\n\nprint("up to and including: "+end_date)\n\n# ---------------------------------------------------------------------------------------------------------------------\n\n#MASTER IF\n\nif start_dateDT > maxSavedDateDT and three_days_agoDT >= end_dateDT and todayDT > maxSavedDateDT:\n\n    # START BACKUP or previous .csv files to an archive\n    # DISABLED because taking up lots of space, will enable manually once in a while instead\n    \'\'\'\n    import pathlib\n    import zipfile\n    from zipfile import ZipFile, ZIP_LZMA\n    \n    directory = pathlib.Path("output/")\n\n    try:\n        with ZipFile("backup_date:_"+maxSavedDate+"_written:_"+now+".zip", mode="w",compression=ZIP_LZMA, allowZip64=True) as archive:\n            for file_path in directory.rglob("*"):\n                archive.write(\n                    file_path,\n                    arcname=file_path.relative_to(directory)\n                )\n            print("Previous .csv-files backed up to: backup_until:_"+maxSavedDate+"_written:_"+now+".zip")\n    except BadZipFile as error:\n        print(error)\n    \'\'\'\n    # END BACKUP  \n\n    # ---------------------------------------------------------------------------------------------------------------------\n\n    # CREDENTIALS\n    # Define function to get authorization\n    def gsc_auth(scopes):\n        creds = None\n        # The file token.json stores the user\'s access and refresh tokens, and is\n        # created automatically when the authorization flow completes for the first\n        # time.\n        if os.path.exists(\'token.json\'):\n            creds = Credentials.from_authorized_user_file(\'token.json\', scopes)\n        # If there are no (valid) credentials available, let the user log in.\n        if not creds or not creds.valid:\n            if creds and creds.expired and creds.refresh_token:\n                creds.refresh(Request())\n            else:\n                flow = InstalledAppFlow.from_client_secrets_file(\n                    \'client_secrets.json\', scopes)\n                creds = flow.run_local_server(port=0)\n            # Save the credentials for the next run\n            with open(\'token.json\', \'w\') as token:\n                token.write(creds.to_json())\n    \n        service = build(\'searchconsole\', \'v1\', credentials=creds)\n    \n        return service\n    \n    scopes = [\'https://www.googleapis.com/auth/webmasters.readonly\']\n    \n    # Authorize\n    service = gsc_auth(scopes)\n    # Query Function\n    \n    # ---------------------------------------------------------------------------------------------------------------------\n\n    # Assign Start Row\n    start_row = 0\n    # Create empty DataFrame to combine data into\n    all_search_analytics_df = pd.DataFrame()\n    \n    # Build Request Body\n    sa_request = {\n                #\'startDate\': \'2023-02-02\',\n                #\'endDate\': \'2023-03-01\',\n                \'startDate\': start_date,\n                \'endDate\': end_date,\n                \'dimensions\': ["date","page","device","query","country"],\n                \'rowLimit\': 25000,\n                }\n    \n    site_url = "https://advokatfamiljforsvar.se"\n    \n    # Loop over requests until all rows are pulled into DataFrame\n    while True:\n        sa_request[\'startRow\'] = start_row\n        gsc_search_analytics = service.searchanalytics().query(siteUrl=site_url, body=sa_request).execute()\n    \n        try:\n    \n            all_search_analytics_df = pd.concat([all_search_analytics_df, pd.DataFrame(gsc_search_analytics[\'rows\'])])\n        except KeyError:\n            break\n    \n        if len(gsc_search_analytics[\'rows\']) < 25000:\n            break\n    \n        start_row += 25000\n    \n    # ---------------------------------------------------------------------------------------------------------------------\n    \n    # Cleaning of data\n        \n    # Deep copy\n    df = all_search_analytics_df.copy()\n    \n    df[\'index\'] = df.reset_index().index\n    df.set_index(\'index\',inplace=True)\n    \n    # new df from the column of lists\n    df_split = pd.DataFrame(df[\'keys\'].tolist(), columns=["date","page","device","query","country"])\n    # concat df and split_df\n    df_split[\'index\'] = df_split.reset_index().index\n    df_split.set_index(\'index\',inplace=True)\n    \n    df_concat = pd.concat([df, df_split], axis=1)\n    # display df\n    df = df_concat.drop(\'keys\', axis=1)\n    \n    df = pd.concat([df.iloc[:,-5:], df.iloc[:,0:-5]], axis="columns")\n    \n    df.reset_index(drop=True,inplace=True)\n    \n    df = dates_funcs.sortOut_date_searchFormat(df)\n    \n    # Columns to case matching reference and analytics data\n    df[\'device\'] = df[\'device\'].str.lower()\n    df[\'country\'] = df[\'country\'].str.upper()\n                \n    # Column names to matching reference and analytics data\n    df.rename(columns = {\'country\':\'countryIdLong\', \'page\':\'landingPage\', \'device\':\'deviceCategory\'}, inplace = True)          \n    \n    df = df.replace(\'\', np.nan)\n    print(df.shape)\n    \n    # Split by years\n    df_by_years = dates_funcs.split_years(df)\n    \n    df_by_years_dc = df_by_years.copy()\n    \n    pd.options.mode.chained_assignment = None \n\n    # List of lists\n    df_by_months = [[] for _ in range(len(df_by_years_dc))]\n\n\n    # Split by month\n    \n    for x in range(len(df_by_years_dc)):\n        df_by_months[x] = dates_funcs.split_months(df_by_years_dc[x])\n    \n    pd.options.mode.chained_assignment = \'warn\' \n\n    # Flatten df_by_months[x][y] (two levels) structure to array of dataframes (one level)\n    # IE, list of lists of dataframes into a list of dataframes\n    dfs_array = list(itertools.chain.from_iterable(df_by_months))\n    #dfs_array = df_by_months.to_numpy().flatten(order=\'F\')\n\n    # ---------------------------------------------------------------------------------------------------------------------\n    \n    ## Max time to latestDatefile, write only after writing data to file below.\n        \n    # Find largest date in dataframes, looking at df eventName, which should have all dates. (?)\n    maxTimestamp = df["dateFull"].max()\n    maxTimestampString = datetime.datetime.strftime(maxTimestamp,\'%Y-%m-%d\')\n    maxDate = datetime.datetime.strptime(maxTimestampString,\'%Y-%m-%d\').date()\n\n    print("\\n")\n    print("Fetched data until "+maxTimestampString)\n        \n    # ---------------------------------------------------------------------------------------------------------------------\n    # For all dataframes, select max year and month for naming.\n    # Convert dataframes all datatypes to strings as well.\n    fileNameList = []\n    \n    for x in range(len(dfs_array)):\n        dfs_array[x] = dfs_array[x].astype(str)\n        fileNameList.append(dfs_array[x][\'year\'].min()+\'_\'+dfs_array[x][\'month\'].min())\n    \n    # Convert list of datetime, to list of strings\n    #fileNameList = [dts.strftime("%Y-%m-%d") for dts in fileNameList]\n\n    # Drop columns we have in Master Date file.\n    for x in range(len(dfs_array)):\n        dfs_array[x].drop(columns=[\'year\'],inplace=True)\n        dfs_array[x].drop(columns=[\'month\'],inplace=True)\n    \n    # Loop over all dataframes and write to file with filename of firstdate in df.\n    for x, y in zip(range(len(dfs_array)),fileNameList):\n        dfs_array[x].to_csv(f\'output/csv/search_console_from_{y}.csv\',index=None,mode=\'a\')\n\n    # ---------------------------------------------------------------------------------------------------------------------\n    # If date is larger than priviously max date.\n    if maxDate > maxSavedDateDT:\n        # Write largest date to file\n        f = open("latestDate.txt", \'w\')\n        f.write(maxTimestampString)\n        f.close()\n        \n    print("Written to latestDate.txt")\n    print("\\n")\n    # ---------------------------------------------------------------------------------------------------------------------\n\nelse:\n    print("ERROR")\n\n# Now to print to log when script completed\n\nnowDT = datetime.datetime.now()\nnow = datetime.datetime.strftime(nowDT,\'%Y-%m-%d_%H:%M:%S\')\nprint("Script finished: "+now)\nprint("\\n")\nprint("--------------------------------------------------------------------------------")\nprint("\\n")\n')


# In[ ]:




