import requests
import json
import csv


base_query = "https://app.verify-email.org/api/v1/{}/verify/{}"
api_key = open("api_key.txt", "r").readline().strip()

successful_guess = []
failed_to_guess = []
needs_manual_processing = []

with open('data.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		full_name = row[0].lower().strip()
		domain = row[1].lower()
		
		first_name = full_name.split(" ")[0]
		last_name = full_name.split(" ")[-1]
		
		emails_to_try = [
			"{}{}@{}".format(first_name, last_name, domain),
			"{}{}@{}".format(last_name, first_name, domain),
			"{}.{}@{}".format(first_name, last_name, domain),
			"{}.{}@{}".format(last_name, first_name, domain),
			"{}{}@{}".format(first_name[0], last_name, domain),
			"{}{}@{}".format(first_name, last_name[0], domain),
			"{}@{}".format(first_name, domain),
			"{}@{}".format(last_name, domain),
		]
	
		confirmed_failure = True
		
		for email in emails_to_try:
			r = requests.get(base_query.format(api_key, email))
			json_data = json.loads(r.text)
			status_description = json_data["status_description"]
			smtp_log = json_data["smtp_log"]
			if status_description == "OK email":
				successful_guess.append("{} valid email for {}".format(email, full_name))
				confirmed_failure = False
				break
			elif status_description == "UNKNOWN email":
				needs_manual_processing.append(full_name)
				confirmed_failure = False
				break
			elif smtp_log != "MailboxDoesNotExist":
				print("Unexpected error for {}, smtp_log: {}".format(email, smtp_log))
				confirmed_failure = False
	
		if confirmed_failure:
			failed_to_guess.append(full_name)
	
	print("Script complete! Successful guesses for these names:")
	for line in successful_guess:
		print(line)
	
	print("\nThese names need manual processing:")
	
	for name in needs_manual_processing:
		print(name)
	
	print("\nScript failed to guess an email for these names:")
	for name in failed_to_guess:
		print(name)
