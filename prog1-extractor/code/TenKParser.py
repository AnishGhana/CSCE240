import os


def parse_text_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return 0, 0, 0, 0  # Return zero values for statistics

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.count('\n') + 1  # Count lines
    words = len(content.split())  # Count words
    chars = len(content)  # Count characters

    # Count fully capitalized instances of "PART" without an empty line before them
    parts = 0
    content_lines = content.split('\n')

    for idx, line in enumerate(content_lines):
        if "PART" in line and (idx == 0 or content_lines[idx - 1].strip() == ""):
            parts += 1

    return lines, words, chars, parts


def format_and_write_output(company_name, statistics):
    output_directory = os.path.join("prog1-extractor", "data", "output")
    # Create 'data/output' directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    output_file = os.path.join(output_directory, f"{company_name}-2022.txt")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"Company: {company_name}\n")
        file.write("Statistics:\n")
        file.write(f"  Lines: {statistics[0]}\n")
        file.write(f"  Words: {statistics[1]}\n")
        file.write(f"  Characters: {statistics[2]}\n")
        file.write(f"  Number of Parts: {statistics[3]}\n")


def main():
    while True:
        choice = input(
            "Enter 1 to analyze Exxon Mobil's 10-K, 2 to analyze Berkshire Hathaway's 10-K, or 3 to quit: ")

        if choice == "1":
            company_name = "Exxon Mobil"
            file_path = "./prog1-extractor/test/ExxonMobil.txt"
        elif choice == "2":
            company_name = "Berkshire Hathaway"
            file_path = "./prog1-extractor/test/BerkshireHathaway.txt"
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        # Parse and analyze the selected text file
        statistics = parse_text_file(file_path)

        # Format and write output to a file
        format_and_write_output(company_name, statistics)

        print(f"Analysis for {company_name} has been saved to the file.")


if __name__ == "__main__":
    main()
