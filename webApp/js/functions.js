function downloadRecordTable(filename)
{
    var downloadLink;
    var tableID = "Attendance_Data";
    var dataType = 'application/vnd.ms-excel';
    var tableSelect = document.getElementById(tableID);
    var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');

    // Specify file name
    filename = filename + '.xls';

    // Create download link element
    downloadLink = document.createElement("a");

    document.body.appendChild(downloadLink);

    if(navigator.msSaveOrOpenBlob){
        var blob = new Blob(['\ufeff', tableHTML], {
            type: dataType
        });
        navigator.msSaveOrOpenBlob( blob, filename);
    }else{
        // Create a link to the file
        downloadLink.href = 'data:' + dataType + ', ' + tableHTML;

        // Setting the file name
        downloadLink.download = filename;

        //triggering the function
        downloadLink.click();
    }
}

function compareDateFunc() {
  var startdate = document.getElementById("startDate").value;
  var enddate = document.getElementById("endDate").value;
  if(enddate != '' && startdate != '')
  {
          if(enddate < startdate)
        {
            alert("Start Date is greater than End Date !");
            return false;
        }
  }
return true;
}