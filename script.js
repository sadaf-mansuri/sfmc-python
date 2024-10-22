<script runat="server">
    Platform.Load("Core", "1.1");
    
    var deName = "TargetDataExtension";  // Replace with your Target Data Extension name
    var de = DataExtension.Init(deName);
    
    // Retrieve all rows from the Target Data Extension
    var dataRows = de.Rows.Retrieve();
    
    // Loop through each row (record)
    for (var i = 0; i < dataRows.length; i++) {
        var row = dataRows[i];
        
        // Fetch the encrypted field value
        var encryptedField = row.EncryptedField;

        // Decrypt the encrypted field (assuming AES128 encryption)
        // Replace this with the appropriate key and encryption method used
        var key = "your-encryption-key";  // Replace with your decryption key
        var keyBlob = Platform.Function.Blob.FromString(key);
        var encryptedBlob = Platform.Function.Base64Decode(encryptedField);
        var decryptedBlob = Platform.Function.Crypto.DecryptWithManagedIV("AES128", keyBlob, encryptedBlob);
        var decryptedValue = decryptedBlob.toString();

        // Update the row with the decrypted value (or store it in another field)
        var updateObject = {
            "DecryptedField": decryptedValue  // Assuming you have a DecryptedField column in the DE
        };

        // Update the record in the Data Extension
        de.Rows.Update(updateObject, ["Id"], [row.Id]);

        Write("Decrypted value for record " + row.Id + ": " + decryptedValue + "<br>");
    }
</script>