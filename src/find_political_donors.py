#!/usr/bin/python
'''
Script      : find_political_donors.py
Description : Script reads/parses input file with political donor data and generates two output files
              organizing funds according to locations and dates for front end processing
Author      : Siddharth Wagh
'''

import argparse, os, sys

# Constant indices for data fields in pipe-delimited input file
CMTE_ID=0
ZIP_CODE=10
TRANSACTION_DT=13
TRANSACTION_AMT=14
OTHER_ID=15

# Constant indices for integer fields in data structures to hold donation information
AMOUNT_LIST=0
DONOR_NUM=1
TOTAL_CONT=2


'''
### Mistakenly calculated average instead of median, can be ignored

def calculate_median(total_cont, donor_num):
    if donor_num and ((total_cont * 100) / donor_num) % 100 < 50:
        return (total_cont / donor_num)
    elif donor_num and  ((total_cont * 100) / donor_num) % 100 >= 50:
        return ((total_cont / donor_num) + 1)
'''


# Function to calculate median from transaction amount list
def find_median(amt_list):
    '''
    Function sorts list of transaction amounts, calculates median
    For odd number of elements, center value is median
    For even number of elements, average of two center values is calculated
    Args: 
        amt_list (list of transaction amounts as they appear in input file)
    Returns: 
        median of list
    '''
    num_cont = len(amt_list)
    sorted_amt_list = sorted(amt_list)
    if num_cont % 2:
        return sorted_amt_list[num_cont/2]
    else:
        med1 = sorted_amt_list[ (num_cont/2) - 1 ]
        med2 = sorted_amt_list[ (num_cont/2) ]
        if (med1 + med2) % 2:
            return (((med1 + med2) / 2) + 1)
        else:
            return ((med1 + med2) / 2)


# Function to validate input for medianvals_by_zip.txt file
def validate_mbz_input(oid, zc, cid, tamt):
    '''
    Function validates fields parsed from input file for output file 1
    Args:
        oid (other id), zc (zip code), cid (cmte_id), tamt (transaction amount)
    Returns:
        True if validation succeeds, False otherwise
    '''
    if len(oid):
        return False
    elif (len(zc) < 4) or (len(zc) > 9):
        return False
    elif (len(cid) != 9):
        return False
    elif not len(tamt):
        return False
    return True
    

# Function to validate input for medianvals_by_date.txt file
def validate_mbd_input(oid, dt, cid, tamt):
    '''
    Function validates fields parsed from input file for output file 2
    Args:
        oid (other id), dt (date), cid (cmte_id), tamt (transaction amount)
    Returns:
        True if validation succeeds, False otherwise
    '''
    if len(oid):
        return False
    elif (len(dt) != 8) or (int(dt[:2]) > 12) or (int(dt[2:4]) > 31):
        return False
    elif (len(cid) != 9):
        return False
    elif not len(tamt):
        return False
    return True

 
# Function to process/parse donor data and create output files
def process_donor_data(infile_path, outfile1_path, outfile2_path):
    '''
    Function to process/parse input file, create relevant data structures and generate required output files
    Args:
        input and output file paths
    Returns:
        None
    '''
    # Dictionary Data structures to hold data for generating output files
    mbz_dict = {}
    mbd_dict = {}

    with open(infile_path, 'r') as inf:
        for line in inf:
            dfield = line.split('|')
            # For valid input parameters, create "medianvals by zip" data structure
            if validate_mbz_input( dfield[OTHER_ID], dfield[ZIP_CODE], dfield[CMTE_ID], dfield[TRANSACTION_AMT] ):
                id_zc_tuple = (dfield[CMTE_ID], dfield[ZIP_CODE][:5]) 
                if id_zc_tuple not in mbz_dict.keys():
                    mbz_dict.update({id_zc_tuple : [[int(dfield[TRANSACTION_AMT])], 1, int(dfield[TRANSACTION_AMT])]})
                else:
                    mbz_dict[id_zc_tuple][TOTAL_CONT] += int(dfield[TRANSACTION_AMT])
                    mbz_dict[id_zc_tuple][DONOR_NUM] += 1
                    mbz_dict[id_zc_tuple][AMOUNT_LIST].append(int(dfield[TRANSACTION_AMT]))
                # Record every dataset in output file since it may change in one of the next iterations
                with open(outfile1_path, 'a') as ouf1:
                    ouf1.write("%s|%s|%d|%d|%d\n" %(dfield[CMTE_ID], dfield[ZIP_CODE][:5], 
                                                    find_median(mbz_dict[id_zc_tuple][AMOUNT_LIST]), 
                                                    mbz_dict[id_zc_tuple][DONOR_NUM], mbz_dict[id_zc_tuple][TOTAL_CONT]))

            # For valid input parameters, create "medianvals by date" data structure
            if validate_mbd_input(dfield[OTHER_ID], dfield[TRANSACTION_DT], dfield[CMTE_ID], dfield[TRANSACTION_AMT]):
                id_dt_tuple = (dfield[CMTE_ID],dfield[TRANSACTION_DT])
                if id_dt_tuple not in mbd_dict.keys():
                    mbd_dict.update({id_dt_tuple : [[int(dfield[TRANSACTION_AMT])], 1, int(dfield[TRANSACTION_AMT])]})
                else:
                    mbd_dict[id_dt_tuple][TOTAL_CONT] += int(dfield[TRANSACTION_AMT])
                    mbd_dict[id_dt_tuple][DONOR_NUM] += 1
                    mbd_dict[id_dt_tuple][AMOUNT_LIST].append(int(dfield[TRANSACTION_AMT]))

    # Create "medianval by date" output file after entire input file is processed 
    # and by sorting the data structure by keys (tuples of (id,date))
    with open(outfile2_path, 'w') as ouf2:
        for id_dt, val in sorted(mbd_dict.iteritems()):
            ouf2.write("%s|%s|%d|%d|%d\n" %(id_dt[0], id_dt[1], find_median(val[AMOUNT_LIST]), val[DONOR_NUM], val[TOTAL_CONT]))
    
    print "\nSuccessfully created output files \"%s\" and \"%s\"\n" %(outfile1_path, outfile2_path)

# Main function
if __name__ == "__main__":
    '''
    Main function to accept arguments, parse them and send file paths to respective method
    '''
    parser = argparse.ArgumentParser(description="Process donor data in political campaigns")
    parser.add_argument("--input", nargs=1, required=False,
                        help="input file path with pipe-delimited donor data", metavar="<infile_path>",
                        default="./input/itcont.txt")
    parser.add_argument("--output", nargs=2, required=False,
                        help="output files paths, for zipcode-parsed and transaction date-parsed data consecutively", metavar="<outfile_path>",
                        default=["./output/medianvals_by_zip.txt", "./output/medianvals_by_date.txt"])
    args = parser.parse_args()
    try:
        if not os.path.exists(args.input[0]):
            print "Input file not found. Exiting."
        else:
            print "\nParsing input file \"%s\" to generate required output..." %(args.input[0])
            process_donor_data(args.input[0], args.output[0], args.output[1])
    except Exception as e:
        print "Data processing failed due to following error:\n%s\n" %e
