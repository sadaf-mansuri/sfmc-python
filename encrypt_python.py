import json
import urllib.parse
from simple_salesforce import Salesforce
from trustpilot_authenticated_encryption import encryption

# Salesforce Authentication - login using the security token method, simply include the Salesforce method and pass in your Salesforce username, password and token (this is usually provided when you change your password):
sf = Salesforce(username='YOURUSER@NAME.COM', password='YOURPASSWORD', security_token='YOURSECURITYTOKEN')

# Trustpilot BGL keys 
# encryption key
encrypt_key = "YOURTPENCRYPTIONKEY"
# authentication key 
hash_key = "YOURTPAUTHENTICATIONKEY" 
# your domain
domain = "YOURDOMAIN.COM"

# Query contacts - get contacts name, email and salesforce id 
records = sf.query("SELECT Id, Name, Email FROM Contact")
records = records['records']
# print(records)
for record in records:
    name = record['Name']
    print (name)
    email = record['Email']
    # print(email)
    uniqueID = record['Id']
    # print(uniqueID)
    payload = {"referenceId": uniqueID, "name": name, "email": email}
    message = json.dumps(payload)
    encrypted_message = encryption.encrypt(message.encode("utf-8"), encrypt_key, hash_key)
    enc_result = (encrypted_message.decode("ascii"))
    final_encryption = urllib.parse.quote(enc_result)
    print ("Trustpilot business generated link:")
    bgl_link = "https://www.trustpilot.com/evaluate-bgl/" + domain + "?p=" + final_encryption
    print (bgl_link)
    info = sf.Contact.get(uniqueID)
    updateSF = sf.Contact.update(uniqueID, {'Description': bgl_link})
    print("Salesforce description field updated with Tustpilot Business Generated Link")
    SF_description_field = info['Description']
    print (SF_description_field)
