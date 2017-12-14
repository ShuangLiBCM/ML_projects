"""
Include functions that take input itcont.txt files of donating information
and output medianvals_by_zip.txt and medianvals_by_date.txt

"""
import os.path
import sys

def file_opener(filename):
    """
    input: name and path of itcont.txt file
    output: list of entries
    """
    text_file = open(filename)
    itcont_list = text_file.read().split('\n')
    return itcont_list

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


# Count sort implementation of the running median
def median_zip(itcont_list):
    input_len = len(itcont_list)
    dict_zip = {}
    output_by_zip = []

    for i in range(input_len):  # Perform serial processing about the data
        itcont = itcont_list[i].split('|')
        core_info = info_extract(itcont)
        if core_info is None:  # Check if the entry is non-empty
            continue

        # Check if ZIP information is valid
        try:
            len_check = core_info['ZIP_CODE'][4]  # check if 'ZIP_CODE' has at least 5 characters
            zip_code = int(core_info['ZIP_CODE'])  # check if 'ZIP_CODE' contains only digit
            trans_amt = int(core_info['TRANSACTION_AMT'])  # check if 'TRANSACTION_AMT' contains only digit
        except:
            continue

        # Create one dictionanry for each recipient and zip
        key = core_info['CMTE_ID'] + core_info['ZIP_CODE']
        # Update the dictionary with new transaction amount
        if key not in dict_zip:
            list_zip = []
        else:
            list_zip = dict_zip[key]

        run_median, trans_num, ttl_amt, dict_zip[key] = running_median(trans_amt, list_zip)
        # Create the first entry for the key
        # Export the current information
        # output_by_zip.append(str(run_median))
        output_by_zip.append(
            '|'.join([core_info['CMTE_ID'], core_info['ZIP_CODE'], str(run_median), str(trans_num), str(ttl_amt)]))
    return output_by_zip


def running_median(trans_amt, list_zip=[]):
    """
    Function for generating running median of a sequence data input
    """
    if len(list_zip) is 0:
        trans_num = 1
        count_arr_below = []  # Store heap as counting sort array for below median
        count_arr_above = []  # Store heap as counting sort array for above median
        count_arr_above_min = 0  # For the above heap, number that represent lowest entry
        run_median = trans_amt
        ttl_amt = trans_amt
    else:
        # Retrieve information from dictionary
        count_arr_below = list_zip[0]
        count_arr_above = list_zip[1]
        count_arr_above_min = list_zip[2]
        run_median = list_zip[3]
        trans_num = list_zip[4]
        ttl_amt = list_zip[5]

        # Update trans_num and ttl_amt
        trans_num = trans_num + 1
        ttl_amt = ttl_amt + trans_amt

        # Update count_arr_below, count_arr_above, count_arr_above_min
        count_arr_below, run_median_below = update_count_arr_below(trans_num, count_arr_below, run_median, trans_amt)
        count_arr_above, count_arr_above_min, run_median_above = update_count_arr_above(trans_num, count_arr_above,
                                                                                        count_arr_above_min, run_median,
                                                                                        trans_amt)
        count_arr_below_max = len(count_arr_below) - 1

        # Update run median

        if run_median_below + run_median_above == 0:
            if trans_num % 2 == 0:
                run_median = round_half((count_arr_below_max + count_arr_above_min) / 2)
            else:
                run_median = trans_amt
        elif run_median_below != 0:
            run_median = run_median_below
        else:
            run_median = run_median_above
    # print(trans_num, trans_amt, count_arr_below, count_arr_above_min, count_arr_above,  run_median)
    list_zip = [count_arr_below, count_arr_above, count_arr_above_min, run_median, trans_num, ttl_amt]
    return run_median, trans_num, ttl_amt, list_zip


def median_date(itcont_list):
    itcont = '|'.join(itcont_list).split('|')

    # Obtain the index with valid data info
    num_entry = int(len(itcont) / 21)

    # Find the entries with Other_Id as [] and TRANS_AMT, TRANS_DT of correct format:

    key_id = [i for i in range(num_entry) if
              (itcont[i * 21 + 15] == '') & (date_format(itcont[i * 21 + 13], itcont[i * 21 + 14])) & (
              len(itcont[i * 21]) > 0)]

    # Generate combination keys with CMTE_ID and TRANS_DT
    keys = [itcont[i * 21] + itcont[i * 21 + 13] for i in key_id]
    unique_key = list(set(keys))
    unique_key.sort()
    output_by_date = []
    for j in range(len(unique_key)):
        indices = [key_id[i] for i, x in enumerate(keys) if x == unique_key[j]]
        trans_num = len(indices)
        trans_amt = [int(itcont[i * 21 + 14]) for i in indices]
        trans_amt.sort()
        ttl_trans = sum(trans_amt)
        if len(trans_amt) == 1:
            median_trans = round(trans_amt)
        elif len(trans_amt) == 2:
            median_trans = round(ttl_trans / 2)
        elif len(trans_amt) % 2 == 0:
            mid_idx = int(len(trans_amt) / 2 - 1)
            median_trans = round(sum(trans_amt[mid_idx:mid_idx + 2]) / 2)
        else:
            mid_idx = int(len(trans_amt) / 2) + 1
            median_trans = round(trans_amt[mid_idx])
        len_key = len(unique_key[j])
        output_by_date.append('|'.join(
            [unique_key[j][:len_key - 8], unique_key[j][len_key - 8:], str(median_trans), str(trans_num),
             str(ttl_trans)]))

    return output_by_date

def update_count_arr_below(trans_num, count_arr_below, run_median, trans_amt):
    if trans_num == 2:
        count_arr_below_max = min(run_median, trans_amt)
        count_arr_below = [0] * (count_arr_below_max + 1)  # Given that round is always up,put the small array first
        count_arr_below[count_arr_below_max] += 1
        run_median = 0  # Not contributing number to be the new median
    elif trans_num % 2 == 1:
        if trans_amt > len(count_arr_below) - 1:
            run_median = 0
        elif trans_amt <= len(count_arr_below) - 1:
            run_median = len(count_arr_below) - 1  # Pop-out max value in count_arr_below as the median
            count_arr_below[trans_amt] += 1
            count_arr_below[len(count_arr_below) - 1] -= 1
            if count_arr_below[len(count_arr_below) - 1] == 0:
                count_arr_below = shrink_count_arr_below(count_arr_below)
    elif trans_num % 2 == 0:
        if trans_amt <= run_median:  # pop in trans_amt into count_arr_below, run_median will be in count_arr_above
            count_arr_below = pop_in_arr_below(count_arr_below, trans_amt)
        else:
            count_arr_below = pop_in_arr_below(count_arr_below, run_median)
        run_median = 0

    return count_arr_below, run_median


def update_count_arr_above(trans_num, count_arr_above, count_arr_above_min, run_median, trans_amt):
    if trans_num == 2:
        count_arr_above_min = max(run_median, trans_amt)
        count_arr_above = [0]
        count_arr_above[0] += 1
        run_median = 0  # Not contributing number to be the new median
    elif trans_num % 2 == 1:
        if trans_amt < count_arr_above_min:
            run_median = 0
        elif trans_amt >= count_arr_above_min:
            run_median = count_arr_above_min  # Pop-out min value in count_arr_above as the median
            count_arr_above, count_arr_above_min = pop_in_arr_above(count_arr_above, count_arr_above_min, trans_amt)
            count_arr_above[0] -= 1
            if count_arr_above[0] == 0:
                count_arr_above, count_arr_above_min = shrink_count_arr_above(count_arr_above, count_arr_above_min)
    elif trans_num % 2 == 0:
        if trans_amt <= run_median:  # Pop in run_median in count_arr_above
            count_arr_above, count_arr_above_min = pop_in_arr_above(count_arr_above, count_arr_above_min, run_median)
        else:
            count_arr_above, count_arr_above_min = pop_in_arr_above(count_arr_above, count_arr_above_min, trans_amt)
        run_median = 0
    return count_arr_above, count_arr_above_min, run_median


def pop_in_arr_below(count_arr_below, value):  # Pop in a value into the count_arr_low
    if value <= len(count_arr_below) - 1:
        count_arr_below[value - 1] += 1
    else:
        count_arr_below_max = len(count_arr_below) - 1
        count_arr_below_new = [0] * (value + 1)
        count_arr_below_new[:count_arr_below_max + 1] = count_arr_below
        count_arr_below = count_arr_below_new
        count_arr_below[len(count_arr_below) - 1] += 1

    return count_arr_below


def pop_in_arr_above(count_arr_above, count_arr_above_min, value):
    if count_arr_above_min <= value < count_arr_above_min + len(count_arr_above):
        min_diff = count_arr_above_min - value
        count_arr_above[min_diff] += 1
    elif value >= count_arr_above_min + len(count_arr_above):
        min_diff = value - (count_arr_above_min + len(count_arr_above) - 1)
        count_arr_above_new = [0] * (len(count_arr_above) + min_diff)
        count_arr_above_new[:len(count_arr_above)] = count_arr_above
        count_arr_above_new[len(count_arr_above_new) - 1] += 1
        count_arr_above = count_arr_above_new
    else:
        min_diff = count_arr_above_min - value
        count_arr_above_new = [0] * (min_diff + len(count_arr_above))
        count_arr_above_new[count_arr_above_min - value:] = count_arr_above
        count_arr_above = count_arr_above_new
        count_arr_above[0] += 1
        count_arr_above_min = value
    return count_arr_above, count_arr_above_min


def shrink_count_arr_below(count_arr_below):
    while count_arr_below[len(count_arr_below) - 1] == 0:
        count_arr_below = count_arr_below[:len(count_arr_below) - 1]
    return count_arr_below


def shrink_count_arr_above(count_arr_above, count_arr_above_min):
    while count_arr_above[0] == 0:
        count_arr_above = count_arr_above[1:len(count_arr_above)]
        count_arr_above_min += 1
    return count_arr_above, count_arr_above_min


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

        if (0 < month < 12) & (0 < date < 32) & (1700 < yr < 2018):
            return True
        else:
            return False
    except:
        return False

def main():

    real_path = sys.argv[1]
    output1 = sys.argv[2]
    output2 = sys.argv[3]

    script_dir = os.getcwd()
    input_path = os.path.join(script_dir, real_path)

    itcont_list = file_opener(input_path)
    median_by_zip = median_zip(itcont_list)
    median_by_date = median_date(itcont_list)

    with open(output1, "w") as test_file:
        test_file.write('\n'.join(median_by_zip))

    with open(output2, "w") as test_file:
        test_file.write('\n'.join(median_by_date))

    return


if __name__ == '__main__':
    main()