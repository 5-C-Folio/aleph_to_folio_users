# aleph_to_folio_users

## Purpose
Migrate current users from Aleph user database to Folio compliant JSON
``` address_csv.py is included for offline testing ```
## Requirements
* usaddress
* CX_oracle
* Python 3.x

## Instructions
1 obtain credentials for Aleph oracle db and place as json in password.json
2 In query, specify the ADM to use and any limits on patron group by adding a WHERE in the query
3 Run querytouser.py
```Depending on the where clause and the size of the query, the process may take a while and produce a very large file```


## Known Issues
* usaddress, as the name implies, does not handle non-US addresses well
* a large number of factors, including but not limited the Aleph database, are hardcoded
* poor commenting
* unclear if UUID for groups will persist through Folio loads
* user UUIDs are randomly generated
