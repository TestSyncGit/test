from django.contrib import admin
from django.core.signing import TimestampSigner
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from . import models


@admin.register(models.Event,
                models.Organizer,
                models.Membership,
                models.PricingRule,
                models.Product, models.Option,
                models.Coupon,
                models.BilletOption,
                models.PaymentMethod,
                models.Question,
                models.Categorie,
                models.Participant)
class BasicAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['participant__first_name', 'participant__last_name',
                     'order__client__first_name', 'order__client__last_name', 'billet__id', 'order__id']
    raw_id_fields = ("participant", "order", 'billet', 'question')
    fields = ("participant", "order", 'billet', 'question', 'value')


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email']
    list_per_page = 20


@admin.register(models.Billet)
class BilletAdmin(admin.ModelAdmin):
    search_fields = ['participants__first_name', 'participants__last_name', 'participants__email']
    list_per_page = 20


@admin.register(models.Invitation)
class InvitationAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email']
    list_per_page = 20


class BilletInline(admin.StackedInline):
    model = models.Billet
    extra = 0


class AnswerInline(admin.StackedInline):
    model = models.Answer
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'client', 'status', 'mercanet', 'created_at', 'amount']
    search_fields = ['client__first_name', 'client__last_name', 'client__email',
                     'transaction__mercanet__transactionReference']
    list_display_links = ['id']
    list_select_related = ('client',)
    list_filter = ['event', 'status']
    list_per_page = 20

    raw_id_fields = ("transaction", "client", 'coupon')
    fields = ('event', 'client', 'status', 'transaction', 'coupon')
    inlines = (BilletInline, AnswerInline)

    actions = ['send_tickets']

    def send_tickets(self, request, queryset):
        queryset = queryset.filter(status=models.Order.STATUS_VALIDATED)
        sent = 0
        for order in queryset.all():
            order.send_tickets()
            sent += 1
        if sent == 1:
            message_bit = _('1 message a  été envoyé')
        else:
            message_bit = _("%s messages ont été envoyés") % sent
        self.message_user(request, message_bit)
    send_tickets.short_description = _('Renvoyer les billets aux commandes valides')

    def billets(self, order):
        return order.billets.all()

    def mercanet(self, order):
        if order.transaction:
            return order.transaction.mercanet.transactionReference
        else:
            return ''

    def amount(self, o):
        return "{}€".format(o.amount)

    def view_on_site(self, obj):
        return reverse('ticket-print', kwargs={'id': TimestampSigner().sign(obj.id)})
