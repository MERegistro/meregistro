from meregistro.shortcuts import my_render
from forms import LoginForm
from authenticate import authenticate

def login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      user = authenticate(
        form.cleaned_data['tipo_documento'],
        form.cleaned_data['documento'],
        form.cleaned_data['password'],
      )
      if user:
        request.session['user'] = {
          'id': user.serializable_value('id'),
          'nombre': user.serializable_value('nombre'),
          'apellido': user.serializable_value('apellido'),
          'documento': user.serializable_value('documento'),
          'tipo_documento': user.serializable_value('tipo_documento'),
        }
        return HttpResponseRedirect('/seleccionarPerfil')
  else:
    form = LoginForm()
  return my_render(request, 'login/login.html', {'form': form})
  
