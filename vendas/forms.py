# vendas/forms.py

from django import forms
from .models import Produto  # substitua pelo nome correto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco_unitario']
        labels = {
            'nome': 'Nome do Produto',
            'preco_unitario': 'Preço Unitário',
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['id','nome', 'preco_unitario','estoque']  # ajuste conforme seus campos


class edit_produto(forms.ModelForm):
    class Meta:
        model=Produto
        fields =['id','est','nome']