//Cria cabeçalho da tabela (True - para adicionar a coluna ações)
function buildHeader(values,action){
    var header = "<tr> <th> # </th>";
    console.log(action)
    for (var i=1; i<values.length; i++){
        header += '<th onclick="sortTable('+i+')" >'+values[i]+ '</th>';
    }
    if (action){
        header += "<th> Ações </th> </tr>";
    }else{
        header += "</tr>";
    }
    return header;
}

//Cria o resto da tabela (True - para adicioonar a coluna ações)
function buildEditTable(jsonArray,action){
    var linhas ="";
    var keys = Object.keys(jsonArray[0]);
    for (var i=0; i<jsonArray.length; i++){
        linhas += "<tr > <td>" + jsonArray[i][keys[0]] + "</td>";
        for (var j=1; j<keys.length; j++){
            linhas += "<td>" + jsonArray[i][keys[j]] + "</td>";
        }
        if (action){
            linhas += "<td><a href=/remove?file="+ jsonArray[i][keys[0]] +" > Remover </a>, <a href=/view?file="+ jsonArray[i][keys[0]] +" > visualizar </a>, Avaliar</td></tr>";
        }else{
            linhas += "</tr>";
        }
    }
    return linhas;
}

function htmlDecode(input){
    var e = document.createElement('div');
    e.innerHTML = input;
    return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
}


function del(){
    console.log(this);
}

//Função para ordenar tabela de resultados creditos: w3schools.com
function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("tabela");
    switching = true;
    // Set the sorting direction to ascending:
    dir = "asc"; 
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
      // Start by saying: no switching is done:
      switching = false;
      rows = table.rows;
      /* Loop through all table rows (except the
      first, which contains table headers): */
      for (i = 1; i < (rows.length - 1); i++) {
        // Start by saying there should be no switching:
        shouldSwitch = false;
        /* Get the two elements you want to compare,
        one from current row and one from the next: */
        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 1].getElementsByTagName("TD")[n];
        /* Check if the two rows should switch place,
        based on the direction, asc or desc: */
        if (dir == "asc") {
          if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        } else if (dir == "desc") {
          if (Number(x.innerHTML) < Number(y.innerHTML)) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
        }
      }
      if (shouldSwitch) {
        /* If a switch has been marked, make the switch
        and mark that a switch has been done: */
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
        // Each time a switch is done, increase this count by 1:
        switchcount ++; 
      } else {
        /* If no switching has been done AND the direction is "asc",
        set the direction to "desc" and run the while loop again. */
        if (switchcount == 0 && dir == "asc") {
          dir = "desc";
          switching = true;
        }
      }
    }
  }