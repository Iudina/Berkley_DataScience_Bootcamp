import os
import csv

# Path to collect data from the Resources folder
election_data = os.path.join('..', 'Resources', 'election_data.csv')

TotalVotes = 0
Results_dict= {}

# Read in the CSV file
with open(election_data, 'r') as csvfile:

    # Split the data on commas
    csvreader = csv.reader(csvfile, delimiter = ',')
    header = next(csvreader)

    # Loop through the data to create dictionary 'Candidate-votes'
    for row in csvreader:
        TotalVotes +=1
        if row[2] in Results_dict:
            Results_dict[row[2]] += 1
        else:
            Results_dict[row[2]] = 1

# Find the winner
Winner = max(Results_dict, key=Results_dict.get)

# Compose a string for output
my_str = "Election Results\n" +\
         "-" * 25 + '\n' +\
        f'Total Votes: {TotalVotes}\n' +\
         "-" * 25 + '\n'

# Split dictionary to calculate %% and add data to my_string (':.3f - three digits in float format otherwise conver to exp)
for key, value in Results_dict.items():
    my_str += f'{key}: {value/TotalVotes*100:.3f}% ({value})\n'
   
my_str += "-" * 25 + '\n' +\
        f'Winner: {Winner}\n' +\
          "-" * 25      

# Print results     
print(my_str)         

with open ("Election Results.txt", "w") as file:
    file.write(my_str)

