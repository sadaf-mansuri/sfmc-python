i<script runat="server">
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


<script runat="server">
    Platform.Load("Core", "1.1");

    function logErrorToDE(errorMessage) {
        try {
            var logDE = DataExtension.Init("ScriptLogDE");
            var logEntry = {
                "LogMessage": errorMessage,
                "LogTimestamp": Platform.Function.Now(),  // Current timestamp
                "LogLevel": "Error"
            };
            logDE.Rows.Add(logEntry);  // Add the log entry to the Data Extension
        } catch (logError) {
            Write("Failed to write to log Data Extension: " + logError.message + "<br>");
        }
    }

    try {
        // Your script logic here
        Write("Processing records...<br>");
        // Example of adding additional logs
        logErrorToDE("Starting record processing...");

        // Simulating a process that could cause an error
        throw new Error("Sample error for testing");

    } catch (e) {
        Write("An error occurred: " + e.message + "<br>");
        logErrorToDE(e.message);  // Log the error message to Data Extension
    }
</script>

Platform.Load("Core", "1");

var key = "your-secret-key";  // Same key used for encryption
var iv = "your-initialization-vector";  // Same IV used for encryption
var encryptedValue = "ENCRYPTED_TEXT_HERE";  // Replace with the encrypted string

var crypto = require("crypto");
var decipher = crypto.createDecipheriv("aes-256-cbc", key, iv);

var decryptedValue = decipher.update(encryptedValue, 'hex', 'utf8');
decryptedValue += decipher.final('utf8');

Write("Decrypted Value: " + decryptedValue);


<script runat="server">
    Platform.Load("Core", "1");

    var key = "your-secret-key";  // Your decryption key
    var base64EncodedCipherText = "BASE64_ENCODED_STRING";  // Replace with your Base64 encoded string

    // Step 1: Extract the IV (first 16 bytes) from the Base64-encoded string
    function getIVFromBase64(encodedString) {
        var binaryString = atob(encodedString);
        var byteArray = new Uint8Array(binaryString.length);
        for (var i = 0; i < binaryString.length; i++) {
            byteArray[i] = binaryString.charCodeAt(i);
        }
        return byteArray.slice(0, 16);  // First 16 bytes are the IV
    }

    var iv = getIVFromBase64(base64EncodedCipherText);

    // Step 2: Decrypt the remaining cipher text (without IV)
    var cipherText = Buffer.from(base64EncodedCipherText, 'base64').slice(16);  // Slice off the first 16 bytes (IV)

    var crypto = require("crypto");
    var decipher = crypto.createDecipheriv("aes-256-cbc", key, iv);

    var decryptedValue = decipher.update(cipherText, 'hex', 'utf8');
    decryptedValue += decipher.final('utf8');

    Write("Decrypted Value: " + decryptedValue);
</script>


var dataExtension = DataExtension.Init("YourDEName");
var rows = dataExtension.Rows.Retrieve();
for (var i = 0; i < rows.length; i++) {
    var encryptedValue = Encrypt(rows[i].YourField, 'encryptionKey');  // Custom function or algorithm
    dataExtension.Rows.Update({YourEncryptedField: encryptedValue}, ['PrimaryKeyField'], [rows[i].PrimaryKeyField]);
}




