var rowsToShow=[];

function findTable() {
  var input, filter, table, tr, td, i, txtValue;
  var fetchData = {
          "inputName": {"valll": document.getElementById("inputName").value.toUpperCase(), "col":1},
          "inputEmpid": {"valll": document.getElementById("inputEmpid").value.toUpperCase(), "col":2},
          "inputGrade": {"valll": document.getElementById("inputGrade").value.toUpperCase(), "col":3},
          "inputPractice": {"valll": document.getElementById("inputPractice").value.toUpperCase(), "col":4},
          "inputOffering": {"valll": document.getElementById("inputOffering").value.toUpperCase(), "col":5},
          "inputRdct": {"valll": document.getElementById("inputRdct").value.toUpperCase(), "col":6},
          "inputLanguage": {"valll": document.getElementById("inputLanguage").value.toUpperCase(), "col":7},
          "inputLevel": {"valll": document.getElementById("inputLevel").value.toUpperCase(), "col":8},
          "inputTools": {"valll": document.getElementById("inputTools").value.toUpperCase(), "col":9},
          "inputCompany": {"valll": document.getElementById("inputCompany").value.toUpperCase(), "col":10},
          "inputMicrocontroller": {"valll": document.getElementById("inputMicrocontroller").value.toUpperCase(), "col":11},
          "inputTechnology": {"valll": document.getElementById("inputTechnology").value.toUpperCase(), "col":12},
          "inputps1": {"valll": document.getElementById("inputps1").value.toUpperCase(), "col":13},
          "inputps2": {"valll": document.getElementById("inputps2").value.toUpperCase(), "col":14},
          "inputps3": {"valll": document.getElementById("inputps3").value.toUpperCase(), "col":15}
        }

  table = document.getElementById("dataTable");
  tr = table.getElementsByTagName("tr");
  showAllRows(tr);
  var textPresent = false;
  for (var i in fetchData){
    if (fetchData[i]['valll'] != ""){
    textPresent = true;
    }
  }

  if(textPresent){
    for (var inp in fetchData) {
      filter = fetchData[inp]['valll'];
      if (filter){
          for (i = 1; i < tr.length; i++) {
            if (tr[i].style.display != "none"){
                td = tr[i].getElementsByTagName("td")[fetchData[inp]['col']];
                if (td) {
                  txtValue = td.textContent || td.innerText;
                  if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                  } else {
                    tr[i].style.display = "none";
                  }
                }
            }
          }
      }
    }
  }
  else{
    showAllRows(tr);
  }

}

function showAllRows(tr){
    for (var i=0; i < tr.length; i++){
    tr[i].style.display = "";
    }
}

var newWin = 0;

function addSelected(rowNum){
    table = document.getElementById("dataTable");
    tr = table.getElementsByTagName("tr");

    if (window.newWin == 0){
        window.newWin = window.open("about:blank", rowNum, "width=auto,height=auto");
        console.log(window.newWin);
        window.newWin.document.write("<html> <head> <link href=\"/compete_mgt/static/css/sb-admin-2.css\" rel=\"stylesheet\"> </head> <body> <script src=\"/compete_mgt/static/js/myTableFunctions.js\"></script> <div class=\"card shadow mb-4\"> <div class=\"card-header py-3\"> <h6 class=\"m-0 font-weight-bold text-primary\">Selected</h6> </div> <div class=\"card-body\"> <div class=\"table-responsive\"> <table class=\"table table-bordered\" id=\"dataTable\"><thead id=\"headers\"><tr><th>Remove</th><th>Name</th><th>Emp ID</th><th>Grade</th><th>Practice</th><th>Offering</th><th>RDCT</th><th>Language</th><th>Level</th><th>Company</th><th>Tools</th><th>Microcontroller</th><th>Technology</th><th>ProjectSpecific1</th><th>ProjectSpecific2</th><th>ProjectSpecific3</th></tr></thead><tbody></tbody></table></div></div> <button id=\"export\" onclick=\"writeHeadersToExcel()\"> Export </button> </div></body></html>");
        var timer = setInterval(function() {
            if(window.newWin.closed) {
                clearInterval(timer);
                window.newWin = 0;
                alert('Selected Staff reset!');
                for (var i=0; i < tr.length; i++){
                    try{
                        document.getElementById("button"+(i)).style.opacity = "";
                        document.getElementById("button"+(i)).style.pointerEvents  = "auto";
                    }catch(err){
                        document.getElementById("button"+(i)).style.opacity = "";
                        console.log(err);
                    }
                }
            }
        }, 1000);
    }

    toggleSelection(tr,rowNum, "none", 0.4, false);

    document.getElementById("button"+(rowNum)).style.pointerEvents = 'none';
    document.getElementById("button"+(rowNum)).style.opacity = 0.4;
    try{
    var selectedTable = window.newWin.document.getElementById("dataTable");
    rowAdded = selectedTable.insertRow(selectedTable.rows.length);
    }catch(err){
    var selectedTable = window.newWin.document.getElementById("dataTable");
    rowAdded = selectedTable.insertRow(selectedTable.rows.length);
    }
    console.log(rowAdded);
    for (var i=0; i < tr[rowNum+2].cells.length; i++){
        td = rowAdded.insertCell(0);
        if (i == 0){
            buttonId = tr[rowNum+2].cells[i].id;
            td.id = buttonId;
            keyy = buttonId.replace('button', '');
                                            td.innerHTML = "<img class=\"select-img\" id=\""+buttonId+"\" onclick=\"removeSelected(this,"+keyy+")\" src=\"/compete_mgt/static/img/deselected.png\">"
        }
        else{
            td.innerText = tr[rowNum+2].cells[i].innerText;
        }
        rowAdded.appendChild(td);
    }
}

function toggleSelection(tr, rowNum, pointEve, opac, openerNeeded){
    filter = tr[rowNum+2].getElementsByTagName("td")[2];
    filterValue = filter.textContent || filter.innerText;
    console.log(filterValue);

    for (var i=0; i < tr.length; i++){
        try{
        td = tr[i].getElementsByTagName("td")[2];
          if (td) {
             txtValue = td.textContent || td.innerText;
             console.log(txtValue);
             if (txtValue === filterValue) {
                if(openerNeeded){
                    window.opener.document.getElementById("button"+(i-2)).style.pointerEvents = pointEve;
                    window.opener.document.getElementById("button"+(i-2)).style.opacity = opac;
                }
                else{
                    document.getElementById("button"+(i-2)).style.pointerEvents = pointEve;
                    document.getElementById("button"+(i-2)).style.opacity = opac;
                }
             }
          }
        }catch(err){
            console.log(err);
        }
    }
}

function removeSelected(other, rowNum){
    var selectedTable = this.document.getElementById("dataTable");
    var mainTable = window.opener.document.getElementById("dataTable");
    selectedTable.deleteRow(other.parentNode.parentNode.rowIndex);
    window.opener.document.getElementById(other.parentNode.id).style.opacity = "";
    window.opener.document.getElementById(other.parentNode.id).style.pointerEvents  = "auto";
    table = window.opener.document.getElementById("dataTable");
    tr = table.getElementsByTagName("tr");
    toggleSelection(tr, rowNum, "auto", "", true);
}

function writeHeadersToExcel()
{
    var downloadLink;
    var dataType = 'application/vnd.ms-excel';
    var tableSelect = this.document.getElementById("dataTable");
    var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');

    filename = 'excel_data.xls';
    downloadLink = this.document.createElement("a");
    this.document.body.appendChild(downloadLink);
    if(navigator.msSaveOrOpenBlob){
        var blob = new Blob(['\ufeff', tableHTML], {
            type: dataType
        });
        navigator.msSaveOrOpenBlob( blob, filename);
    }else{
        downloadLink.href = 'data:' + dataType + ', ' + tableHTML;
        downloadLink.download = filename;
        downloadLink.click();
    }
}