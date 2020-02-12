import cx_Oracle
import json
import re
with open("passwords.json", "r") as pwFile:
    pw =json.load(pwFile)


class query():
    def __init__(self, connection):
        self.connection = connection

    #convert tuple to dict
    def makeDictFactory(self,cursor):
        columnNames = [d[0] for d in cursor.description]
        def createRow(*args):
            return dict(zip(columnNames, args))
        return createRow

    def space_snip(string):
        #collapse consecutive spaces
        snipped = re.sub("  +", "", string)
        return snipped



    def user_query(self):
        cursor = self.connection.cursor()
        cursor.execute( '''
    SELECT us.Z303_REC_KEY ,  SUBSTR(ext.Z308_REC_KEY,3) as external_id, 
    SUBSTR(bar.Z308_REC_KEY,3) as barcode, 
    us.Z303_NAME,
    address1.Z304_EMAIL_ADDRESS as email1,
    address2.Z304_EMAIL_ADDRESS as email2,
    address1.Z304_TELEPHONE as phone1,
    address2.Z304_TELEPHONE as phone2,
    address1.Z304_ADDRESS as address1,
    address1.Z304_ADDRESS_TYPE as addresstype1,
    address1.Z304_ZIP as zip1,
    address2.Z304_ADDRESS as address2,
    address2.Z304_ZIP as zip2,
    address2.Z304_ADDRESS_TYPE as addresstype2,
    threeohfive.Z305_BOR_TYPE,
    threeohfive.Z305_BOR_STATUS,
    threeohfive.Z305_EXPIRY_DATE
    from FCL00.Z303 us
    left join FCL00.Z308 ext
    on us.Z303_REC_KEY = ext.Z308_ID
    and SUBSTR(ext.Z308_REC_KEY, 0,2) = '02'
    inner join FCL00.Z308 bar
    on us.Z303_REC_KEY = bar.Z308_ID
    and SUBSTR(bar.Z308_REC_KEY, 0,2) = '01'
    left join FCL00.Z304 address1 
    on us.Z303_REC_KEY = SUBSTR(address1.Z304_REC_KEY,0,12) and SUBSTR(address1.Z304_REC_KEY,13) = '01'
    left join FCL00.Z304 address2 
    on us.Z303_REC_KEY = SUBSTR(address2.Z304_REC_KEY,0,12) and SUBSTR(address2.Z304_REC_KEY,13) = '02'
    inner join AMH50.Z305 threeohfive on 
    us.Z303_REC_KEY = substr(threeohfive.Z305_REC_KEY,0,12)
    WHERE threeohfive.Z305_BOR_STATUS IN ('30','31','32','33','37,41')
     ''')
        cursor.rowfactory = self.makeDictFactory(cursor)
        return cursor.fetchall()

if __name__ == "__main__":
    with open("passwords.json", "r") as pwFile:
        pw = json.load(pwFile)

    x= query(cx_Oracle.connect(f"{pw['username']}", f"{pw['password']}", "server"))
    x = x.user_query()
    for row in x :
        print(row)


