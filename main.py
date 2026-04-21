import csv
import re


with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

for contact in contacts_list[1:]:
    full_name = " ".join(contact[:3]).split()
    contact[0:3] = (full_name + ["", "", ""])[:3]


phone_pattern = re.compile(
    r'(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})'
    r'(?:\s*\(?(доб\.?|ext\.?)\s*(\d+)\)?)?'
)

def format_phone(phone):
    match = phone_pattern.search(phone)
    if not match:
        return phone

    number = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"

    if match.group(7):
        number += f" доб.{match.group(7)}"

    return number

for contact in contacts_list[1:]:
    if contact[5]:
        contact[5] = format_phone(contact[5])


contacts_dict = {}

for contact in contacts_list[1:]:
    key = (contact[0], contact[1])

    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        existing = contacts_dict[key]
        for i in range(len(contact)):
            if contact[i] and not existing[i]:
                existing[i] = contact[i]


result = [contacts_list[0]] + list(contacts_dict.values())


with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(result)