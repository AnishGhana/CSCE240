import re
from pathlib import Path
import os
from difflib import SequenceMatcher
import time  # this is for formatting session file with date and time
import datetime  # this for finding date time difference during session


# Set Max match ratio threshold
max_match_threshold = 0.7

# Define the regex patterns for matching company names
berkshire_pattern = re.compile(r'.*berkshire\s*hathaway.*', re.IGNORECASE)
exxon_pattern = re.compile(r'.*exxon\s*mobil.*', re.IGNORECASE)

# The dictionay has section names and corresponding array that has start and end index
sections = {
    "Business Description": ["Item\s1\.\s", "Item\s1A\.\s"],
    "Risk Factors": ["Item\s1A\.\s", "Item\s1B\.\s"],
    "Risks": ["Item\s1A\.\s", "Item\s1B\.\s"],
    "Unresolved Staff Comments": ["Item\s1B\.\s", "Item\s2\.\s"],
    "Properties Description": ["Item\s2\.\s", "Item\s3\.\s"],
    "Legal Proceedings": ["Item\s3\.\s", "Item\s4\.\s"],
    "Mine Safety Disclosures": ["Item\s4\.\s", "Item\s5\.\s"],
    "financial data": ["Item\s5\.\s", "Item\s7\.\s"],
    "financial report": ["Item\s5\.\s", "Item\s7\.\s"],
    "revenue details": ["Item\s5\.\s", "Item\s7\.\s"],
    "Market for Registrant's Common Equity, Related Security Holder Matters and Issuer Purchases Equity Securities": ["Item\s5\.\s", "Item\s7\.\s"],
    "Management Discussion and Analysis Financial Condition and Results Operations": ["Item\s7\.\s", "Item\s7A\.\s"],
    "Quantitative and Qualitative Disclosures About Market Risk": ["Item\s7A\.\s", "Item\s8\.\s"],
    "Financial Statements and Supplementary Data": ["Item\s8\.\s", "Item\s9\.\s"],
    "Changes in and Disagreements with Accountants on Accounting and Financial Disclosure": ["Item\s9\.\s", "Item\s9A\.\s"],
    "Controls and Procedures": ["Item\s9A\.\s", "Item\s9B\.\s"],
    "Other Information": ["Item\s9B\.\s", "Item\s10\.\s"],
    "Directors, Executive Officers and Corporate Governance": ["Item\s10\.\s", "Item\s11\.\s"],
    "CEO": ["Item\s10\.\s", "Item\s11\.\s"],
    "Executive Compensation": ["Item\s11\.\s", "Item\s12\.\s"],
    "Executive Salary": ["Item\s11\.\s", "Item\s12\.\s"],
    "Security Ownership Certain Beneficial Owners and Management and Related Stockholder Matters": ["Item\s12\.\s", "Item\s13\.\s"],
    "Certain Relationships and Related Transactions, and Director Independence": ["Item\s13\.\s", "Item\s14\.\s"],
    "Principal Accountant Fees and Services": ["Item\s14\.\s", "Item\s15\.\s"],
    "Exhibits and Financial Statement Schedules": ["Item\s15\.\s", "Item\s16\.\s"],
    "Statement": ["Item\s15\.\s", "Item\s16\.\s"],
    "All Information": ["Table\sof\sContents", "SIGNATURES"]
}

# session log file name
sessionFileName = "session_" + time.strftime("%Y%m%d-%H%M%S")

########################## logging chatbot and user conversations #########################


def logSessionMessage(strMessage):
    print("\n" + strMessage)

    # opens the file writer and write session log
    g = open("../data/" + sessionFileName + ".txt", "a", encoding='utf-8')
    g.write("\n" + strMessage)
    g.close()


######################### Function to calculate Max match ratio in understanding user's query #########################
def get_max_match_ratio(user_input):

    max_match_ratio = 0
    best_query = None

    # loop through sections
    for section in sections:

        # find match ratio
        match_ratio = SequenceMatcher(
            None, user_input.lower(), section.lower()).ratio()

        # if match ration is greate that max match ratio then set the new match_ratio as max
        if match_ratio > max_match_ratio:
            max_match_ratio = match_ratio
            best_query = section

    return max_match_ratio, best_query


######################### Function to determine the supported company from user input and return company fine #########################
def get_companyFile(user_input):
    if berkshire_pattern.search(user_input):
        return "../data/BerkshireHathaway.txt"  # Assign company_file
    elif exxon_pattern.search(user_input):
        return "../data/ExxonMobil.txt"  # Assign company_file
    else:
        return None


######################### Function that writes the output to file #########################
def print_to_file(company_file, start, end):
    # This initalizes the regular expression for the start
    regexStart = re.compile(start)
    # This initalizes the regular expression for the end
    regexEnd = re.compile(end)
    # With isWithin we create a boolean value to determine whether the file reader is in between the beginning and end
    isWithin = False

    logSessionMessage(
        "<ChatBot> : Answer found and the answer is directed to output.txt file in data folder.")

    f = open(company_file, "r", encoding='utf-8')  # opens the file reader
    # opens the file writer
    g = open("../data/output.txt", "w", encoding='utf-8')

    for line in f:
        # checking the line to see if the start regex is contained within it
        if regexStart.search(line):
            isWithin = True  # Does the switch so lines can be printed to output file
        # checking the line to see if the end regex is contained within it
        if regexEnd.search(line):
            isWithin = False  # This switches the boolean value to be false
        if (isWithin):  # This checks the boolean value to make sure that the file reader is between the beginning and end
            g.write(line)  # This prints the line to the output file

    f.close()  # Here we close the file reader
    g.close()  # Here we close the file writer


######################### parses user input, gets related company file, gets match ratio #########################
######################### and prints the appropriate content to output file ######################################
def parse_user_input(user_input):

    # Function to parse user input and determine related section
    companyFile = get_companyFile(user_input)

    # check if company file is not none
    if not companyFile:
        logSessionMessage(
            "<ChatBot> : Company not supported. Please mention Berkshire Hathaway or Exxon Mobil.")
        return None  # Return None if company is not supported

    # checking for file existance
    if not os.path.exists(companyFile):
        logSessionMessage("<ChatBot> : Company File " + companyFile +
                          " does not exists in the current folder.")
        return None

    user_input = removeFillerWords(user_input)

    # get max match ratio
    max_match_ratio, best_query = get_max_match_ratio(user_input)
    if max_match_ratio < max_match_threshold:
        logSessionMessage(
            "<ChatBot> : Match Ratio is below threshold. Please rephrase your query.")
        return None  # Return None if max match ratio is below threshold

    logSessionMessage(f"<ChatBot> : Maximum match Ratio: {max_match_ratio}")
    logSessionMessage(f"<ChatBot> : Best Query: {best_query}")

    # Check for section names related to the company
    for section in sections:
        if best_query.upper().find(section.upper()) != -1:
            # values for sections dictionary contains array that has start and end point
            print_to_file(
                companyFile, sections[section][0], sections[section][1])

            break


######################### This function removes common words to help with the string matching #########################
def removeFillerWords(user_input):

    # Add all words that need to be removed from user input to an array
    words_to_remove = ["?", ".", "provide", "show", "what", "who", "the", "is", "of", "are", "for", "about",
                       "item", "tell", "me", "give", "a", "berkshire", "hathaway", "exxon", "mobil"]

    # get all words that doesn't have removed words
    resultwords = [word for word in re.split(
        "\W+", user_input) if word.lower() not in words_to_remove]

    # join words together
    ret = ' '.join(resultwords)

    # return joined words
    return ret


######################### Main Program #########################
file_path = Path(__file__)  # get current file path

# Change the current working directory to the directory name of the current Python file
os.chdir(file_path.parent)

# getting session begin time
sessionBeginTime = datetime.datetime.now()

# logging all session messages
logSessionMessage("<ChatBot> : Welcome!")

# Main loop
while True:
    logSessionMessage(
        "<ChatBot> : Please enter a question about Berkshire Hathaway or Exxon Mobil, or enter Quit, quit or q: ")
    user_input = input()

    if user_input.upper() == "QUIT" or user_input.upper() == "Q":
        logSessionMessage("<ChatBot> : Thank you. Bye!")

        sessionEndTime = datetime.datetime.now()
        sessionTime = sessionEndTime - sessionBeginTime
        logSessionMessage("This program took " +
                          str(sessionTime.total_seconds()) + " seconds")

        break

    # logging all user chat
    logSessionMessage("<User> : " + user_input)

    parse_user_input(user_input)
