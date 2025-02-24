from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from decimal import Decimal
from django.contrib.auth import authenticate, login
from django.apps import apps
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *


@login_required
def index(request):
    return render(request,'index.html')

####################################### CATEGORIA #################################################
@login_required
def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html', contexto)

@login_required
def form_categoria(request):
    if request.method == 'POST':
       form = CategoriaForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            form.save() # salva a instancia do modelo no banco de dados
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('categoria') # redireciona para a listagem
    else:# método é get, novo registro
        form = CategoriaForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'categoria/formulario.html', contexto)

@login_required
def detalhes_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    return render(request, 'categoria/detalhes.html', {'categoria': categoria})

@login_required
def editar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado!')
        return redirect('categoria')  # Redireciona para a listagem


    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save() # save retorna o objeto salvo
            messages.success(request, 'Operação realizada com Sucesso!')
            lista = []
            lista.append(categoria) 
            return render(request, 'categoria/lista.html', {'lista': lista})
    else:
         form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/formulario.html', {'form': form,})

@login_required
def excluir_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado!')
        return redirect('categoria')  # Redireciona para a listagem

    if request.method == "POST":
        categoria.delete()
        messages.success(request, 'Operação realizada com Sucesso!')
        return redirect('categoria')

    return render(request, 'categoria/confirmar_exclusao.html', {'categoria': categoria})

######################################### CLIENTE ###############################################
@login_required
def cliente(request):
    contexto = {
        'lista': Cliente.objects.all().order_by('-id'),
    }
    return render(request, 'cliente/lista.html', contexto)
@login_required
def form_cliente(request):
    if request.method == 'POST':
       form = ClienteForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            form.save() # salva a instancia do modelo no banco de dados
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('cliente') # redireciona para a listagem
    else:# método é get, novo registro
        form = ClienteForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'cliente/formulario.html', contexto)

def detalhes_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    return render(request, 'cliente/detalhes.html', {'cliente': cliente})

def editar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado!')
        return redirect('categoria')  # Redireciona para a listagem


    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save() # save retorna o objeto salvo
            messages.success(request, 'Operação realizada com Sucesso!')
            lista = []
            lista.append(cliente) 
            return render(request, 'cliente/lista.html', {'lista': lista})
    else:
         form = ClienteForm(instance=cliente)
    return render(request, 'cliente/formulario.html', {'form': form,})

@login_required
def excluir_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado!')
        return redirect('cliente')  # Redireciona para a listagem

    if request.method == "POST":
        cliente.delete()
        messages.success(request, 'Operação realizada com Sucesso!')
        return redirect('cliente')

    return render(request, 'cliente/confirmar_exclusao.html', {'cliente': cliente})

######################################### PRODUTO ###############################################
@login_required
def produto(request):
    contexto = {
        'lista': Produto.objects.all().order_by('-id'),
    }
    return render(request, 'produto/lista.html', contexto)

@login_required
def form_produto(request):
    if request.method == 'POST':
       form = ProdutoForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            form.save() # salva a instancia do modelo no banco de dados
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('produto') # redireciona para a listagem
    else:# método é get, novo registro
        form = ProdutoForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'produto/formulario.html', contexto)

@login_required
def detalhes_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'produto/detalhes.html', {'produto': produto})

@login_required
def editar_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
    except Produto.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado!')
        return redirect('produto')  # Redireciona para a listagem

    if request.method == 'POST':
        action = request.POST.get('action')  # Identifica a ação do botão clicado

        if action == 'save':  # Verifica se o botão "Salvar" foi clicado
            form = ProdutoForm(request.POST, instance=produto)
            if form.is_valid():
                produto = form.save()  # save retorna o objeto salvo
                messages.success(request, 'Operação realizada com Sucesso!')
                lista = [produto]
                return render(request, 'produto/lista.html', {'lista': lista})
        else:
            # Se outro botão foi clicado (como "Voltar"), não faz nada e redireciona
            return redirect('produto')  # Substitua 'categoria' pela URL desejada para "Voltar"
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produto/formulario.html', {'form': form})

@login_required
def excluir_produto(request, id):
    try:
        produto = Produto.objects.get(pk=id)
    except Produto.DoesNotExist:
        messages.error(request, 'Registro não encontrado!')
        return redirect('produto')  # Redireciona para a listagem

    if request.method == "POST":
        produto.delete()
        messages.success(request, 'Operação realizada com Sucesso!')
        return redirect('produto')

    return render(request, 'produto/confirmar_exclusao.html', {'produto': produto})

@login_required
def ajustar_estoque(request, id):
    produto = Produto.objects.get(pk=id)
    estoque = produto.estoque  # Pega o objeto estoque relacionado ao produto
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com sucesso!')
            return redirect('produto')  # Redireciona para a listagem de produtos
        else:
            messages.error(request, 'Erro ao ajustar o estoque. Verifique os valores inseridos.')
    else:
        form = EstoqueForm(instance=estoque)
    return render(request, 'produto/estoque.html', {'form': form})

################################ TESTE #######################################################
@login_required
def teste1(request):
    return render(request, 'testes/teste1.html')

@login_required
def teste2(request):
    return render(request, 'testes/teste2.html')

@login_required
def teste3(request):
    return render(request, 'testes/teste3.html')

@login_required
def buscar_dados(request, app_modelo):
    termo = request.GET.get('q', '') # pega o termo digitado
    try:
        # Divida o app e o modelo
        app, modelo = app_modelo.split('.')
        modelo = apps.get_model(app, modelo)
    except LookupError:
        return JsonResponse({'error': 'Modelo não encontrado'}, status=404)
    
    # Verifica se o modelo possui os campos 'nome' e 'id'
    if not hasattr(modelo, 'nome') or not hasattr(modelo, 'id'):
        return JsonResponse({'error': 'Modelo deve ter campos "id" e "nome"'}, status=400)
    
    resultados = modelo.objects.filter(nome__icontains=termo)
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)

########################################## PEDIDO ##################################################
@login_required
def pedido(request):
    lista = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': lista})

@login_required
def novo_pedido(request,id):
    if request.method == 'GET':
        try:
            cliente = Cliente.objects.get(pk=id)
        except Cliente.DoesNotExist:
            # Caso o registro não seja encontrado, exibe a mensagem de erro
            messages.error(request, 'Registro não encontrado')
            return redirect('cliente')  # Redireciona para a listagem
        # cria um novo pedido com o cliente selecionado
        pedido = Pedido(cliente=cliente)
        form = PedidoForm(instance=pedido)# cria um formulario com o novo pedido
        return render(request, 'pedido/formulario.html',{'form': form,})
    else: # se for metodo post, salva o pedido.
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            return redirect('pedido')

@login_required
def data_atual(request):
    return{
        'data_atual': datetime.now()
    }

@login_required
def detalhes_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')  # Redireciona para a listagem    
    
    if request.method == 'GET':
        itemPedido = ItemPedido(pedido=pedido)
        form = ItemPedidoForm(instance=itemPedido)
    else:  # method Post
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item_pedido = form.save(commit=False)  # commit=False permite modificações antes de salvar
            item_pedido.preco = item_pedido.produto.preco  # Acessando o preço do produto relacionado
            estoque_atual = item_pedido.produto.estoque
            
            # Verificação do estoque
            print (f'Quantidade pedido: {item_pedido.qtde}')
            print (f'Estoque: {estoque_atual.qtde}')
            if item_pedido.qtde > estoque_atual.qtde:
                messages.error(request, 'Estoque insuficiente para este produto')
            else:
                # Decrementando a quantidade do estoque
                estoque_atual.qtde = estoque_atual.qtde - item_pedido.qtde
                item_pedido.produto.estoque.qtde = estoque_atual
                item_pedido.produto.estoque.save()   # Salvando a atualização do estoque
                item_pedido.save()  # Salvando o item do pedido
                estoque_atual.save()

                messages.success(request, 'Produto adicionado com sucesso!')
                itemPedido = ItemPedido(pedido=pedido)
                form = ItemPedidoForm(instance=itemPedido)
        else:
            messages.error(request, 'Erro ao adicionar produto')


    contexto = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'pedido/detalhes.html', contexto)

@login_required
def remover_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('detalhes_pedido', id=id)
    
    pedido_id = item_pedido.pedido.id  # Armazena o ID do pedido antes de remover o item
    estoque = item_pedido.produto.estoque  # Obtém o estoque do produto
    estoque.qtde += item_pedido.qtde  # Devolve a quantidade do item ao estoque
    estoque.save()  # Salva as alterações no estoque
    # Remove o item do pedido
    item_pedido.delete()
    messages.success(request, 'Operação realizada com Sucesso')


    # Redireciona de volta para a página de detalhes do pedido
    return redirect('detalhes_pedido', id=pedido_id)

@login_required
def remover_pedido(request, id):
    try:
        pedido = Pedido.objects.get(pk=id)
        itens_pedido = ItemPedido.objects.filter(pedido=pedido)  # Obtém todos os itens do pedido

        # Devolve cada item ao estoque antes de excluir o pedido
        for item in itens_pedido:
            estoque_item = Estoque.objects.get(produto=item.produto)  # Obtém o estoque correto
            estoque_item.qtde += item.qtde  # Atualiza a quantidade no estoque
            estoque_item.save()  # Salva a atualização no banco de dados
        
        # Agora que os itens foram devolvidos ao estoque, podemos removê-los
        itens_pedido.delete()
        
        # Exclui o pedido após os itens terem sido removidos corretamente
        pedido.delete()
        
        messages.success(request, 'Exclusão realizada com sucesso.')
    except Pedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
    except Estoque.DoesNotExist:
        messages.error(request, 'Erro ao atualizar estoque. Produto não encontrado.')

    return redirect('pedido')


@login_required
def editar_item_pedido(request, id):
    try:
        item_pedido = ItemPedido.objects.get(pk=id)
    except ItemPedido.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('detalhes_pedido', id=id)

    pedido = item_pedido.pedido  # Obtém o pedido relacionado
    quantidade_anterior = item_pedido.qtde  # Armazena a quantidade anterior do item

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item_pedido)
        if form.is_valid():
            item_pedido_editado = form.save(commit=False)  # Prepara o item atualizado sem salvar ainda
            
            nova_quantidade_item = item_pedido_editado.qtde  # Nova quantidade do item
            estoque_item = Estoque.objects.get(produto=item_pedido.produto)  # Obtém o estoque do produto
            
            # Recalculando o estoque corretamente
            estoque_item.qtde += quantidade_anterior  # Devolvendo a quantidade anterior ao estoque
            if estoque_item.qtde >= nova_quantidade_item:
                estoque_item.qtde -= nova_quantidade_item  # Retirando a nova quantidade do estoque
                
                estoque_item.save()  # Salva a atualização no estoque
                item_pedido_editado.save()  # Agora salva o item atualizado
                messages.success(request, 'Operação realizada com sucesso')
            else:
                messages.error(request, 'Quantidade em estoque insuficiente para o produto.')
                return redirect('detalhes_pedido', id=pedido.id)

            return redirect('detalhes_pedido', id=pedido.id)

    else:
        form = ItemPedidoForm(instance=item_pedido)

    contexto = {
        'pedido': pedido,
        'form': form,
        'item_pedido': item_pedido,
    }
    return render(request, 'pedido/detalhes.html', contexto)

@login_required
def form_pagamento(request,id):
    try:
        pedido = Pedido.objects.get(pk=id)
    except Pedido.DoesNotExist:
        # Caso o registro não seja encontrado, exibe a mensagem de erro
        messages.error(request, 'Registro não encontrado')
        return redirect('pedido')  # Redireciona para a listagem    
    
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Operação realizada com Sucesso')

            pagamento = Pagamento(pedido=pedido)
            form = PagamentoForm(instance=pagamento)
    else: 
        pagamento = Pagamento(pedido=pedido)
        form = PagamentoForm(instance=pagamento)
        
        
    # prepara o formulário para um novo pagamento

    contexto = {
        'pedido': pedido,
        'form': form,
    }    
    return render(request, 'pedido/pagamento.html',contexto)

@login_required
def remover_pagamento(request, id):
    try:
        pagamento = Pagamento.objects.get(pk=id)
        pagamento.delete()
        messages.success(request, 'Exclusão realizda com Sucesso.')
        pagamento_id = pagamento.pedido.id
    except:
        messages.error(request, 'Registro não encontrado')
        return redirect('form_pagamento', id=pagamento_id)
    
    return redirect('form_pagamento', id=pagamento_id)

def notafiscal(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Se o pedido já contém os valores, podemos formatá-los corretamente antes de enviar para o template
    # Garantir que valores como total, impostos, etc., sejam passados corretamente como string ou formatados
    total = pedido.total
    icms = pedido.icms
    pis = pedido.pis
    ipi = pedido.ipi
    cofins = pedido.cofins
    total_impostos = pedido.impostos_totais  # Corrigido para impostos_totais
    valor_final = pedido.valor_final

    # Converter os valores de Decimal para string com o formato correto
    total_formatado = f"R$ {total:.2f}"
    icms_formatado = f"R$ {icms:.2f}"
    pis_formatado = f"R$ {pis:.2f}"
    ipi_formatado = f"R$ {ipi:.2f}"
    cofins_formatado = f"R$ {cofins:.2f}"
    total_impostos_formatado = f"R$ {total_impostos:.2f}"
    valor_final_formatado = f"R$ {valor_final:.2f}"

    if request.method == "POST":
        # Criação da Nota Fiscal
        nota_fiscal = NotaFiscal.objects.create(pedido=pedido)
        return redirect('detalhes_nota_fiscal', nota_fiscal.id)  # Corrigido o nome da variável e o redirecionamento
    
    # Passando os valores formatados para o template
    return render(request, 'notafiscal/notafiscal.html', {
        'pedido': pedido,
        'total': total_formatado,
        'icms': icms_formatado,
        'pis': pis_formatado,
        'ipi': ipi_formatado,
        'cofins': cofins_formatado,
        'total_impostos': total_impostos_formatado,
        'valor_final': valor_final_formatado,
        'chave_acesso': pedido.chave_acesso
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Tenta autenticar o usuário
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Se a autenticação for bem-sucedida, faz o login
            login(request, user)
            return redirect('home')  # Redireciona para a página inicial (ajuste conforme necessário)
        else:
            # Se a autenticação falhar, adiciona uma mensagem de erro
            messages.error(request, "Usuário ou senha inválidos.")
    
    return render(request, 'login.html')
