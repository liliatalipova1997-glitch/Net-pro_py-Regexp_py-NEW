import csv
import re
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код
for contact in contacts_list[1:]:
    full_name = " ".join(contact[0:3]).split()
    full_name = [part for part in full_name if part]
    if len(full_name) >= 3:
        contact[0] = full_name[0]
        contact[1] = full_name[1]
        contact[2] = full_name[2]
    elif len(full_name) == 2:
        contact[0] = full_name[0]
        contact[1] = full_name[1]
        contact[2] = ""
    elif len(full_name) == 1:
        contact[0] = full_name[0]
        contact[1] = ""
        contact[2] = ""

phone_pattern = re.compile(
  r'(\+7|8)?\s*\(?(\d{3})\)?\s*[- ]?(\d{3})'
  r'[- ]?(\d{2})[- ]?(\d{2})'
  r'(?:\s*\(?\s*(?:доб\.?|ext|добавочный\.?)\s*(\d+)\s*\)?)?'
)

for contact in contacts_list[1:]:
    phone = contact[5]
    if phone:
        match = phone_pattern.search(phone)
        if match:
            formatted_phone = f'+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}'
            if match.group(6):
                formatted_phone += f' доб.{match.group(6)}'
            contact[5] = formatted_phone

contacts_dict = {}
for contact in contacts_list[1:]:
    key = (contact[0], contact[1])
    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        existing = contacts_dict[key]
        for i in range(len(contact)):
            if not existing[i] and contact[i]:
                existing[i] = contact[i]

new_contacts_list = [contacts_list[0]] + list(contacts_dict.values())

pprint(new_contacts_list)

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(new_contacts_list)