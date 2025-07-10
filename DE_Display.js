<script runat="server">
Platform.Load("Core", "1.1");

var dataExtensionName = "campaign_name_categories";

// Retrieve all records from the DE
var deRows = DataExtension.Init(dataExtensionName).Rows.Retrieve();

// Begin building HTML table
var htmlTable = "<table border='1' cellpadding='5' cellspacing='0' style='border-collapse: collapse;'>";
htmlTable += "<tr><th>Campaign Name</th><th>Order</th><th>Type</th></tr>";

// Loop through rows and build table rows
for (var i = 0; i < deRows.length; i++) {
    htmlTable += "<tr>";
    htmlTable += "<td>" + deRows[i].CampaignName + "</td>";
    htmlTable += "<td>" + deRows[i].Order + "</td>";
    htmlTable += "<td>" + deRows[i].Type + "</td>";
    htmlTable += "</tr>";
}

htmlTable += "</table>";
</script>

<!-- Output the table to the page -->
<html>
  <head>
    <title>Campaign Name Categories</title>
  </head>
  <body>
    <h2>Campaign Name Categories</h2>
    <div>
      %%=v(@htmlTable)=%%
    </div>
  </body>
</html>
