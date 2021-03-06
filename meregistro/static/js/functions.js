function confirmDelete(msg){
	msg = msg == null ? 'Está seguro de eliminar el registro? Esta acción no puede deshacerse.' : msg;
	return confirm(msg);
}

ambitosStack = Array();
linksStack = Array();

function seleccionarAmbito(selectorId, ambitoFieldId, ambitoFieldDescripcion, ambitoParentId, linkSeleccionado)
{
	if(linkSeleccionado)
	{
		$(ambitoFieldId).val(ambitoParentId);
		$(ambitoFieldDescripcion).html($(linkSeleccionado).text());
        ambitosStack.push(ambitoParentId)
        linksStack.push(linkSeleccionado);
	}
    if(!ambitoParentId)
    {
        ambitosStack = Array();
    }

	$(selectorId).show();
	url = "/seguridad/ambito/selector";
	if(ambitoParentId)
		url += "?parent=" + ambitoParentId;

	$.get(url, function(data) {
  	ambitos = eval(data);
		html = "";
		if(linkSeleccionado)
			html += "<b>" + $(linkSeleccionado).text() + "</b>";
		html += "<ul>";
		for(i = 0; i < ambitos.length; i++)
		{
			html += "<li><a href='#' onclick='seleccionarAmbito(\""+selectorId+"\", \""+ambitoFieldId+"\", \""+ambitoFieldDescripcion+"\", "+ambitos[i].id+", this); return false;'>" + ambitos[i].descripcion + "</a></li>";
		}
        if(ambitosStack.length > 0)
        {
    		html += "<ul><a href='#' onclick='seleccionarAmbitoVolver(\""+selectorId+"\", \""+ambitoFieldId+"\", \""+ambitoFieldDescripcion+"\");'>Volver</a>";
        }
		html += "<ul><a href='#' onclick='$(\""+selectorId+"\").hide();$(\""+selectorId+"\").html(\"\")'>Aceptar</a>";
		$(selectorId).html(html);
  });
}

function seleccionarAmbitoVolver(selectorId, ambitoFieldId, ambitoFieldDescripcion)
{
    // Popear el actual

    ambitosStack.pop();
    linksStack.pop();

    // En head del stack esta el parent a usar
    if(ambitosStack.length > 0)
    {
        parent = ambitosStack.pop();
        lnk = linksStack.pop();
        //ambitosStack.push(parent);
        //linksStack.push(lnk);
        seleccionarAmbito(selectorId, ambitoFieldId, ambitoFieldDescripcion, parent, lnk);
		$(ambitoFieldId).val(parent);
		$(ambitoFieldDescripcion).html($(linkSeleccionado).text());
    }
    else
    {
        seleccionarAmbito(selectorId, ambitoFieldId, ambitoFieldDescripcion);
		$(ambitoFieldId).val(0);
		$(ambitoFieldDescripcion).html("");
    }
    
}

// http://www.netlobo.com/url_query_string_javascript.html
function get_url_param(name){
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.href);
    if(results == null){
	return "";
    } else {
	return results[1];
    }
}


// Verificacion de datos de Unidades Educativas
function establecimientoVerificarDato(id, dato, verificado)
{
    $.ajax({
      url: "/registro/ajax/verificar_dato_establecimiento/"+id,
      data: "dato="+dato+"&verificado="+verificado
    });
}

function anexoVerificarDato(id, dato, verificado)
{
    $.ajax({
      url: "/registro/ajax/verificar_dato_anexo/"+id,
      data: "dato="+dato+"&verificado="+verificado
    });
}

function extensionAulicaVerificarDato(id, dato, verificado)
{
    $.ajax({
      url: "/registro/ajax/verificar_dato_extension_aulica/"+id,
      data: "dato="+dato+"&verificado="+verificado
    });
}
