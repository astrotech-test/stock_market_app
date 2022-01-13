from django.contrib import admin
from .models import Queries, Stocks
from import_export.admin import ExportActionMixin

# Register your models here.
class QueriesAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'security_code', 'security_name', 'close', 'market_cap', 'query', 'stock_id')

admin.site.register(Queries, QueriesAdmin)
