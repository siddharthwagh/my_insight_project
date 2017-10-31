-------------------------
PROJECT CHALLENGE SUMMARY
-------------------------
The challenge summary for project can be found at:
https://github.com/InsightDataScience/find-political-donors


-----------------------------
PROJECT DESIGN CONSIDERATIONS
-----------------------------
1. Data structure to hold data for "Medianvals_By_Zip" output file:
{
    (<cmte_id1>, <zip_code1>) : [[<transaction_amount11>, <transaction_amount12>, ...], <donor_number1>, <total_contribution1>],
    (<cmte_id2>, <zip_code2>) : [[<transaction_amount21>, <transaction_amount22>, ...], <donor_number2>, <total_contribution2>],
    ...
}

2. Data structure to hold data for "Medianvals_By_Date" output file:
{
    (<cmte_id1>, <transaction_date1>) : [[<transaction_amount11>, <transaction_amount12>, ...], <donor_number1>, <total_contribution1>],
    (<cmte_id2>, <transaction_date2>) : [[<transaction_amount21>, <transaction_amount22>, ...], <donor_number2>, <total_contribution2>],
    ...
}

3. Output file 1 is written dynamically for every valid input line (validated using validate() functions)

4. Output file 2 is written after the entire input file is processed, so that resulting data can be sorted according to tuple-key pairs.
   (sorted) method from Python would sort according to CMTE_ID first, and then as per TRANSACTION_DATE.

5. Transaction amount list is not pre-sorted in case the amount data is required as per its order in political data input file.

6. Median value is calculated each time an entry is made in the output file.
   For odd number of values in amount list, central value is median
   For even number of values in amount list, average of central two values is taken and ceiled if result is xx.50


-------------------------------
HOW TO RUN SCRIPT INDEPENDENTLY
-------------------------------

usage: find_political_donors.py [-h] [--input <infile_path>]
                                [--output <outfile_path> <outfile_path>]

Process donor data in political campaigns

optional arguments:
  -h, --help            show this help message and exit
  --input <infile_path>
                        input file path with pipe-delimited donor data
  --output <outfile_path> <outfile_path>
                        output files paths, for zipcode-parsed and transaction
                        date-parsed data consecutively

-------
CONTACT 
-------
Regarding questions about the project, please contact swagh [at] cac [dot] rutgers [dot] edu
# my_insight_project
