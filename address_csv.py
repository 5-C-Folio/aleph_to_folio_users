from csv import DictReader
import json
from schema import userRecord
from address_parser import address_parser, nameSplit
import re
import uuid
import userGroup
def space_snip(string):
    # collapse consecutive spaces
    snipped = re.sub("  +", "", string)
    return snipped

def date_format(date):
    year = date[0:4]
    month = date[4:6]
    day = date[6:]
    return (f"{year}-{month}-{day}")

def userMaker(file):
    outputFile = []
    with open("amh_users.txt", 'r', encoding='utf8') as user_file:
        userparse =  DictReader(user_file, delimiter = "|")
        for row in userparse:
            x = uuid.uuid4()
            address = address_parser(row['ADDRESS1'])
            address = address.parse()
            name = nameSplit(row["Z303_NAME"])
            name = name.namesplit()
            name["email"] = row["EMAIL1"]
            name["phone"] = row["PHONE2"]
            if row['Z305_BOR_TYPE'] in ["EM", "RE", "SP"]:
                group = row["Z305_BOR_STATUS"] + "AC"
                #print (group)
            else:
                group =  row["Z305_BOR_STATUS"]+ row['Z305_BOR_TYPE']
            groupUUID = userGroup.groups("userGroups.csv", group)

            if address:

                if  len (space_snip(row["ZIP1"])) > 3:
                    address['postalCode'] = space_snip(row["ZIP1"])
                name["addresses"] = [address]

            newUser = userRecord(
                id = str(x),
                externalSystemId = space_snip(row["EXTERNAL_ID"]),
                barcode =  space_snip(row['BARCODE']),
                type = row['Z305_BOR_TYPE'],
                personal = name,
                expirationDate = date_format(row['Z305_EXPIRY_DATE']),
                patronGroup = groupUUID.getgroup(),
                customFields = {"bor_type": row['Z305_BOR_TYPE'],
                            "alephKey": space_snip(row["Z303_REC_KEY"]) })
            outputFile.append(newUser)

        return outputFile



if __name__ == "__main__":
    x = userMaker("mhc_users.txt")
    with open("outputFile.json", 'w') as output:
        json.dump(x, output, indent = 4)




