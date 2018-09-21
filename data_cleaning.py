import numpy as np
import pandas as pd
import datetime as dt
import os
import shutil
import datetime
import matplotlib.pyplot as plt

os.chdir('./raw_data/')
# CPI data of Northeast Urban from 1997 to 2017

# read cpi data to dataframe, clean, and put to CSV
def clean_cpi(cpi):
    cpi_new = pd.DataFrame()
    cpi_new['Time'] = list(map(lambda x: datetime.datetime(x, 5, 1, 0, 0), cpi['Year']))     + list(map(lambda x: datetime.datetime(x, 11, 1, 0, 0), cpi['Year']))

    cpi_new['Cpi'] = cpi['HALF1'].append(cpi['HALF2']).values
    return cpi_new


# Employment and h_means data 

# flatten any subdirectory
def flatten():
    for file in os.listdir():
        if os.path.isdir(file):
            for subfile in os.listdir(file):
                os.rename(os.getcwd()+'/'+file+'/'+subfile, os.getcwd()+'/'+subfile)


# Execptions: 2009 data files are not properly named (manually found)
def rename():
    os.rename('MSA_dl_1.xls', 'MSA_M2009_dl_1.xls')
    os.rename('MSA_dl_2.xls', 'MSA_M2009_dl_2.xls')
    os.rename('MSA_dl_3.xls', 'MSA_M2009_dl_3.xls')


# put excel files to a dictionary, whose key is file name and value is dataframe
# we use dictionary rather than list, because some files don't have 'year' column --> use dict to get year from file name
def to_dict():
    file_df = {}
    i = 0
    for file in os.listdir():
        if '.xls' in file: 
            file_df[file.replace('.xls', '')] = pd.read_excel(file);
            i = i+1
        elif '.xlsx' in file:
            file_df[file.replace('.xlsx', '')] = pd.read_excel(file);
            i = i+1
    return file_df


# check if a list is the correct header
def header_check(alist):
    return (('PRIM_STATE' in alist) | ('prim_state' in alist))     & (('AREA' in alist) | ('area' in alist))     & (('AREA_NAME' in alist) | ('area_name' in alist))


# keep data with a correct header
def correct_header(df):
    df_data = {}
    for key in df.keys():
        if header_check(df[key].columns.values):
            df_data[key] = df[key]
        else:
            for i in range(len(df[key].index)):
                if header_check(df[key].iloc[i].values):
                    temp_df = df[key].copy()
                    new_header = temp_df.iloc[i]
                    temp_df = temp_df.iloc[(i+1):]
                    temp_df.columns = new_header
                    df_data[key] = temp_df
    # write all headers in the lower case
    for key in df_data.keys():
        df_data[key].columns = list(map(str.lower, df_data[key].columns))
    return df_data


# only keep the dataframe parts containing Buffalo region
def select_buffalo(df_data):
    df_buffalo = {}
    for key in df_data.keys():
        temp = df_data[key].copy()
        if len(temp[(temp['prim_state']=='NY') & (list(map(lambda x: 'Buffalo' in x, temp['area_name'])))].index) > 0:
            df_buffalo[key] = temp[(temp['prim_state']=='NY') & (list(map(lambda x: 'Buffalo' in x, temp['area_name'])))]
    return df_buffalo


# change the keys to timestamps
def string_to_time(astring):
    yr_short = np.array(['97', '98', '99', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',                      '16', '17'])
    yr_full = np.array(['1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',                     '2011', '2012', '2013', '2014', '2015', '2016', '2017'])
    # extract month   (assume May if string not containing 'november')
    if astring.find('november') !=-1:
        month = '11'
    else:
        month = '5'
    # extract year
    search_yr_full = yr_full[np.array(list(map(astring.find, yr_full))) !=-1]
    if len(search_yr_full) !=0:
        year = search_yr_full[0]
    else:
        search_yr_short = yr_short[np.array(list(map(astring.find, yr_short))) !=-1]
        if len(search_yr_short) !=0:
            year = search_yr_short[0]
        else:
            print('error: year of ' + astring + ' not found!')
    if len(year) == 4:
        return datetime.datetime.strptime(year+month, '%Y%m')
    elif len(year) == 2:
        return datetime.datetime.strptime(year+month, '%y%m')
    else:
        print('error: string_to_time(' + astring + '), length of year is wrong!')


# convert keys to timestamps
def key2time(df_buffalo):
    df_time = df_buffalo
    old_keys = tuple(df_time.keys())
    for key in old_keys:
        df_time[string_to_time(key)] = df_time.pop(key)
    # Exception
    df_time[datetime.datetime(2000, 5, 1,0,0)].rename(columns={'occ_titl': 'occ_title'}, inplace=True)
    return df_time





# combine data of different dates
def combine_dates(df_time):
    df_occ = pd.DataFrame()
    for key in df_time.keys():
        if 'group' in df_time[key].columns:
            temp = df_time[key][df_time[key]['group'] == 'major'].copy()
        else:
            temp = df_time[key][df_time[key]['occ_group'] == 'major'].copy()
        temp = temp[['occ_title', 'tot_emp', 'h_mean']]
        temp['occ_title'] = list(map(lambda x: min(x[0: x.find(' occupations')], x[0: x.find(' Occupations')]).lower(), temp['occ_title']))
        temp['date'] = key
        df_occ = df_occ.append(temp)
    return df_occ


# uniformize some occupation namings
def occ_naming(df_occ):
    df_emp = df_occ.pivot_table(values='tot_emp', index='date', columns='occ_title', aggfunc='first')
    df_hmean = df_occ.pivot_table(values='h_mean', index='date', columns='occ_title', aggfunc='first')

    for index in df_emp.index:
        if index < datetime.datetime(2010,1,1,0,0):
            df_emp.loc[index]['community and social service'] = df_emp.loc[index]['community and social services']
            df_hmean.loc[index]['community and social service'] = df_hmean.loc[index]['community and social services']
        if (index < datetime.datetime(2010,1,1,0,0)) & (index > datetime.datetime(2008,1,1,0,0)):
            df_emp.loc[index]['computer and mathematical'] = df_emp.loc[index]['computer and mathematical science']
            df_hmean.loc[index]['computer and mathematical'] = df_hmean.loc[index]['computer and mathematical science']
        if index == datetime.datetime(2009,5,1,0,0):
            df_emp.loc[index]['healthcare practitioners and technical'] = df_emp.loc[index]['healthcare practitioner and technical']
            df_hmean.loc[index]['healthcare practitioners and technical'] = df_hmean.loc[index]['healthcare practitioner and technical']
    df_emp.drop(labels=['all','community and social services', 'computer and mathematical science', 'healthcare practitioner and technical'],              axis=1, inplace=True)
    df_hmean.drop(labels=['all','community and social services', 'computer and mathematical science', 'healthcare practitioner and technical'],              axis=1, inplace=True)
    # tackle '*' cells in h_mean
    df_hmean = df_hmean.replace('*', np.NaN)
    df_hmean.fillna(method='ffill');
    # change object to numerical values
    df_emp = df_emp.applymap(float);
    df_hmean = df_hmean.applymap(float);
    return df_emp, df_hmean


def main():
	try:
		cpi = pd.read_excel('cpi_northeast.xlsx', header=11)
	except:
		print('\033[1;31m\n Error: file cpi_northeast.xlsx Not Found! \n\033[1;m')
		return
		
	clean_cpi(cpi).to_csv('../cpi_northeast.csv')
	print('\ncpi_northeast.csv file created \n')
	
	flatten()
	print('Subdirectory flattened!\n')
	rename()
	print('2009 data file names corrected!\n')
	df = to_dict()
	print('Dictionary created: file names as key, dataframe as value!\n')
	
	df_data=correct_header(df)
	print('Header corrected!\n')
	df_buffalo = select_buffalo(df_data)
	print('Buffalo region data selected out!\n')
	
	df_time = key2time(df_buffalo)
	print('Dict keys converted to TimeStamps')
	
	df_occ = combine_dates(df_buffalo)
	print('Data of different dates combined!\n')
	df_emp, df_hmean = occ_naming(df_occ)
	print('Occupation names uniformized!\n')

	# save emp_tot time series, and h_mean time series, to two CSV files
	df_emp.to_csv('../emp_tot.csv')
	print('emp_tot.csv created!\n')
	df_hmean.to_csv('../h_mean.csv')
	print('h_mean.csv created!\n')

if __name__ == "__main__":
    main()
