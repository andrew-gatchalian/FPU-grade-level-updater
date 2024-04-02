# Grade Level Updater
This Python application is designed to streamline data processing tasks by providing a user-friendly interface for selecting files and executing scripts on the selected data. Utilizing the Tkinter library for its GUI components, the application allows users to choose CSV files from their filesystem and perform specific data processing functions on them. The primary focus of this application is on processing Salesforce data exported as CSV files, with specific operations to filter, modify, and export this data based on predefined criteria.

#### Features:
- **File Selection Interface:** Users can select CSV files through a simple dialog interface, which then displays the path of the selected file within the application window.
- **Data Processing:** Once a file is selected, the application processes the CSV file to identify records that match specific criteria (e.g., containing specific notes about award eligibility) and then performs further data manipulation. This includes:
  - Cleaning data to retain only essential columns.
  - Separating and analyzing text in columns to derive additional insights.
  - Dynamically adjusting data based on custom logic related to academic information and program enrolment.
  - Exporting the processed data to a new CSV file, with the option for the user to specify the save location and filename.
- **Flexible Data Handling:** The application handles various data formats and scenarios, including missing data and specific data structure requirements. It utilizes Pandas for data manipulation, ensuring efficient and accurate processing.
- **Customizable Output:** Users can specify the output filename and save location, with the application automatically suggesting a filename based on the current date.

#### How It Works:
1. **Starting the Application:** The GUI initializes with options to select a CSV file and run the processing script.
2. **Selecting a File:** Users click the "Select Salesforce Data (.csv)" button to open a file dialog and choose a file, which updates the interface to show the selected file path.
3. **Processing Data:** By clicking the "Run Script" button, the application processes the selected file based on the logic defined in the `cannot_award_list` function. This includes cleaning the data, splitting text fields, calculating and comparing values, and ultimately generating a new CSV file that highlights specific changes or conditions in the data.
4. **Exporting Results:** After processing, the application prompts the user to save the resulting CSV file, applying modifications and filters as per the script's logic.

#### Requirements:
- Python 3.x
- Tkinter (for the GUI components)
- Pandas (for data manipulation)
- Additional Python standard libraries: `re`, `csv`, `datetime`, `sys`, `os`

This application is ideal for users looking for an efficient way to select, process, and analyze CSV files, particularly in scenarios requiring specific data manipulation tasks related to educational or academic data.
