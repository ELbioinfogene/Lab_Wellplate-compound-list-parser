'''Well Screen Population Builder v3
Eric Larsen
Albrecht Lab 2021
~+~
Input is a TSV table of all drugs applied to a well plate
Each unique compound name gets an integer ID (population #)
Two output variables are saved as CSVs to be read by another software:
POPULATION_IDs > NAME_LIST.csv
    - has each compound name and its associated population #
POPULATION_MAP > POP_MAP.csv
    - population #s as physically assigned on the well plate
WORKING 9/23/21
'''
#Dependencies
import csv

#Import TSV file
'''input format:
well, drugname, numRow, numCol, intensity, drug(?), animals(?)
This convention is 24 'rows' (1 thru 24) and 17 'Columns' (A thru P)
'''
#should be in same folder as this .py
#\/ MANUALLY DEFINE FILE(S) HERE \/
INPUT_1 = 'DEMO_PLATE_DATA.tsv'
INPUT_FILE = open(INPUT_1)

#PROCESS FILE
RAW_INPUT = csv.reader(INPUT_FILE,delimiter='\t',lineterminator='\n')
RAW_LIST = list(RAW_INPUT)
INPUT_FILE.close()
#GET HEADER
ENTRY_TITLES = RAW_LIST[0]
#Data without header
DATA_LIST = RAW_LIST[1::]
#Number of wells
WELL_COUNT = len(DATA_LIST)

#create dictionary of compounds
POPULATION_IDs = {}

#Eric's 384 wellplate convention: 17 'rows' (A thru P) and 24 'Columns' (1 thru 24)
#Build array of 0's for population map
HIGHEST_WELL_COL = int(DATA_LIST[WELL_COUNT-1][2])
HIGHEST_WELL_ROW = int(DATA_LIST[WELL_COUNT-1][3])
POPULATION_MAP = [[0 for COLUMN in range(HIGHEST_WELL_COL)] for ROW in range(HIGHEST_WELL_ROW)]
#FOR DEBUG ONLY - confirmed good 9/23
PHYSICAL_MAP = [[0 for COLUMN in range(HIGHEST_WELL_COL)] for ROW in range(HIGHEST_WELL_ROW)]

#count compounds
population_N = 0
#loop through all TSV entries
for N in range(WELL_COUNT):
    #build dictionary of compound names and population #s
    COMPOUND_ADDRESS = DATA_LIST[N][0]
    COMPOUND_NAME = DATA_LIST[N][1]
    COMPOUND_COL = int(DATA_LIST[N][2])
    COMPOUND_ROW = int(DATA_LIST[N][3])
    '''#DEBUG - DISPLAY EVERY 25th value
    if N%25 == 0:
        print(f'{COMPOUND_NAME} in well {COMPOUND_ADDRESS}')
    #END DEBUG SEQUENCE - WORKS 9/22/21'''
    #Compound is already in dictionary
    try:
        POPULATION_TAG = POPULATION_IDs[COMPOUND_NAME]
    #NEW ENTRY - add to dictionary
    except KeyError:
        population_N = population_N + 1
        POPULATION_IDs[COMPOUND_NAME] = population_N
        POPULATION_TAG = population_N
    
    #assign population # on wellplate array
    POPULATION_MAP[COMPOUND_ROW-1][COMPOUND_COL-1] = POPULATION_TAG
    #FOR DEBUG- Confirm A01 thru P24 result vs POPULATION_MAP result
    PHYSICAL_MAP[COMPOUND_ROW-1][COMPOUND_COL-1] = COMPOUND_ADDRESS
#END OF TSV ENTRY LOOP

print(f'''
        File read complete!
        {population_N} compounds identified
        Preparing for CSV output...''')
#WORKING 9/22/21
#population_N is all the populations detected
#POPULATION_IDs is a dictionary of compounds and the ID#
#POPULATION_MAP is an array of physical locations of ID#
#FOR DEBUG: PHYSICAL_MAP is an array of physcial locations of well address strings

#list of compound name strings
COMPOUND_NAME_LIST = list(POPULATION_IDs)
#Output Compound Name List as a CSV
#\/ MANUALLY SET FILE OUTPUT HERE \/
LISTOUT = open('PLATE_DEMO_NAME_LIST.csv','w',newline='')
LISTWRITER = csv.writer(LISTOUT)
for N in range(population_N):
    compound = COMPOUND_NAME_LIST[N]
    LISTWRITER.writerow([f'{N+1}',f'{compound}'])
LISTOUT.close()
print('Name List CSV generated')
#this works 9/22/21 - adapted from v1

#Output Population Map as CSV
#Uncomment Debug Sections to output a CSV of Well Addresses
#IE A01 thru P24 as they would be on the plate
#\/ MANUALLY SET FILE OUTPUT HERE \/
MAPOUT = open('PLATE_DEMO_POP_MAP.csv','w',newline='')
MAPWRITER = csv.writer(MAPOUT)
'''#DEBUG:
PHYSICAL_OUT = open('PLATE_DEMO_WELL_MAP.csv','w',newline='')
WELLWRITER = csv.writer(PHYSICAL_OUT)
#END DEBUG'''
#Build rows for CSV write
for ROW in range(HIGHEST_WELL_ROW):
    DATA_ROW = POPULATION_MAP[ROW]
    MAPWRITER.writerow(DATA_ROW)
    '''#DEBUG:
    WELL_ROW = PHYSICAL_MAP[ROW]
    WELLWRITER.writerow(WELL_ROW)
    #END DEBUG'''
MAPOUT.close()
print('Population Map CSV generated')
'''#DEBUG:
PHYSICAL_OUT.close()
print('Well Name Map CSV generated')
#END DEBUG'''
#9/22/21 - adapted from v1
#not quite right - doesn't map to physical plate
#9/23 - FIXED - confusion of row/col nomenclature from TSV file
