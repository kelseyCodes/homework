import csv, os
zips = csv.reader(open('zips.csv', 'r'))
plans = csv.reader(open('plans.csv', 'r'))
original_csv = open('slcsp.csv', 'r')
slcsp = csv.reader(original_csv)


# Since this is a LOT of zip codes, lets pull in slcsp's zips so we only get the data for those zips, not all of them
zips_we_want = {}
# we don't want to include headers in this comparison
next(slcsp)
next(zips)
next(plans)

for row in slcsp:
	zips_we_want[row[0]] = {}

#we'll go through zips and mpa zip codes to state/rate area 
for row in zips:
	# we only care about our relevant zips and need to concatenate state and rate_area fields
	if row[0] in zips_we_want:
		# if we haven't assigned a value for rate_area yet or our rate_area is the same
		if zips_we_want[row[0]] == {} or zips_we_want[row[0]] == row[1] + row[4]:
			zips_we_want[row[0]] = row[1] + row[4]
		# in the case of multiple rate_areas for the same zipcode, leave blank
		else:
			zips_we_want[row[0]] = ""
	else:
		next

rate_areas = zips_we_want.values()
rate_obj = {}

# include any rates that are Silver plans for that rate area in another object
for row in plans:
	if row [2] == 'Silver' and (row[1] + row[4]) in rate_areas:
		if not (row[1] + row[4]) in rate_obj:
			rate_obj[(row[1] + row[4])] = [row[3]]
		# if there are less than 2 items in our array, we want to add the other plans to find the slcsp
		elif len(rate_obj[(row[1] + row[4])]) < 2:
			rate_obj[(row[1] + row[4])].insert(0,row[3])
		# if there are more than 2 items in our array, since we only need the second lowest price, 
		# we can just store the lowest 2 so we don't store a bunch of data that's irrelevant
		else: 
			rate_obj[(row[1] + row[4])].insert(0,row[3])
			rate_obj[(row[1] + row[4])].sort()
			rate_obj[(row[1] + row[4])].pop()

zips_and_prices = {}
# combine our two dicts so we have a zip code to prices mapping
for zip in zips_we_want:
	if zips_we_want[zip] != "" and zips_we_want[zip] in rate_obj:
		zips_and_prices[zip] = rate_obj[zips_we_want[zip]]
	else:
		zips_and_prices[zip] = ""

# create a temporary file to write too since we can't read and write simultaneously to a file
writer = csv.writer(open('temp_file.csv', 'w'))
writer.writerow(['zipcode','rate'])

# we need to rewind the file since we have to print these in the original order
# and our zips_we_want object does not store keys in order
original_csv.seek(0)
next(slcsp)

for row in slcsp:
	temp_list = zips_and_prices[row[0]]
	if temp_list != "":
		writer.writerow([row[0], temp_list[1]])
	else:
		writer.writerow([row[0], ""])

# rename the file to our original CSV, as required in the Readme
os.remove('./slcsp.csv')
os.rename('./temp_file.csv', './slcsp.csv')
