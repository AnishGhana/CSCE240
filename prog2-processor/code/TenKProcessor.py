import re
fileName = ""
exit = False
# used to keep the program running


def print_to_file(start, end):
    # This initalizes the regular expression for the start
    regexStart = re.compile(start)
    # This initalizes the regular expression for the end
    regexEnd = re.compile(end)
    # With isWithin we create a boolean value to determine whether the file reader is in between the beginning and end
    isWithin = False
    with open(fileName, "r", encoding='utf-8') as f:  # opens the file reader
        with open("./prog2-processor/data/output.txt", "w", encoding='utf-8') as g:  # opens the file writer
            for line_i, line in enumerate(f, 1):
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


def parse_user_input(user_input):
    # Define the regex patterns for matching company names
    berkshire_pattern = re.compile(r'berkshire\s*hathaway', re.IGNORECASE)
    exxon_pattern = re.compile(r'exxon\s*mobil', re.IGNORECASE)

    # Check if the input matches either company
    if berkshire_pattern.search(user_input):
        company_name = "Berkshire Hathaway"
        return "./prog2-processor/data/BerkshireHathaway.txt"
        # A Berkshire Hathaway 10-K that is just like the first project
    elif exxon_pattern.search(user_input):
        company_name = "Exxon Mobil"
        return "./prog2-processor/data/ExxonMobil.txt"
        # A Exxon Mobil 10-K that is just like the first project
    else:
        print("Company not recognized.")
        # If neither company is inputed by the user
        return


def search(user_input):
    # The section names for each of the parts of the company's 10-K
    sections = ["Business Description", "Risk Factors", "Unresolved Staff Comments", "Description of Properties",
                "Legal Proceedings", "Mine Safety Disclosures",
                "Market for Registrant's Common Equity, Related Security Holder Matters and Issuer Purchases of Equity Securities",
                "Management’s Discussion and Analysis of Financial Condition and Results of Operations",
                "Quantitative and Qualitative Disclosures About Market Risk", "Financial Statements and Supplementary Data",
                "Changes in and Disagreements with Accountants on Accounting and Financial Disclosure", "Controls and Procedures",
                "Other Information", "Exhibits and Financial Statement Schedules", "All Information"]

    # The corresponding item number (except for the last one) for each section
    regex = ["Item\s1\.\s", "Item\s1A\.\s", "Item\s1B\.\s", "Item\s2\.\s",
             "Item\s3\.\s", "Item\s4\.\s", "Item\s5\.\s", "Item\s7\.\s",
             "Item\s7A\.\s", "Item\s8\.\s", "Item\s9\.\s", "Item\s9A\.\s",
             "Item\s9B\.\s",  "Item\s15\.\s", "Table\sof\sContents"]

    # Check for section names related to Exxon Mobil
    for section in sections:
        if (user_input.upper().find(section.upper()) != -1):
            # Use a case-insensitive regex to match the section name regardless of case
            startIndex = sections.index(section)
            # How to get "all information"
            if (regex[startIndex] == "Table\sof\sContents"):
                print_to_file(regex[startIndex], "SIGNATURES")
                break
            else:
                print_to_file(regex[startIndex], regex[startIndex+1])
                break


while (not exit):
    # prompt to enter question about Berkshire Hathaway or Exxon Mobil
    user_input = input(
        "Please enter a question that you have about Berkshire Hathaway or Exxon Mobil, or enter 1 to exit the program.")
    # If the user inputs the number "1", then the program is ended
    if (user_input == "1"):
        exit = True
        break
# Example use:
    fileName = parse_user_input(user_input)
    search(user_input)
