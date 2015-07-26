from datetime import datetime
import sys
import csv

def fill_column(survey_file, col_file):
    with open(survey_file, 'rb') as f:
        reader = csv.reader(f)
        surveys = list(reader)

    with open(col_file, 'rb') as f:
        reader = csv.reader(f)
        grade_center = list(reader)

    #removes extra quotes that BOM adds...
    grade_center[0][0] = 'Last Name'

    #some constants that might be changed for future usage
    #export only 1 column from TED so the TED_PID and SCORE idxs stay same
    TIME_IDX = 0
    RES_PID_IDX = 45
    TED_PID_IDX = 3
    SCORE_IDX = 6
    SUCCESS_SCORE = "1"
    FAIL_SCORE = "0"
    DEADLINE = "5/5/2015 17:15:00"

    #gather PIDs of people who submitted on time
    valid = set()
    deadline = datetime.strptime(DEADLINE, "%m/%d/%Y %H:%M:%S")
    for user in surveys[1:]:
        time = datetime.strptime(user[TIME_IDX], "%m/%d/%Y %H:%M:%S")
        if time <= deadline:
            valid.add(user[RES_PID_IDX])

    for pid in valid:
        upper_pid = pid.upper()
        valid.remove(pid)
        valid.add(upper_pid)

    #give them a score in grade center
    for student in grade_center[1:]:
        if student[TED_PID_IDX].upper() in valid:
            student[SCORE_IDX] = SUCCESS_SCORE
        else:
            student[SCORE_IDX] = FAIL_SCORE

    #write to file and upload to TED
    with open(col_file, 'w') as csvfile:
        writer = csv.writer(csvfile, quotechar="\"",  \
                quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        writer.writerows(grade_center)

if __name__ == "__main__":
    fill_column(sys.argv[1], sys.argv[2])
