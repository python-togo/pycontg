import csv
from app.utils.python_communities import send_email

with open("app/utils/PyConOrganizer.csv") as file:
    reader = csv.reader(file)
    next(reader)
    print(reader)
    for Timestamp, name, email in reader:
        if '@' not in email:
            print(f"Invalid email for {name}: {email}")
            continue
        print(f"Sending email to {name}")
        print(f"Email: {email}")
        send_email(to=email, org_name=name)
