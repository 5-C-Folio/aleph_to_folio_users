import re
import usaddress
#https://usaddress.readthedocs.io/en/latest/
def truthChecker(dict, dictvalue):
    if dict.get(dictvalue):
        return dict.get(dictvalue)

class address_parser():
    def __init__(self, address):
        self.address = address


    def parse(self):
        y = re.sub("  +", "; ", self.address)
        x = y.split(';')
        z = " ".join(x[1:])
        address = {}
        try:
            rawAddress, addressType = usaddress.tag(z)
            addDict = dict(rawAddress)
            if addressType == 'PO Box':
                addressLine1 = addDict.get("USPSBoxType", '') + ' ' + addDict.get('USPSBoxID', '')
                address['addressLine1'] = addressLine1
                if addDict.get('Recipient', None):
                    addressLine2 = addDict.get('Recipient', None)
                    address['addressLine2'] = addressLine2
                if  addDict.get('PlaceName',None):
                    city = addDict.get('PlaceName', None)
                    address["city"] = city
                if  addDict.get('StateName',None):
                    statename = addDict.get('StateName', None)
                    address['region'] = statename
                if addDict.get('ZipCode', None):
                    address['postalCode'] = addDict['ZipCode']


                return address
            if addressType == 'Street Address' or addressType == 'Ambiguous' :
                addressLine1 = []
                addressLine1.append(addDict.get("AddressNumber", ''))
                addressLine1.append(addDict.get("StreetNamePreDirectional", ''))
                addressLine1.append(addDict.get("StreetName", ''))
                addressLine1.append(addDict.get("StreetNamePostType", ''))
                address['addressLine1']= re.sub(" +", ' ', ' '.join(addressLine1))

                addressLine2 = []
                addressLine2.append(addDict.get('BuildingName',''))
                addressLine2.append(addDict.get("OccupancyType",''))
                addressLine2.append(addDict.get('OccupancyIdentifier',''))
                if  ' '.join(addressLine2) != '  ':
                    address["addressLine2"] = ' '.join(addressLine2)

                if addDict.get('StateName', None):
                    address['region'] = addDict['StateName']

                if addDict.get("PlaceName", None):
                    address['city'] = addDict["PlaceName"]

                if addDict.get('ZipCode', None):
                    address['postalCode'] = addDict['ZipCode']
                return address
            if addressType == 'Ambiguous' :
                print ('oops')



        except usaddress.RepeatedLabelError:
            x = y.split(';')
            if len(x) > 2:
                address1 = x[1]
                city_state = x[2]

                if "," in city_state:
                    city_list = city_state.split(",")
                    city = city_list[0]
                    state = city_list[1]

                    return {"addressLine1": address1, "city": city, "region": state}

            return address


class nameSplit():
    def __init__(self, name):
        self.name = name

    def namesplit(self):
        if "," in self.name:
            nameList = self.name.split(",")
            lastName = nameList[0]
            nameblock = nameList[1]
            nameblock = nameblock.lstrip()
            firstMiddle = nameblock.split(" ")
            firstName = firstMiddle[0]
            if len(firstMiddle) > 1:
                middleName = firstMiddle[1]
                return {"firstName": firstName, "middleName": middleName, "lastName" : lastName}
            else:
                return {"firstName": firstName,  "lastName": lastName}
        else:
            return {"lastName": self.name}


if __name__ == "__main__":
    print("hello")