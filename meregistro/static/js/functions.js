function confirmDelete(msg){
	msg = msg == null ? 'Está seguro de eliminar el registro? Esta acción no puede deshacerse.' : msg;
	return confirm(msg);
}
