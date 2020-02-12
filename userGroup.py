from csv import DictReader

class groups():
    def __init__(self, file, usergroup):
        self.file = file
        self.usergroup = usergroup

    def getgroup(self):
        with open(self.file, 'r') as groupFile:
            groupDict = DictReader(groupFile)
            groupDict2 = {}
            for row in groupDict:
                groupDict2[row["AlephGroup"]] = row["UUID"]
            if  groupDict2.get(self.usergroup):
                print (groupDict2.get(self.usergroup))
                return groupDict2.get(self.usergroup)
            else:
                return "NOPE!"

if __name__ == "__main__":

    x = groups("userGroups.csv", "22SC")
    print (x.getgroup())
