import json
import pandas as pd
import numpy as np
import psycopg2
from datetime import datetime
import time
import concurrent
import os
import subprocess
import sys
sys.path.insert(0, "/opt/cm/lib/ops/mediadb/")

mail_recipients = "mpawar@criticalmention.com krane@criticalmention.com hshaikh@criticalmention.com "

def mail_send(subject, body, file):
    mail_command = " echo \""+ body + "\" | mailx -s \"" + subject + "\" -a " + file + " " + mail_recipients
    status       = subprocess.call(mail_command, shell=True)
    return status

state_file = {}
state_file['is_prod'] = True
state_file['db_id'] = 'mayur'
state_file['db_pass'] = '$st$$7qbay671'
cd_df_2 = pd.read_csv(r'Job_curation.csv', encoding='utf-8')
if cd_df_2.shape[0] > 0:
    cd_df_2['replacement'] = cd_df_2['replacement'].str.strip()
    cd_df_2['original'] = cd_df_2['original'].str.strip()
    cd_df_2['original_l'] = cd_df_2['original'].str.lower()
    # cd_df_2 = cd_df_2[['replacement', 'original']]
    f_w = open(r'corrected_job_title_UltraMax.sql', 'w')
    f_w.close()

else:
    cd_df_2 = pd.DataFrame(columns = [['replacement', 'original']])

cd_df = pd.read_csv(r'Job Title curation - Remove1(1).csv', encoding='utf-8')
if cd_df.shape[0] > 0:
    cd_df['original'] = cd_df['original'].str.strip()
    cd_df['original_l'] = cd_df['original'].str.lower()
else:
    cd_df = pd.DataFrame(columns = [['original']])

# connect to database    
def database_connect(query):
    connection = 'connection'
    conn_attemps = 5
    while (connection == 'connection' or connection.closed != 0) and conn_attemps != 0:
        try:
            host_ = 'mediadb.czv2sdjvmqu8.us-east-2.rds.amazonaws.com' if state_file['is_prod'] else "mediadb-qa.czv2sdjvmqu8.us-east-2.rds.amazonaws.com"
            connection = psycopg2.connect(user = state_file['db_id'],
                                            password = state_file['db_pass'],
                                            host = host_,
                                            port = "5432",
                                            database = "mediadb")

            conn_attemps = 5
        except:
            conn_attemps -= 1
    try:
        if conn_attemps == 0 and connection.closed != 0:
            print("database couldn't connect")
            sys.exit()
    except:
            print("database couldn't connect")
            sys.exit()
    
    df = pd.read_sql(query , connection)
    connection.close()
    print("done")
    return df

# remove function
def case_correction_remove(rec):
    the_split = rec[1].split(',')
    change_case = False
    the_split_p = []
    try:
        tag_ = rec[3]+',remove'
    except IndexError:
        tag_ = rec[3]+',remove'
    for elem in the_split:
        elem_strip = elem.strip()
        if elem_strip != '':
            the_find = cd_df[cd_df['original_l'] == elem_strip.lower()]
            if the_find.shape[0] > 0:
                the_split_p.append('')
                change_case = True
            else:
                the_split_p.append(elem_strip)
        else:
            change_case = True

    the_split_p = [ij for ij in the_split_p if ij != '']
    the_split_p = ', '.join(the_split_p)
    
    if change_case:
        if rec[1].lower() != the_split_p.lower():
            if the_split_p == '': 
                id_, topics_ = rec[0], 'NULL'
            else:
                the_split_p = the_split_p.replace(r"'", "''")
                id_, topics_ = rec[0], the_split_p
        else:
            id_, topics_ = np.nan, np.nan
    else:
        id_, topics_ = np.nan, np.nan
    return id_, topics_, rec[2], tag_

# remove function_2
def case_correction_remove_2(rec):
    try:
        the_split = rec[1].split(',')
    except AttributeError:
        the_split = ""    
    change_case = False
    the_split_p = []
    try:
        tag_ = 'remove'
    except IndexError:
        tag_ = 'remove'

    for elem in the_split:
        elem_strip = elem.strip()
        if elem_strip != '':
            the_find = cd_df[cd_df['original_l'] == elem_strip.lower()]
            if the_find.shape[0] > 0:
                the_split_p.append('')
                change_case = True
            else:
                the_split_p.append(elem_strip)
        else:
            change_case = True

    the_split_p = [ij for ij in the_split_p if ij != '']
    the_split_p = ', '.join(the_split_p)
    
    if change_case:
        if rec[1].lower() != the_split_p.lower():
            if the_split_p == '': 
                id_, topics_ = rec[0], 'NULL'
            else:
                the_split_p = the_split_p.replace(r"'", "''")
                id_, topics_ = rec[0], the_split_p
        else:
            id_, topics_ = np.nan, np.nan
    else:
        id_, topics_ = np.nan, np.nan
    return id_, topics_, rec[1], tag_

# replace function 2
def case_correction_replace(rec):
    try:
        the_split = rec[1].split(',')
    except AttributeError:
        the_split = ""

    change_case = False
    the_split_p = []
    tag_ = 'replace'
    for elem in the_split:
        elem_strip = elem.strip()
        if elem_strip != '':
            the_find = cd_df_2[cd_df_2['original_l'] == elem_strip.lower()]
            if the_find.shape[0] > 0:
                the_split_p.append(the_find['replacement'].iat[0])
                change_case = True
            else:
                the_split_p.append(elem_strip)
        else:
            change_case = True

    the_split_p = ', '.join(the_split_p)
    
    if change_case:
        if rec[1].lower() != the_split_p.lower():
            if the_split_p == '': 
                id_, topics_ = rec[0], 'NULL'
            else:
                the_split_p = the_split_p.replace(r"'", "''")
                id_, topics_ = rec[0], the_split_p

        else:
            id_, topics_ = np.nan, np.nan
    else:
        id_, topics_ = np.nan, np.nan

    # print(id_, topics_, rec[1], tag_)
    return id_, topics_, rec[1], tag_

def temp_df(data_):
    x_df = pd.DataFrame(data_, columns=['reporter_id', 'designation', 'designation_old', 'found_in'])
    x_df = x_df[x_df['reporter_id'].isna() == False]
    if x_df.shape[0] > 0:
        x_df['reporter_id'] = x_df['reporter_id'].astype(int)
    return x_df

def find_redundant(dft):
    id_ = []
    updated = []
    tag = []
    old_designation_ = []
    for index in dft.index:

        a_designation = dft['designation'][index]
        if a_designation != 'NULL':
            words = a_designation.split(',')
            words = [x.strip(' ') for x in words]
            words = [x.strip(', ') for x in words]

        if len(words) != len(set(words)):
            test_list = list(set(words))
            words = ", "
            words = words.join(test_list)
            tag1 = dft['found_in'][index]+",redundant"
            des_ = words

            des_old_ = dft['designation_old'][index]
            id_1 = dft['reporter_id'][index]
            tag.append(tag1)
            updated.append(des_)
            old_designation_.append(des_old_)
            id_.append(id_1)

    my_df_ = {'reporter_id': id_, 'designation': updated, 'designation_old':old_designation_, 'found_in':tag}
    dt = pd.DataFrame(my_df_)
    frames = [dft, dt]
    result_7 = pd.concat(frames)
    result_7 = result_7.drop_duplicates(subset='reporter_id', keep="last")
    result_7['reporter_id'] = result_7['reporter_id'].replace(".0", '', regex=True)

    return result_7
 
 # redundant
def find_redundant_2(df):
    df = df.replace(np.nan, 'NULL', regex=True)

    id_ = []
    updated = []
    tag = []
    old_designation_ = []
    for index in df.index:

        a_designation = df['designation'][index]
        if a_designation != 'NULL':
            words = a_designation.split(',')
            words = [x.strip(' ') for x in words]
            words = [x.strip(', ') for x in words]

        if len(words) != len(set(words)):
            test_list = list(set(words))
            words = ", "
            words = words.join(test_list)
            tag1 = "redundant"
            des_ = words

            des_old_ = df['designation'][index]
            id_1 = df['reporter_id'][index]
            tag.append(tag1)
            updated.append(des_)
            old_designation_.append(des_old_)
            id_.append(id_1)


    my_df_ = {'reporter_id': id_, 'designation': updated, 'designation_old':old_designation_, 'found_in':tag}
    dt = pd.DataFrame(my_df_)
    dt['reporter_id'] = dt['reporter_id'].replace(".0", '', regex=True)

    return dt

r_t_df = """Select reporter_id, designation from tbl_reporters where designation is not NULL;"""
r_t_df = database_connect(r_t_df)

now = datetime.utcnow()
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

start_time = time.time()
results = []
for i in r_t_df.to_numpy():
    results.append(case_correction_replace(i))
print("The total time", time.time()-start_time)

case_df_rep = temp_df(results)

results_2 = []
for i in case_df_rep.to_numpy():
    results_2.append(case_correction_remove(i))
print("The total time", time.time()-start_time)

case_df_rep_2 = temp_df(results_2)
frames = [case_df_rep, case_df_rep_2]

result_5 = pd.concat(frames)
result_5 = result_5.drop_duplicates(subset='reporter_id', keep="last")

result_3 = []
for i in r_t_df.to_numpy():
    result_3.append(case_correction_remove_2(i))
print("The total time", time.time()-start_time)

case_df_rep_3 = temp_df(result_3)
frames = [result_5, case_df_rep_3]
result_6 = pd.concat(frames)
result_6 = result_6.drop_duplicates(subset='reporter_id', keep="first")
result_6.to_csv(r'corrected_job_titles_final.csv', index = False)
time.sleep(1)

dft = pd.read_csv("corrected_job_titles_final.csv")
dft = dft.replace(np.nan, 'NULL', regex=True)

file = 'corrected_job_titles_final.csv'
if(os.path.exists(file) and os.path.isfile(file)):
  os.remove(file)

r7 =find_redundant(dft)

# redudancy over full data
rx = find_redundant_2(r_t_df)

frames = [r7, rx]
result_x = pd.concat(frames)
result_x = result_x.drop_duplicates(subset='reporter_id', keep="first")
result_x['reporter_id'] = result_x['reporter_id'].replace('.0', '')
result_x.to_csv(r'../../data/curate_designations/corrected_job_titles_1010.csv', index = False)

body = """
Hello,

designation Curation process has been done.
Kindly go through the attached .csv file 

Regards,
Automation Team.
"""

mail_send("MCDB1205 - Rearrange Emails",body,f'../../data/curate_designations/corrected_job_titles_1010.csv')
# "../../data/curate_designations/{op}.csv"
