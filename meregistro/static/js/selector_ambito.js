
function actualizarAmbito(idx)
{

  if($("#ambito" + idx).val() == "")
  {
    $("#ambito_div_"+(idx+1)).html("");
    $("#ambito").val(idx > 0 ? $("#ambito" + (idx-1)).val() : "");
    return;
  }
  $("#ambito").val($("#ambito" + idx).val());
  url = "/seguridad/ambito/selector?parent="+$("#ambito").val();

  $.get(url, function(data) {
    ambitos = eval(data);
    html = "<select onchange='actualizarAmbito("+(idx+1)+")' name='ambito"+(idx+1)+"' id='ambito"+(idx+1)+"'><option value=''>Seleccione...</option>";
    for(i = 0; i < ambitos.length; i++)
    {
      html += "<option value='"+ambitos[i].id+"'>" + ambitos[i].descripcion + "</option>";
    }
    html += "</select><div id='ambito_div_"+(idx+2)+"' style='margin-left: 0px;'></div>";

    $("#ambito_div_"+(idx+1)).html(html);
  });
}

$(document).ready(function () {
    url = "/seguridad/ambito/selector";
    $.get(url, function(data) {
    ambitos = eval(data);
    html = "<select onchange='actualizarAmbito(0)' name='ambito0' id='ambito0'><option value=''>Seleccione...</option>";
    for(i = 0; i < ambitos.length; i++)
    {
	    html += "<option value='"+ambitos[i].id+"'>" + ambitos[i].descripcion + "</option>";
    }
    html += "</select><div id='ambito_div_1' style='margin-left: 170px;'></div>";

    $("#ambito_div_0").html(html);
    });
});
