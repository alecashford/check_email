This is a script that attempts to guess a person's email address from their first name using common email patterns of corporate email addresses. Some use-cases for this include sales or marketing email campaigns or personal networking.

The script uses the API found at verify-email.org, you will need a key. It also expects a headerless, two-column CSV of full names (e.g. "John Doe") and corporate email domains (e.g. "@examplecompany.com") in that order. Place both in the main directory and name them as seen in the .gitignore (api_key.txt and data.csv, respectively).
