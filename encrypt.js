<script runat="server">
    Platform.Load("Core", "1");

    // Define the Data Extension name
    var dataExtensionName = "YourDataExtension"; 

    // Retrieve the data from the Data Extension
    var dataExtension = DataExtension.Init(dataExtensionName);
    var rows = dataExtension.Rows.Retrieve();
    
    // Loop through the rows and process each record
    for (var i = 0; i < rows.length; i++) {
        var email = rows[i].email;   // Field 1: email
        var name = rows[i].name;     // Field 2: name
        var ref = rows[i].ref;       // Field 3: ref
        
        // Create the payload as a JSON object
        var payload = {
            "email": email,
            "name": name,
            "ref": ref
        };

        // Convert the payload object to a JSON string
        var payloadString = Stringify(payload);

        // Encrypt the payload (for demonstration, we are using Base64 encoding)
        var encryptedPayload = Base64Encode(payloadString);

        // Output encrypted payload (you can log it or use it in your process)
        Write("Encrypted Payload: " + encryptedPayload);
        
        // Optionally, store the encrypted payload back in the Data Extension or elsewhere
        // For example, to update a field in the Data Extension:
        dataExtension.Rows.Update({EncryptedPayload: encryptedPayload}, ['PrimaryKeyField'], [rows[i].PrimaryKeyField]);
    }
</script>
