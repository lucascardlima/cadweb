from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *



def index(request):
    return render(request,'index.html')


def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html', contexto)

def form_categoria(request):
    if request.method == 'POST':
       form = CategoriaForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            form.save() # salva a instancia do modelo no banco de dados
            return redirect('categoria') # redireciona para a listagem
    else:# método é get, novo registro
        form = CategoriaForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'categoria/formulario.html', contexto)

def detalhes_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})

def editar_categoria(request, id):
    categoria = Categoria.objects.get(pk=id)
    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save() # save retorna o objeto salvo
            lista = []
            lista.append(categoria) 
            return render(request, 'categoria/lista.html', {'lista': lista})
    else:
         form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/formulario.html', {'form': form,})

def excluir_categoria(request, id):
    if request.method == "DELETE":
        try:
            # Obtém o objeto Categoria ou retorna 404 se não encontrado
            categoria = get_object_or_404(Categoria, pk=id)
            categoria.delete()  # Exclui a categoria
            return JsonResponse({'success': True}, status=200)  # Retorna resposta de sucesso
        except Exception as e:
            # Retorna erro em caso de falha
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False}, status=400)  # Caso não seja uma requisição DELETE
