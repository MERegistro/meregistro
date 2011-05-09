function confirmDelete(msg){
	msg = msg == null ? 'Está seguro de eliminar el registro? Esta acción no puede deshacerse.' : msg;
	return confirm(msg);
}

function seleccionarAmbito(selectorId, ambitoFieldId, ambitoFieldDescripcion, ambitoParentId, linkSeleccionado)
{
	if(linkSeleccionado)
	{
		$(ambitoFieldId).val(ambitoParentId);
		$(ambitoFieldDescripcion).html($(linkSeleccionado).text());
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
		html += "<ul><a href='#' onclick='$(\""+selectorId+"\").hide();$(\""+selectorId+"\").html(\"\")'>Aceptar</a>";
		$(selectorId).html(html);
  });
}
