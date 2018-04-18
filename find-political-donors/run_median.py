"""
define functions that are necessary for generating running medians
"""

import numpy as np

## First version of implementation, not correct
# Define the function to calculate the running median by recipient and zip code
def median_zip(itcont_list):
    input_len = len(itcont_list)
    dict_zip = {}
    output_by_zip = []
    # core_info_track = []
    for i in range(input_len):
        itcont = itcont_list[i].split('|')
        core_info = info_extract(itcont)
        if core_info is None:  # Check if the core information pass criteria
            continue

        # core_info_track.append(core_info)

        # Generate the output for medianvals_by_zip.txt
        # Check if ZIP information is valid
        try:
            len_check = core_info['ZIP_CODE'][4]  # check if 'ZIP_CODE' has at least 5 characters
            zip_code = int(core_info['ZIP_CODE'])  # check if 'ZIP_CODE' contains only digit
            trans_amt = int(core_info['TRANSACTION_AMT'])  # check if 'TRANSACTION_AMT' contains only digit
        except:
            continue

        key = core_info['CMTE_ID'] + core_info['ZIP_CODE']
        if key not in dict_zip:
            trans_num = 1
            run_median_cache = [trans_amt]
            run_median = trans_amt
            ttl_amt = trans_amt
            dict_zip[key] = [run_median_cache, run_median, trans_num, ttl_amt]  # Create the first entry for the key
            output_by_zip.append(
                '|'.join([core_info['CMTE_ID'], core_info['ZIP_CODE'], str(run_median), str(trans_num), str(ttl_amt)]))
        else:
            trans_num = dict_zip[key][2] + 1
            run_median_cache = dict_zip[key][0]
            run_median_cache.append(trans_amt)
            run_median_cache.sort()
            if trans_num == 2:
                run_median = round_half(sum(run_median_cache) / 2)
            elif trans_num % 2 == 0:
                run_median_cache = run_median_cache[1:2]
                run_median = round_half(sum(run_median_cache) / 2)
            else:
                run_median = run_median_cache[1]
            ttl_amt = dict_zip[key][3] + trans_amt
            dict_zip[key] = [run_median_cache, run_median, trans_num, ttl_amt]  # Update the entry for the key
            output_by_zip.append(
                '|'.join([core_info['CMTE_ID'], core_info['ZIP_CODE'], str(run_median), str(trans_num), str(ttl_amt)]))

        # Generate the output for medianvals_by_date.txt
        try:
            len_check = core_info['ZIP_CODE'][4]  # check if 'ZIP_CODE' has at least 5 characters
            zip_code = int(core_info['ZIP_CODE'][0:4])  # check if 'ZIP_CODE' has the correct format
            trans_amt = int(core_info['TRANSACTION_AMT'])  # check if 'TRANSACTION_AMT' has the correct format
        except:
            continue

    return output_by_zip

# Dependency function

def round_half(x):
    if x - np.floor(x) < 0.5:
        return int(np.floor(x))
    else:
        return int(np.ceil(x))

# Provide several solutions based on potential complication in the data
# Location based: Given the information that the incoming data will always follow the FEC format, we will used | splitter and location
# To prepare the data
def info_extract(FEC_list):
    """
    input: list of strings, representing every single enter from the input file,
    output: length 5 dict
    """
    # Check if length of the list is correct:
    if len(FEC_list) < 21:
        return

    str_comb = FEC_list[10] + FEC_list[13]
    if (len(FEC_list[15]) == 0) & (len(FEC_list[0]) > 0) & (len(FEC_list[13]) > 0) & (len(FEC_list[14]) > 0):
        key_info = {}
        key_info['CMTE_ID'] = FEC_list[0]
        key_info['ZIP_CODE'] = FEC_list[10][:5]
        key_info['TRANSACTION_DT'] = FEC_list[13]
        key_info['TRANSACTION_AMT'] = FEC_list[14]
        key_info['OTHER_ID'] = FEC_list[15]
        return key_info
    else:
        return