from django.contrib import admin
from django.core.signing import TimestampSigner
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from . import models


@admin.register(models.Event,
                models.Organizer,
                models.Membership,
                models.PricingRule,
                models.Product, models.Option,
                models.Coupon,
                models.InvitationGrant,
                models.PaymentMethod,
                models.Question,
                models.Categorie,
                models.Participant)
class BasicAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BilletOption)
class BilletOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'participant', 'billet', 'option', 'amount']
    search_fields = ['participant__first_name', 'participant__last_name',
                     'billet__order__client__first_name', 'billet__order__client__last_name', 'billet__id', 'billet__order__id']
    raw_id_fields = ("participant", 'billet', 'option')
    fields = ("participant", 'billet', 'option', 'amount')
    list_filter = ['billet__order__event__name', 'option__name']
    list_per_page = 20

    def get_queryset(self, request):
        qs = super(BilletOptionAdmin, self).get_queryset(request)
        return qs.filter(Q(billet__order__id=None) | Q(billet__order__status=models.Order.STATUS_VALIDATED))


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'participant', 'billet', 'question']
    search_fields = ['participant__first_name', 'participant__last_name',
                     'order__client__first_name', 'order__client__last_name', 'billet__id', 'order__id']
    raw_id_fields = ("participant", "order", 'billet', 'question')
    fields = ("participant", "order", 'billet', 'question', 'value')
    list_filter = ['order__event__name', 'question__question']
    list_per_page = 20

    def get_queryset(self, request):
        qs = super(AnswerAdmin, self).get_queryset(request)
        return qs.filter(Q(order__id=None) | Q(order__status=models.Order.STATUS_VALIDATED))


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email']
    list_per_page = 20


class ParticipantInline(admin.StackedInline):
    model = models.Participant

    def get_max_num(self, request, obj=None, **kwargs):
        if obj is None:
            return None
        if obj.product is None:
            return 0
        return obj.product.seats


class BilletOptionInline(admin.StackedInline):
    model = models.BilletOption
    raw_id_fields = ("option", "participant")
    extra = 0


@admin.register(models.Billet)
class BilletAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'participants', 'mercanet', 'product']
    search_fields = ['participants__first_name', 'participants__last_name', 'participants__email']
    raw_id_fields = ('order', 'product')
    list_filter = ['canceled', 'order__event__name', 'order__status', 'product__name']
    inlines = (BilletOptionInline, ParticipantInline)
    list_per_page = 20

    def participants(self, billet):
        p = []
        for participant in billet.participants.all():
            p.append(str(participant))
        return ' # '.join(p)

    def mercanet(self, billet):
        if billet.order.transaction:
            return billet.order.transaction.mercanet.transactionReference
        else:
            return ''


class InvitationGrantInline(admin.StackedInline):
    model = models.InvitationGrant
    extra = 3


@admin.register(models.Invitation)
class InvitationAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email']
    raw_id_fields = ('client',)
    inlines = (InvitationGrantInline,)
    list_per_page = 20


class BilletInline(admin.StackedInline):
    model = models.Billet
    extra = 0

    def admin_link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                              instance._meta.module_name),
                      args=(instance.id,))
        return format_html(u'<a href="{}">Edit: {}</a>', url, instance.title)

    def participants(self, billet):
        p = []
        for participant in billet.participants.all():
            p.append(str(participant))
        return ' # '.join(p)

    def options_by(self, billet):
        p = []
        for o in billet.billet_options.all():
            p.append('{} x{}'.format(str(o.option.name), o.amount))
        return ' # '.join(p)
    options_by.verbose_name = 'Options'

    readonly_fields = ('participants', 'options_by')


class AnswerInline(admin.StackedInline):
    model = models.Answer
    raw_id_fields = ("participant", "order", 'billet', 'question')
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'client', 'status', 'mercanet', 'created_at', 'amount']
    search_fields = ['client__first_name', 'client__last_name', 'client__email',
                     'transaction__mercanet__transactionReference']
    list_display_links = ['id']
    list_select_related = ('client',)
    list_filter = ['event__name', 'status']
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
