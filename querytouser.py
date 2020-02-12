import query
import json
from schema import userRecord
from address_parser import address_parser, nameSplit
import re
import uuid
import userGroup
import cx_Oracle
def space_snip(string):
    # collapse consecutive spaces
    snipped = re.sub("  +", "", string)
    return snipped

def date_format(date):
    date = str(date)
    year = date[0:4]
    month = date[4:6]
    day = date[6:]
    return (f"{year}-{month}-{day}")

def userMaker():
    with open("passwords.json", "r") as pwFile:
        pw = json.load(pwFile)
    alephcursor = query.query(cx_Oracle.connect(f"{pw['username']}", f"{pw['password']}", "server"))
    aleph= alephcursor.user_query()
    outputFile = []
    for row in aleph:
            id = uuid.uuid4()
            if row['ADDRESS1']:
                address = address_parser(row['ADDRESS1'])
                address = address.parse()
            elif row['ADDRESS2']:
                address = address_parser(row['ADDRESS2'])
                address = address.parse()
            try:
                if row["ZIP1"] is not None:
                    address["postalCode"] = space_snip(str(row["ZIP1"]))
                elif row["ZIP2"]:
                    address["postalCode"] = space_snip(str(row["ZIP2"]))
                else:
                    address["postalCode"]=''
            except TypeError:
                continue


            name = nameSplit(row["Z303_NAME"])
            name = name.namesplit()
            try:
                ex = space_snip(row["EXTERNAL_ID"])
            except TypeError:
                ex = None

            if row['EMAIL1'] :
                name["email"] = row["EMAIL1"]
            elif row['EMAIL2']:
                name["email"] = row["EMAIL2"]
            else:
                name["email"] = "##"

            if row["PHONE1"]:
                name["phone"] = row["PHONE1"]
            elif row["PHONE2"]:
                name["phone"] = row["PHONE2"]
            else:
                name["phone"] = ''

            if row['Z305_BOR_TYPE'] in ["EM", "RE", "SP", "FC"]:
                group = row["Z305_BOR_STATUS"] + "AC"
                print (group)
                groupID = userGroup.groups("userGroups.csv", group)
                groupUUID = groupID.getgroup()
            else:
                try:
                    group =  row["Z305_BOR_STATUS"]+ row['Z305_BOR_TYPE']
                    groupID = userGroup.groups("userGroups.csv", group)
                    groupUUID = groupID.getgroup()
                except TypeError:
                    groupUUID = "1bc376ce-2886-478b-9e66-8c17aad8bceb"
            if row['Z305_BOR_TYPE']:
                rowtype = row['Z305_BOR_TYPE']
            else:
                rowtype = ''

            name["addresses"] = [address]
            newUser = userRecord(
                id = str(id))
            if ex:
                newUser.externalSystemId = ex
            if row['BARCODE']:
                newUser.barcode =  space_snip(row['BARCODE'])
            newUser.type = rowtype
            newUser.personal = name
            newUser.expirationDate = date_format(row['Z305_EXPIRY_DATE'])
            newUser.patronGroup = groupUUID
            newUser.customFields = {"bor_type": row['Z305_BOR_TYPE'],
                            "alephKey": space_snip(row["Z303_REC_KEY"]) }

            outputFile.append(newUser)

    return outputFile



if __name__ == "__main__":
    x = userMaker()
    with open("outputFile.json", 'w') as output:
        json.dump(x, output, indent = 4)
