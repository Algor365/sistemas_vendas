from django.shortcuts import render,redirect, get_object_or_404
from .models import Produto,Venda,ItemVenda
from .forms import ProdutoForm,edit_produto
from decimal import Decimal

from django.contrib import messages


def vendas(request):
    if 'cupom' not in request.session:
        request.session['cupom'] = []

    cupom = request.session['cupom']
    mensagem = ''
    total = sum(Decimal(item['valor']) for item in cupom)

    if request.method == 'POST':
        if 'finalizar' in request.POST:
            if cupom:
                venda = Venda.objects.create(total=total)
                for item in cupom:
                    produto = Produto.objects.get(est=item['id'])
                    ItemVenda.objects.create(
                        venda=venda,
                        produto=produto,
                        quantidade=int(item['quantidade']),
                        valor_unitario=produto.preco_unitario
                    )
                request.session['cupom'] = []  # limpa o cupom
                mensagem = 'Venda finalizada com sucesso!'
                total = Decimal('0.00')
                cupom = []
            else:
                mensagem = 'Não há itens para finalizar.'

        elif 'limpar' in request.POST:
            request.session['cupom'] = []
            mensagem = 'Cupom limpo com sucesso!'
            total = Decimal('0.00')
            cupom = []

    elif request.method == 'GET' and 'codigo' in request.GET:
        codigo = request.GET.get('codigo')
        quantidade = request.GET.get('quantidade')

        if not quantidade or not quantidade.isdigit() or int(quantidade) <= 0:
            mensagem = 'Informe uma quantidade válida.'
        else:
            try:
                produto = Produto.objects.get(est=codigo)
                quantidade = int(quantidade)
                valor_total = quantidade * produto.preco_unitario

                item = {
                    'id': produto.est,
                    'descricao': produto.nome,
                    'quantidade': quantidade,
                    'valor': str(valor_total)
                }
                cupom.append(item)
                request.session['cupom'] = cupom
                total += valor_total

            except Produto.DoesNotExist:
                mensagem = 'Produto não encontrado.'

    return render(request, 'produtos/vendas.html', {
        'cupom': cupom,
        'total': total,
        'mensagem': mensagem
    })

def cadastrar_item(request):
    if request.method == 'POST':
        print("POST RECEBIDO:", request.POST)  # Para verificar os dados

        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        estoque = request.POST.get('estoque')

        print(f"Nome: {nome}, Preço: {preco}, Estoque: {estoque}")  # Para verificar valores recebidos

        # Verificar se algum campo está vazio
        if not nome or not preco or not estoque:
            messages.error(request, 'Preencha todos os campos.')
        else:
            try:
                # Converter preço para decimal
                preco_decimal = float(preco.replace(',', '.'))
                # Converter estoque para inteiro
                estoque_int = int(estoque)

                # Criar o produto no banco
                Produto.objects.create(nome=nome, estoque=estoque_int, preco_unitario=preco_decimal)

                messages.success(request, 'Produto cadastrado com sucesso!')
                return redirect('cadastrar_item')  # Redireciona após o sucesso

            except ValueError:
                messages.error(request, 'Preço ou estoque inválidos. Certifique-se de usar o formato correto.')

    return render(request, 'produtos/cadastrar_item.html')

def consulta(request):
    query = request.GET.get('busca', '')  # Pega o valor de 'busca' do GET
    if query:
        # Filtra produtos que correspondem ao nome ou ao código (id) do produto
        produtos = Produto.objects.filter(est__icontains=query)  # Filtra pelo nome
    else:
        produtos = Produto.objects.all()  # Se não houver busca, exibe todos os produtos

    return render(request, 'produtos/produtos_lista.html', {'produtos': produtos, 'query': query})

def editar_produto(request, produto_est):
    # Buscar o produto com base no campo 'est' (em vez de 'id')
    produto = get_object_or_404(Produto, est=produto_est)

    if request.method == 'POST':
        form = edit_produto(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')  # Substitua pela sua view de listagem
    else:
        form = edit_produto(instance=produto)

    return render(request, 'produtos/editar_produto.html', {'form': form, 'produto': produto})