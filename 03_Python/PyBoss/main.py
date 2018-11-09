import os
import csv

# Path to collect data from the Resources folder
employee_data = os.path.join('..', 'Resources', 'employee_data.csv')

# Specify the file to write to
output = os.path.join ('employee_data_converted.csv')

# Read in the CSV file
with open(employee_data, 'r') as csvfile, open(output, 'w', newline='') as csvfile1:
 
    # Split the data on commas
    csvreader = csv.reader(csvfile, delimiter = ',')
    header = next(csvreader)

    # Open the file using "write" mode. Specify the variable to hold the contents
    csvwriter = csv.writer(csvfile1, delimiter=',')
    csvwriter.writerow(['Emp ID', 'First Name', 'Last Name', 'DOB' ,'SSN', 'State'])

    for row in csvreader:
        
        ID = row [0]
       # Split data in each line to reorganize it
        Name = str.split(row [1])
       
        # Change position of letters for MM/DD/YYYY format
        chars = [char for char in row[2]]
        DOB = f'{chars[5]}{chars[6]}/{chars[8]}{chars[9]}/{chars[0]}{chars[1]}{chars[2]}{chars[3]}'
        
        # Split SSN line and create a string ***-**-{XXXX}
        chars = [char for char in row[3]]
        SSN = f'***-**-{chars[7]}{chars[8]}{chars[9]}{chars[10]}'
        
        # Split State name and leave upper case of first two letters
        chars = [char.upper() for char in row[4]]
        State = f'{chars[0]}{chars[1]}'
         
         # Write a string into CSV file
        csvwriter.writerow([ID,Name[0],Name[1],DOB,SSN,State])