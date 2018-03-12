import csv

plans = csv.reader(open('plans.csv', 'r'))
zips = csv.reader(open('zips.csv', 'r'))
slcsp = csv.reader(open('slcsp.csv', 'r'))
prices = []
kyrow = 'No KY'
no_info_example = 'None'

# zip code 64148 corresponds to rate area MO3
# on the update CSV, this zip code has 245.2 as the price
# there don't seem to be any state info on plans.csv with KY as the state
for row in plans:
	if row[1] == 'MO' and str(row[4]) == '3' and row[2] == "Silver":
		prices.insert(0, row[3])
	elif row[1] == 'KY':
		kyrow = row
	elif row[1] == 'NJ' and str(row[4]) == '1':
		no_info_example = row
 
prices.sort()

print "Check one: ", prices[1]
print "Check two: ", kyrow
print "No Info Zip Ex: ", no_info_example
# result is 245.2
#PASS

# when I run this, 54923 has no plan info. this means they must have multiple rate areas
rate_areas = []


for row in zips:
	if row[0] == "54923":
		rate_areas.insert(0, row[1] + row[4])
print "Check three: ", rate_areas

# result was ['11', '11', '15']; 
# PASS

no_info_zips = []
for row in slcsp:
	if row[1] == '':
		no_info_zips.insert(0, row[0])

print no_info_zips

# one of those was 07184 which corresponds to NJ1 - added a hceck above and wasn't found
# I would generally go back to whoever gave this to me, since this was supposed to be a complete list of plans,
# and inquire about why Kentucky and this district don't seem to have plan info
# Perhaps we're missing information.







