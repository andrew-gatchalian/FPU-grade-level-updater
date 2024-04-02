import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import re
import csv
import pandas as pd
from tkinter import messagebox
import datetime
import sys
import os

# get the path to the directory where PyInstaller extracted the files
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    bundle_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()

# load the logo image
#logo_path = os.path.join(bundle_dir, "logo.png")
#logo = tk.PhotoImage(file=logo_path)

# create a label with the logo
#logo_label = tk.Label(root, image=logo, width=100, height=63)
#logo_label.pack()

#100x50 logo

# set the window title and size
root.title("File Selection")
root.geometry("500x300")

# initialize variables to hold file paths
csv_file_path = ""

def select_file(file_type):
    global csv_file_path
    # open the file dialog to select a file of the specified type
    file_path = filedialog.askopenfilename(
        title=f"Select {file_type.upper()} file",
        filetypes=[(f"{file_type.upper()} Files", f"*.{file_type}"), ("All Files", "*.*")]
    )
    if file_path:
        if file_type == "csv":
            csv_file_path = file_path
            csv_label.config(text=f"Selected {file_type} file: {csv_file_path}")


# create the CSV file selection button
csv_button = tk.Button(root, text="Select Salesforce Data (.csv)", command=lambda: select_file("csv"))
csv_button.pack(pady=10)

# create a label to show the selected CSV file path
csv_label = tk.Label(root, text="")
csv_label.pack(pady=5)

# create the label for the copyright notice
copyright_label = tk.Label(root, text="Copyright © 2023 Andrew Gatchalian", font=("Arial", 8))

# pack the label onto the window
copyright_label.pack(side="bottom", pady=5)



def cannot_award_list(csv_file_path):

    #clean so only essential columns
    df = pd.read_csv(csv_file_path)

    df = df.loc[df["Cannot Award Notes"].str.contains("grade", na=False)]
    df = df.loc[:, ["Colleague ID", "Name", "FAFSA Acad Year", "FAFSA Year in College", "Person: Undergrad Units Complete", "Active Programs"]]

    #fill empty rows with none
    df["Active Programs"] = df["Active Programs"].fillna("No Program")
    
    #split into 3 rows
    df[["Program 1","Program 2"]] = df["Active Programs"].str.split(", ", n=1, expand=True)
    df["Program 2"] = df["Program 2"].fillna("No Program, ")

    df[["Program 2","Program 3"]] = df["Program 2"].str.split(", ", n=1, expand=True)
    df["Program 3"] = df["Program 3"].fillna("No Program")

    #drop active programs
    df = df.drop("Active Programs", axis=1)

    #new dataframe of each seperate program, create highest degree column
    program_df = df[["Program 1", "Program 2", "Program 3"]]
    
    #program_values = pd.read_csv('C:/Users/Andrew.Gatchalian/projects/cal_grant_rosterizer/active program lists/active_programs.csv')
    degree_values = {
        'BA': [0,1,2,3,4],
        'BS': [0,1,2,3,4],
        'UN': [0,1,2,3,4],
        'CD': [5],
        'MS': [6,7],
        'MD': [6,7],
        'MB': [6,7],
        'MA': [6,7],
        'CT': [6,7],
        'No Program': []
    }

    def get_highest_degree(row):
        # Define the degree values lookup table

        # Check if there are any programs
        if pd.isna(row['Program 1']) or row['Program 1'] == 'No Program':
            return "No Program"
        # Check if there is only one program
        elif row['Program 2'] is None and row['Program 3'] is None:
            return row['Program 1']
        # Get the highest value program
        programs = [program for program in [row['Program 1'], row['Program 2'], row['Program 3']] if program is not None]
        highest_value_program = max(programs, key=lambda program: degree_values.get(program[:3], 0))
        return(highest_value_program)

    
    df["Highest Degree"] = program_df.apply(get_highest_degree, axis=1)

    #clean so only highest degree and fafsa year in college
    df = df.drop(["Program 1", "Program 2", "Program 3"], axis=1)

    #New column 'degree level' for all possible degree values
    df['Degree Level'] = df['Highest Degree'].apply(lambda x: degree_values.get(x[:2], []))

    # Make a new column "status" that compares if the value in the column "FAFSA Year in College" is located in the "Degree Level" column for each row.
    # If it is found, return "ok". If not return "update"
    df["Status"] = df.apply(lambda row: "ok" if int(row["FAFSA Year in College"]) in row["Degree Level"] else "update", axis=1)

    def change_grade_level_to(row):
        #undergrad freshman 0-29
        if row["Status"] == "update" and str(row["Degree Level"]) == "[0, 1, 2, 3, 4]" and row["Person: Undergrad Units Complete"] <= 29:
            return "1"
        
        #undergrad sophmore 30-59
        elif row["Status"] == "update" and str(row["Degree Level"]) == "[0, 1, 2, 3, 4]" and row["Person: Undergrad Units Complete"] <= 59 and row["Person: Undergrad Units Complete"] >= 30:
            return "2"

        #undergrad sophmore 60-89
        elif row["Status"] == "update" and str(row["Degree Level"]) == "[0, 1, 2, 3, 4]" and row["Person: Undergrad Units Complete"] <= 89 and row["Person: Undergrad Units Complete"] >= 60:
            return "3"
        
        #undergrad sophmore 90+
        elif row["Status"] == "update" and str(row["Degree Level"]) == "[0, 1, 2, 3, 4]" and row["Person: Undergrad Units Complete"] >= 90:
            return "4"

        #teaching cred 5
        elif row["Status"] == "update" and str(row["Degree Level"]) == "[5]":
            return "5"
        
        #grad 6
        elif row["Status"] == "update" and str(row["Degree Level"]) == "[6, 7]" and row["Person: Undergrad Units Complete"] <= 149:
            return "6"
        
        #grad 7
        elif row["Status"] == "update" and str(row["Degree Level"]) == "[6, 7]" and row["Person: Undergrad Units Complete"] >= 150:
            return "7"
        
        elif row["Status"] == "update" and str(row["Degree Level"]) == "[]":
            return "N/A"
        
        else: 
            return "New Grade Level Correct"

    df["Change Grade Level To:"] = df.apply(change_grade_level_to, axis=1)

    #sort by grade levels
    df = df.sort_values(by=['Change Grade Level To:'])
    
    #drop columns so only important stuff
    df = df.drop(["Degree Level", "Status"], axis=1)

    #rename for cleaner view
    df = df.rename(columns={'FAFSA Year in College': 'Current Grade Level'})

    print(df)

    # Get current date and time MM-DD-YY
    now = datetime.datetime.now()
    filename = now.strftime("%Y%m%d") + "_cannot_award_update.csv"

    # Allow user to select file path
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                initialfile=filename,
                                                filetypes=[("CSV Files", "*.csv")])
    if not file_path:  # user cancelled the dialog
        return
    
    df.to_csv(file_path, index=False)

def run_script():
    # check if both files have been selected
    if csv_file_path:
        # run the function return_ssn
        cannot_award_list(csv_file_path)
        root.update_idletasks()
        # run the function merge
        print("Scripts completed successfully.")
        # show message box when root is destroyed
        messagebox.showinfo("Complete", "Scripts completed successfully.")
        #Close

    else:
        print("Please select file before running the scripts.")

# create the run scripts button
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.pack(pady=10)

root.mainloop()