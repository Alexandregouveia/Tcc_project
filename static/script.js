//Cria cabeçalho da tabela (True - para adicioonar a coluna ações)
function buildHeader(values,action){
    var header = "<tr> <th> # </th>";
    console.log(action)
    for (var i=1; i<values.length; i++){
        header += "<th >"+values[i]+"</th>";
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
