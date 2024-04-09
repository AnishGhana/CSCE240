import csv  # importing csv library
import os  # importing os library
import re  # importing re library
from pathlib import Path  # import Path to get current file path
import sys  # to use command line arguments

###################### prints the summary of a single chat session ######################


def chatSummary(n):
    count = 0  # creates a variable named count and sets it to 0

    with open("../data/chat_statistics.csv", 'r', newline='\n') as csvFile:  # opens the csv file
        csvReader = csv.reader(csvFile)  # creates a csv file reader
        for line in csvReader:  # loops through each line in the csv
            count += 1  # incremets count by 1
            if (line[0] == n):  # checks to see if the session number in the csv file and compares it to the input value
                # prints the statement below
                print("Chat "+n+" has user asking " +
                      line[2]+" times and system respond "+line[3]+" times. Total duration is "+line[4]+" seconds.")

    if (int(n) >= count):  # checks to see if the value of input value is greater than or equal to the value of count
        # prints the statement below
        print("Error. There are only "+str(count) +
              " sessions. Please choose a valid number. The session numbers go from 0 to "+str(count-1)+".")

    csvFile.close()  # closes the file


###################### prints the entire chat to the terminal ######################
def showchat(n):
    fileName = ""  # creates a fileName variable
    count = 0  # creates a variable named count and sets it to 0

    with open("../data/chat_statistics.csv", 'r', newline='\n') as csvFile:  # opens the csv file
        csvReader = csv.reader(csvFile)  # creates a csv file reader
        for line in csvReader:  # goes through each line in the csv
            if (line[0] == n):  # checks to see if the session number in the csv file and compares it to the input value
                # sets the fileName variable to the chat file variable in the csv file
                fileName = line[1]
            count += 1  # increments count by one
    csvFile.close()  # closes the file

    if (int(n) >= count):  # checks to see if the input value is greater than or equal to the value of count
        # prints the statement below
        print("Error. There are only "+str(count) +
              " sessions. Please choose a valid number. The session numbers go from 0 to "+str(count-1)+".")
        return  # returns so that the rest of the program does not run

    print("Chat "+n+" chat is:")  # prints this statement
    # opens a file reader for the correct chat session file
    with open("../data/chat_sessions/"+fileName) as f:
        for line in f:  # iterates through the file
            print(line)  # prints the line

    f.close()  # closes file reader


###################### creates the csv file with the chat session files ######################
def initCSV():
    sessionFileList = []  # creates an empty list

    # creates the following 4 variables and sets them equal to 0
    totalNum = 0
    totalUserUtt = 0
    totalSysUtt = 0
    totalTime = 0

    # Checking the existance of session log files.
    # If the session log files are not present throw error message and exit the program
    if len(os.listdir('../data/chat_sessions')) <= 0:
        print("ERROR: Session log files are missing. Please add session log files to data/chat_sessions folder")
        quit()

    # iterates through all the files in the chat_sessions folder
    for path in os.listdir('../data/chat_sessions'):
        sessionFileList.append(path)  # adds the file to the empty list

    # opens a filewriter for the csv writer
    with open("../data/chat_statistics.csv", 'w') as csvfile:
        # creates a csv writer using the csv library
        writer = csv.writer(csvfile)
        sessionNum = 0  # creates a variable called sessionNum and sets it to 0

        for chatfile in sessionFileList:  # iterates through the session file list
            totalNum += 1  # increases the totalNum variable by 1
            userUtt = 0  # creates a userUtt variable and sets it to 0
            sysUtt = 0  # creates a sysUtt variable and sets it to 0
            time = 0  # creates a time variable and sets it to 0

            # opens a file reader for the current file
            with open("../data/chat_sessions/" + chatfile, "r") as f:
                # iterates through each line in the file
                for line_i, line in enumerate(f, 1):
                    # creates a regex for the bot utterances
                    bot = re.compile("<ChatBot> :")
                    # creates a regex for the user utterances
                    user = re.compile("<User> :")

                    if (bot.search(line)):  # checks to see if the bot regex is in the line
                        sysUtt += 1  # increments the sysUtt by 1
                        totalSysUtt += 1  # increments the totalSysUtt by 1

                    elif (user.search(line)):  # checks to see if the user regex is in the line
                        userUtt += 1  # increments the userUtt by 1
                        totalUserUtt += 1  # increments the totalUserUtt by 1

                    # checks to see if the word seconds is in the line
                    elif (line.find("seconds") != -1):
                        # finds the index of the word seconds
                        end = line.find(" seconds")
                        # sets time equal to the correct substring of the line
                        time = line[18:end]
                        # increments the totalTime by time
                        totalTime += float(time)

            # writes a row into the csv file
            writer.writerow([sessionNum, chatfile, userUtt, sysUtt, time])

            sessionNum += 1  # increments the sessionNum by 1

    csvfile.close()  # closes the filewriter

    # creates a list of four variable and returns it
    return [totalNum, totalUserUtt, totalSysUtt, totalTime]


########################### Get Session summary details #######################
def getSessionSummary(choice, isFromCommandLine):
    choice = choice.upper()  # makes the input all uppercase

    if (checkFullSummary.search(choice)):  # checks to see if the checkFullSummary matches the input
        print("There are "+str(fullStat[0])+" chats to date with user asking "+str(fullStat[1]) +
              " times and system respond "+str(fullStat[2])+" times. Total duration is "+str(fullStat[3])+" seconds.")

    elif (checkChatSummary.search(choice)):  # checks to see if the checkChatSummary matches the input
        session = choice[17:len(choice)]  # finds out the number from the input
        chatSummary(session)  # calls the summary function

    elif (checkChat.search(choice)):  # checks to see if the checkChat matches the input
        session = choice[9:len(choice)]  # finds out the number from the input
        showchat(session)  # calls the showchat function

    elif (checkQuit.search(choice)):  # checks to see if the checkQuit matches the input
        return False  # breaks the loop

    else:
        # prints this statement if none of the regex match
        print("Please only enter one of the 4 options.")
        if isFromCommandLine:
            print(strMessage)

    return True


###################### Main Program ######################
file_path = Path(__file__)  # get current file path

# Change the current working directory to the directory name of the current Python file
os.chdir(file_path.parent)

fullStat = initCSV()  # calls the initCSV() function and sets the return value to fullStat

checkFullSummary = re.compile("^SUMMARY$")  # creates a checkFS regex
checkChatSummary = re.compile(
    "^SHOWCHAT-SUMMARY\s[0-9]+$")  # creates a checkOS regex
checkChat = re.compile("^SHOWCHAT\s[0-9]+$")  # creates a checkOC regex
checkQuit = re.compile("^QUIT$")  # creates a checkQ regex

# Message that comes up when executes with no command line arguments or when user enters invalid argument
strMessage = "\n1. Type \"summary\" for the summary of all the sessions. \n2. Type \"showchat-summary <number>\" to find the summary of a singular session. \n3. Type \"showchat <number>\" to see the full chat from a session. \n4. Type \"quit\" to end the program."

print("\nWelcome to the Session Logger!")  # prints a welcome statement

if len(sys.argv) > 1:  # if the user executes from command line providing command line arguments
    # join all command line arguments as one string
    choice = ' '.join(sys.argv[1:])

    # remove "-" from command line argument
    while choice.startswith("-"):
        choice = choice[len("-"):]

    # Execute session commands
    getSessionSummary(choice, True)
else:
    # if the user executes without providing command line arguments then loop infinite
    while True:
        # prompts the user
        print(strMessage)
        choice = input()

        if not getSessionSummary(choice, False):
            break
