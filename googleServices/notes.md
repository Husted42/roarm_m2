Linking accounts and creating credentials is necessary to read the google assistant input

# Account linking
## IFTT
The workflow for getting the assistant to send a mail was done via IFTT.

Our flow is: 
 - IF : Scence Robotarm is activated
 - Then : Send a gmail

## Gmail
Create google credentials
 - Create OAuth client id
    - google auth platform -> credentials -> credentials secret
    - Make sure to download the credentials as json when creating them

*Test account link*
test the connection with `test_gmail_reader.py`
 1) Setup path to credentials 
 2) Add yourself as test user in google auth platform -> credentials -> credentials secret
 3) Enable API at gmail.googleapis.com/

