"""
Class to generate specific test case for unittest
"""
from datetime import date
import random
import sys
import os.path
import numpy as np

# Generate total test data size as: 20*10*5 = 1000
# Simulate CMTE_ID

def test_median(itcont_ttl, reci_test=[1,1], zip_test=[1,0], date_test=[1,0], if_test_ID=0):
    correct_reci = reci_test[0]
    wrong_reci = reci_test[1]
    reci_list = []

    for i in range(correct_reci):
        reci_list.append(''.join(random.choice('0123456789ABCDEFG') for i in range(9)))

    for i in range(wrong_reci):
        reci_list.append('')

    # Simulate ZIP
    correct_zip = zip_test[0]
    wrong_zip = zip_test[1]
    zip_list = []

    for i in range(correct_zip):
        zip_list.append(''.join(random.choice('0123456789') for i in range(9)))

    for i in range(wrong_zip):
        if i < wrong_zip // 2:
            zip_list.append(str(random.randint(1, 500)))
        else:
            zip_list.append(''.join(random.choice('0123456789ABCDEFG') for i in range(5)))

    # Simulate Trans_DT
    correct_date = date_test[0]
    wrong_date = date_test[1]
    date_list = []

    for i in range(correct_date):
        m, d, y = true_date_gen()
        date_list.append(''.join([m, d, y]))

    for i in range(wrong_date):
        m, d, y = false_date_gen()
        date_list.append(''.join([m, d, y]))

    # Simulate Other_ID
    ttl_correct_case = correct_reci * correct_zip * correct_date

    correct_ID = ttl_correct_case
    ID_list = []

    if if_test_ID:
        wrong_ID = correct_ID
    else:
        wrong_ID = 0

    for i in range(correct_ID):
        ID_list.append('')
    for i in range(wrong_ID):
        ID_list.append(''.join(random.choice('0123456789ABCDEFG') for i in range(9)))

    num_case = 6
    test_data_list = []
    count = 1
    amt_track_zip = {}
    amt_track_date = []
    for i in range(len(reci_list)):
        for j in range(len(zip_list)):
            key = str(reci_list[i]) + str(zip_list[j][:5])
            if (i < correct_reci) & (j < correct_zip):
                amt_track_zip[key] = []
            for k in range(len(date_list)):
                random.seed(count)
                samp_index = random.randint(1, num_case)
                itcont_samp = itcont_ttl[samp_index].split('|')
                itcont_samp[0] = reci_list[i]
                itcont_samp[10] = zip_list[j]
                itcont_samp[13] = date_list[k]
                itcont_samp[15] = 'test'
                amt_tmp = random.randint(0, 100)
                if (i < correct_reci) & (j < correct_zip):
                    amt_track_zip[key].append(amt_tmp)
                if (i < correct_reci) & (k < correct_date):
                    amt_track_date.append(amt_tmp)
                itcont_samp[14] = str(amt_tmp)
                count += 1
                test_data_list.append('|'.join(itcont_samp))

    test_data_output = '\n'.join(test_data_list)

    return test_data_output, amt_track_zip, amt_track_date, test_data_list

def test_zip_ans(test_data_list, amt_track):
    output_by_zip = []
    count_dict = {}
    for i in range(len(test_data_list)):
        core_info = info_extract(test_data_list[i].split('|'))
        if core_info is None:  # Check if the entry is non-empty
            continue

        key = core_info['CMTE_ID'] + core_info['ZIP_CODE']

        if key not in amt_track:
            continue

        if key not in count_dict:
            count_dict[key] = 0
        else:
            count_dict[key] += 1

        run_median = round_half(np.median(amt_track[key][:count_dict[key]+1]))
        ttl_amt = sum(amt_track[key][:count_dict[key]+1])
        trans_num = count_dict[key]+1
        output_by_zip.append(
           '|'.join([core_info['CMTE_ID'], core_info['ZIP_CODE'], str(run_median), str(trans_num), str(ttl_amt)]))
    return output_by_zip

def test_date_ans(test_data_list, amt_track_date):
    itcont = '|'.join(test_data_list).split('|')

    # Obtain the index with valid data info
    num_entry = int(len(itcont) / 21)

    # Find the entries with Other_Id as [] and TRANS_AMT, TRANS_DT of correct format:
    key_id = []
    keys = []
    for i in range(num_entry):
        core_info = info_extract(test_data_list[i].split('|'))

        if core_info is None:
            continue

        if (core_info['OTHER_ID'] == '') & (len(core_info['CMTE_ID']) > 0) & (date_format(core_info['TRANSACTION_DT'], core_info['TRANSACTION_AMT'])):
            try:
                key_id.append(i)
                keys.append(core_info['CMTE_ID'] + core_info['TRANSACTION_DT'])
            except:
                continue

    # Generate combination keys with CMTE_ID and TRANS_DT
    unique_key = list(set(keys))
    unique_key.sort()
    output_by_date = []
    for j in range(len(unique_key)):
        indices = [i for i, x in enumerate(keys) if x == unique_key[j]]
        trans_num = len(indices)
        trans_amt = [amt_track_date[i] for i in indices]
        ttl_trans = sum(trans_amt)
        median_trans = int(round(np.median(trans_amt)))
        len_key = len(unique_key[j])
        output_by_date.append('|'.join(
            [unique_key[j][:len_key - 8], unique_key[j][len_key - 8:], str(median_trans), str(trans_num),
             str(ttl_trans)]))

    return output_by_date

def file_opener(filename):
    """
    input: name and path of itcont.txt file
    output: list of entries
    """
    text_file = open(filename)
    itcont_list = text_file.read().split('\n')
    return itcont_list

def info_extract(FEC_list):
    """
    input: list of strings, representing every single enter from the input file,
    output: length 5 dict
    """
    # Check if length of the list is correct:
    if len(FEC_list) < 21:
        return

    if (len(FEC_list[15]) == 0) & (len(FEC_list[0]) > 0) &(len(FEC_list[13]) > 0) & (len(FEC_list[14]) > 0):
        key_info = {}
        key_info['CMTE_ID'] = FEC_list[0]
        key_info['ZIP_CODE'] = FEC_list[10][:5]
        key_info['TRANSACTION_DT'] = FEC_list[13]
        key_info['TRANSACTION_AMT'] = FEC_list[14]
        key_info['OTHER_ID'] = FEC_list[15]
        return key_info
    else:
        return

def true_date_gen():
    start_date = date.today().replace(day=1, month=1, year=2000).toordinal()
    end_date = date.today().toordinal()
    random_day = date.fromordinal(random.randint(start_date, end_date))
    date_str = ''.join([date_to_str(random_day.month), date_to_str(random_day.day), date_to_str(random_day.year)])
    if date_format(date_str,1) is False:
        print(date_str)

    return date_to_str(random_day.month), date_to_str(random_day.day), date_to_str(random_day.year)


def false_date_gen():
    month = random.randint(13, 30)
    day = random.randint(32, 200)
    year = random.randint(100, 1000)

    if month < 15:
        month = 0

    return date_to_str(month), date_to_str(day), date_to_str(year)


def date_to_str(num_info):
    if num_info < 10:
        return '0' + str(num_info)
    else:
        return str(num_info)

def round_half(x):
    if x - int(x) < 0.5:
        return int(x)
    else:
        return int(x) + 1

def date_format(date_str, amt_str):
    """
        date_str: string to check
    """
    try:
        month = int(date_str[:2])
        date = int(date_str[2:4])
        yr = int(date_str[-4:])
        amt = int(amt_str)

        if (0 < month < 13) & (0 < date < 32) & (1700 < yr < 2018):
            return True
        else:
            return False
    except:
        return False


def main(reci_test=[10,10], zip_test=[10,10], date_test=[100,10], if_test_ID=0):

    real_path = sys.argv[1]
    output1 = sys.argv[2]
    output2 = sys.argv[3]
    output3 = sys.argv[4]

    script_dir = os.getcwd()
    input_path = os.path.join(script_dir, real_path)

    itcont_ttl = file_opener(input_path)
    test_data, amt_track_zip, amt_track_date, test_data_list = test_median(itcont_ttl, reci_test, zip_test, date_test, if_test_ID)
    output_by_zip = test_zip_ans(test_data_list, amt_track_zip)
    output_by_date = test_date_ans(test_data_list, amt_track_date)

    with open(output1, "w") as output1_file:
        output1_file.write(test_data)

    with open(output2, "w") as output2_file:
        output2_file.write('\n'.join(output_by_zip))

    with open(output3, "w") as output2_file:
        output2_file.write('\n'.join(output_by_date))

    return

if __name__ == '__main__':
    main()
