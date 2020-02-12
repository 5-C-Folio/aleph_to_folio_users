import re

class address_parser():
    def __init__(self, address):
        self.address = address



    def parse(self):
        y = re.sub("  +", ";", self.address)
        #create a list based on the ;
        y = y.split(";")
        #ignore [0] and define [1] as address 1

        if len(y) > 2:
            address1 = y[1]
            city_state = y[2]

            if "," in city_state:
                city_list = city_state.split(",")
                city = city_list[0]
                state = city_list[1]

                return {"addressLine1":address1, "city":city, "region": state}
            else:

                return {"addressLine1":address1, "addressLine2":f"{city_state}"}
            #if the address doesn't conform to a normal looking address field
        else: pass


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