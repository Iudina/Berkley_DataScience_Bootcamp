import os
import csv

# Path to collect data from the Resources folder
budget_data = os.path.join('..', 'Resources', 'budget_data.csv')

NoOfMonths, Year, MonthlyChange = [], [], []
TotalRevenue, Month0 = 0, 0
 
# Read in the CSV file
with open(budget_data, 'r') as csvfile:

    # Split the data on commas
    csvreader = csv.reader(csvfile, delimiter = ',')
    header = next(csvreader)

    # Loop through the data
    for row in csvreader:
        # Calculate total number of month
        NoOfMonths.append(row[0])
        # Calculate total revenue
        TotalRevenue += float(row[1])
        # Calculate a list of month to month changes
        Month1 = float(row[1])
        Change = Month1 - Month0
        Month0 = Month1
        MonthlyChange.append(Change)
        Year.append(row[0])
        
        #MonthlyChange2.update({row[0]:Change})

# Remove first change from list because it is equal to ('first month revenue' - 0)
del(MonthlyChange[0])
del(Year[0])

# Calculate  average change
AverageChange = sum(MonthlyChange)/len(MonthlyChange)

# Return indexes of Max and Min Change
MaxInd = MonthlyChange.index(max(MonthlyChange))
MinInd = MonthlyChange.index(min(MonthlyChange))

# Form results and add them to string
my_str = "Financial Analysis\n" +\
        f'-' *50 +'\n' +\
        f'Total Months: {len(NoOfMonths)}\n' +\
        f'Net revenue: ${TotalRevenue}\n' +\
        f'Average Change: ${AverageChange}\n' +\
        f'Greatest Increase in profits: {Year[MaxInd]} ${max(MonthlyChange)}\n' +\
        f'Greatest Decrease in profits: {Year[MinInd]} ${min(MonthlyChange)}\n'
# Print results
print (my_str)

with open ("Financia Analysis.txt", "w") as file:
    file.write(my_str)