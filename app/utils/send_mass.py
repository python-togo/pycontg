import csv
from app.utils.python_communities import send_email

with open("app/utils/PyConOrganizer.csv") as file:
    reader = csv.reader(file)
    next(reader)
    for Timestamp, name, email in reader:
        if '@' not in email:

            continue

        send_email(to=email, org_name=name)
