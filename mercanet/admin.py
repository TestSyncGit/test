from django.contrib import admin
from .models import *


@admin.register(TransactionRequest, MercanetToken)
class BasicAdmin(admin.ModelAdmin):
    pass


@admin.register(TransactionMercanet)
class TransactionMercanetAdmin(admin.ModelAdmin):
    search_fields = ['transactionReference']
    list_per_page = 20
