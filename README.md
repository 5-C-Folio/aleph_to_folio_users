# aleph_to_folio_users

## Purpose
Migrate current users from Aleph user database to Folio compliant JSON
``` address_csv.py is included for offline testing ```
## Requirements
* usaddress
* CX_oracle
* Python 3.x

## Known Issues
* usaddress, as the name implies, does not handle non-US addresses well
* a large number of factors, including but not limited the Aleph database, are hardcoded
* poor commenting
