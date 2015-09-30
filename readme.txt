MockupJSONParser:
commande line to compare preference mockups and spreadsheets

Example Usage: 
	python mockup.py -help
	python mockup.py -action=generate -input=in.json -output=out.csv
	python mockup.py -action=compare -input=in.json -output=out.csv \
							-s=correct.csv

Two Actions:
	-generate:
		this action accepts a Balsamiq Mockup input file and outputs a
		summary of the mockup in a csv file format
	-compare: 
		This action first executes the generate action but then 
		also compares with  

File Arguments:
	-input: 
		This file should be the exported Balsamiq Mockup JSON.
		To generate such a JSON file, in the Balsamiq application
		use
			Project->Export->Mockup TO JSON
	-output:
		This will be a a csv file where each row represents one
		preference and the following data is found in the columns
		index:  
			- logical order of the preference where the top
			left preference is indexed at number 1
			- skips five indices for every five indices 
			counted to accomodate for future preferences
		name: raw preference name found in blue callout box
		summary: text in label
		type: corresponds to PREF_TYPE 
		default_val: 	

Caveats: 
 - Each Preference must be organized into a Balsamiq 'Group' before
   exportation.  That is Balsamiq 'Groups' should contain at least 
   two or more things, a preference label and a preference name.
 - This parser will still with 'Groups' of 'Groups' as long as the 
   lowest level of 'Group' is a preference.
 - 
