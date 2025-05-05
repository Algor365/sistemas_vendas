from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Produto, Venda, ItemVenda

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id','nome', 'preco_unitario')
    search_fields = ('nome',)

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'total')
    readonly_fields = ('data', 'total')

@admin.register(ItemVenda)
class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ('venda', 'produto', 'quantidade', 'valor_unitario', 'valor_total_display')

    def valor_total_display(self, obj):
        return obj.valor_total()
    valor_total_display.short_description = 'Valor Total'
