from django.forms import ModelForm
from django import forms
from .models import *
from datetime import datetime




class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Produto'}),
            'ordem':forms.NumberInput(attrs={'class': 'inteiro form-control', 'placeholder': ''}),
        }
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome  
    
    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')
        if ordem <= 0:
            raise forms.ValidationError("O campo ordem deve ser maior que zero.")
        return ordem
    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': 'C.P.F'}),
            'datanasc': forms.DateInput(attrs={'class': 'data form-control', 'placeholder': 'Data de Nascimento'}, format='%d/%m/%Y'),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if len(cpf) < 14:
            raise forms.ValidationError("O CPF deve ter pelo menos 14 caracteres.")
        return cpf

    def clean_datanasc(self):
        datanasc = self.cleaned_data.get('datanasc')
        if datanasc:
            hoje = datetime.today().date()
            if datanasc > hoje:
                raise forms.ValidationError("A data de nascimento não pode ser no futuro.")
            idade = hoje.year - datanasc.year - ((hoje.month, hoje.day) < (datanasc.month, datanasc.day))
            if idade < 18:
                raise forms.ValidationError("O cliente deve ter pelo menos 18 anos.")
        return datanasc

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria','img_base64']
        widgets = {
            'categoria': forms.HiddenInput(),
            'nome':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'img_base64': forms.HiddenInput(), 
            # a classe money mascara a entreda de valores monetários, está em base.html
            #  jQuery Mask Plugin
            'preco':forms.TextInput(attrs={
                'class': 'money form-control',
                'maxlength': 500,
                'placeholder': '0.000,00'
            }),
        }
        
        labels = {
            'nome': 'Nome do Produto',
            'preco': 'Preço do Produto',
        }


    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['preco'].localize = True
        self.fields['preco'].widget.is_localized = True   

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto', 'qtde']

        widgets = {
            'produto': forms.HiddenInput(),
            'qtde': forms.NumberInput(attrs={
                'class': 'inteiro form-control',
                'min': 0,  # Evita valores negativos no navegador
                'placeholder': 'Digite a quantidade',
            }),
        }

    def clean_qtde(self):
        qtde = self.cleaned_data.get('qtde')
        if qtde < 0:
            raise forms.ValidationError("O valor de quantidade não pode ser negativo.")
        return qtde

class PedidoForm(forms.ModelForm):
     class Meta:
          model = Pedido
          fields = ['cliente']
          widgets = {
               'cliente': forms.HiddenInput(),
          }

class ItemPedidoForm(forms.ModelForm):
     class Meta:
          model = ItemPedido
          fields = ['pedido', 'produto', 'qtde']

          widgets = {
               'pedido': forms.HiddenInput(),
               'produto': forms.HiddenInput(),
               'qtde': forms.TextInput(attrs={'class': 'inteiro form-control',}),
          }
     
     def clean_qtde(self):
        qtde = self.cleaned_data.get('qtde')
        if not isinstance(qtde, int) or qtde < 0:
            raise forms.ValidationError('A quantidade deve ser um número inteiro positivo.')
        return qtde

class PagamentoForm(forms.ModelForm):
     class Meta:
          model = Pagamento
          fields = ['pedido', 'forma', 'valor']
          widgets = {
               'pedido': forms.HiddenInput(),
               'forma': forms.Select(attrs={'class': 'form-control'}),
               'valor': forms.TextInput(attrs={
                    'class': 'money form-control',
                    'maxlenght': '500',
                    'placeholder': '0.000,00',
            }),
         }
     
     def __init__(self, *args, **kwargs):
          super(PagamentoForm, self).__init__(*args, **kwargs)
          self.fields['valor'].localize = True 
          self.fields['valor'].widget.is_localized = True 

     
     def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        pedido = self.cleaned_data.get('pedido')

        if valor <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")

        if pedido:
            debito = pedido.debito  # Obtém o valor do débito do pedido
            if valor > debito:
                raise forms.ValidationError("O valor do pagamento não pode ser maior que o débito do pedido.")

        return valor

class NotaFiscalForm(forms.ModelForm):
    class Meta:
        model = NotaFiscal
        exclude = ['data_emissao']  # Exclui o campo do formulário
        fields = ['pedido', 'chave_acesso', 'data_emissao', 'total_pedido', 'icms', 'ipi', 'pis', 'cofins', 'impostos_totais', 'valor_final']
        widgets = {
            'chave_acesso': forms.TextInput(attrs={'readonly': 'readonly'}),
            'data_emissao': forms.TextInput(attrs={'readonly': 'readonly'}),
            'total_pedido': forms.TextInput(attrs={'readonly': 'readonly'}),
            'icms': forms.TextInput(attrs={'readonly': 'readonly'}),
            'ipi': forms.TextInput(attrs={'readonly': 'readonly'}),
            'pis': forms.TextInput(attrs={'readonly': 'readonly'}),
            'cofins': forms.TextInput(attrs={'readonly': 'readonly'}),
            'impostos_totais': forms.TextInput(attrs={'readonly': 'readonly'}),
            'valor_final': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
