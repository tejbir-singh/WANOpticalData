import matplotlib.pyplot as plt
import os
import glob
import datetime
import re
import subprocess

def calculateAverageQFactorForDay(date, qfac_lst):
    return None

# remember that strings in python are immutable (can't be changed)
# https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
# In Python 3, strings are unicode.
def getDateFromString(date_string):
    translation_table = dict.fromkeys(map(ord, '-'), None)
    date_string = date_string.translate(translation_table)
    date_obj = datetime.datetime.strptime(date_string.strip(), "%Y%m%d" ).date()
    return date_obj


def getFileDateRange(fname):
    with open(fname) as file:
        file_name = file.name
        file_size = os.stat(fname).st_size
        first_line = file.readline()
        last_line = file.readlines()[-1]
        first_line_split = [x.strip() for x in first_line.split(',')]
        last_line_split = [x.strip() for x in last_line.split(',')]
        (dateString_lowerBound, dateString_upperBound) = (first_line_split[0][1:11], last_line_split[0][1:11])
        return (file_name, dateString_lowerBound, dateString_upperBound)


def writeFile_date_AveQFactor(fileName, dateQFactor_dict):
    return None




def main():
# loop over all the files containing our interval time window and Q-factors for each channel
    for filename in glob.glob('*.txt'):
        (fname, lowerBoundDate, upperBoundDate) = getFileDateRange(filename)
        #print(fname, fsize, firstLine, lastLine)
        with open(filename, 'r') as f:  # open the file and iterate over each line
            first_line = f.readline()
            firstLine_split = [x.strip() for x in first_line.split(',')]  # split the line based on the delimiter
            (date, q_fac) = (firstLine_split[0][1:11], firstLine_split[1])
            begin_date = getDateFromString(date)
            # create a dictionary, {"Date", [Q-factor list]}
            date_qFactorLstDict = {}
            q_factorLst = list()
            q_factorLst.append(float(q_fac))
            # date_qFactorLstDict[begin_date.strftime('%Y-%m-%d')] = q_factorLst
            # print(date_qFactorLstDict)
            # last_line = subprocess.check_output(['tail', '-1', filename]) # this code is prepending an unwanted char at the beginning
            #last_line = f.readlines()[-1]
            #print(last_line)
            for line in f:
                line_split = [x.strip() for x in line.split(',')]  # split the line based on the delimiter
                # print(line_split) # ['"2015-03-19 22:30:00"', '14.71']
                (date, q_fac) = (line_split[0][1:11], line_split[1]) # list of [Date-time, Q-factor]
                date_nextLine = getDateFromString(date)
                #print(begin_date)
                #print(date_nextLine)
                if (begin_date == date_nextLine ):
                    q_factorLst.append(float(q_fac))
                else:  # date_nextLine is now 03-19
                    date_qFactorLstDict[begin_date.strftime('%Y-%m-%d')] = q_factorLst
                    del q_factorLst  # empty the contents of the list
                    begin_date = date_nextLine # begin_date now becomes 03-20
                    q_factorLst = list()
                    q_factorLst.append(float(q_fac)) # we need to append the q-factor value of line already read in
                    #print(date_nextLine)
                    #print(begin_date)
                    print(date_qFactorLstDict)
            else:
                date_qFactorLstDict[begin_date.strftime('%Y-%m-%d')] = q_factorLst
                del q_factorLst
                print(date_qFactorLstDict)
                # write the dictionary to a file
        #print(date_qFactorLstDict)


main()