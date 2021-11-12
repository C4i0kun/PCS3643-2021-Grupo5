from django.contrib import admin
from catalogo.models import CustomUser, Lote, Leilao, Lance

admin.site.register(Lote)
admin.site.register(Leilao)
admin.site.register(Lance)
admin.site.register(CustomUser)