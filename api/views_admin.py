# This file contains routes only allowed for a membership user
# Permission must be ensure by link between an organization and a user
# User and Organization is a One to Many relationship. A user can have only one organization.
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDay
from rest_framework.pagination import PageNumberPagination

from .utils.serializers import CustomSerializerViewSet
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from api import permissions
from api.serializers import admin as serializers
from api.models import Event, Organizer, Invitation, Billet, Order, Product, Question, Answer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer
    permission_classes = [permissions.IsEventManager]

    def get_queryset(self):
        return (Event.objects.filter(organizer__membership__user=self.request.user) |
                Event.objects.filter(membership__user=self.request.user))

    @detail_route(methods=['get'])
    def products(self, *args, **kargs):
        return Response(
            serializers.ProductSerializer(Product.objects.filter(event=self.get_object()), many=True).data
        )


class OrganizerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.OrganizerSerializer
    permission_classes = [permissions.IsEventManager]

    def get_queryset(self):
        return Organizer.objects.filter(membership__user=self.request.user)


class InvitationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InvitationSerializer
    permission_classes = [permissions.InvitationPermission]

    def get_queryset(self):
        return Invitation.objects.filter(event__organizer__membership__user=self.request.user) | \
               Invitation.objects.filter(event__membership__user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        if type(serializer) is serializers.InvitationSerializer:
            serializer.fields['event_id'].queryset = (
                    Event.objects.filter(organizer__membership__user=self.request.user) |
                    Event.objects.filter(membership__user=self.request.user))
        return serializer


class BilletsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BilletSerializer
    permission_classes = [permissions.IsEventManager]

    def get_queryset(self):
        base = Billet.objects.filter(
            order__event__organizer__membership__user=self.request.user) | Billet.objects.filter(
            order__event__membership__user=self.request.user)
        if 'status' in self.request.GET:
            status = self.request.GET.get('status', '')
            base = base.filter(order__in=Order.accountable_orders())
            if status == 'accountable':
                pass
            elif status == 'validated':
                base = base.filter(order__in=Order.objects.filter(status=Order.STATUS_VALIDATED))
        if 'event' in self.request.GET:
            event = self.request.GET.get('event', '')
            event = self.allowed_events().get(id=event)
            base = base.filter(order__event=event)
        if 'products' in self.request.GET:
            products = self.products_for_order()
            base = base.filter(product__in=products)
        return base

    def products_for_order(self):
        return Product.objects.filter(event=self.allowed_events(),
                                      id__in=self.request.GET.get('products', '').split(','))

    def allowed_events(self):
        return (Event.objects.filter(organizer__membership__user=self.request.user) |
                Event.objects.filter(membership__user=self.request.user))

    @list_route(methods=['get'])
    def countSeatsByDay(self, *args):
        count = (self.get_queryset()
            .annotate(day=TruncDay('order__created_at'))
            .values('day').annotate(total=Sum('product__seats'))
            )
        return Response({
            'counts': count,
            'products': serializers.ProductSerializer(self.products_for_order().all(), many=True).data
        })

    @list_route(methods=['get'])
    def countByDay(self, *args):
        count = (self.get_queryset()
            .annotate(day=TruncDay('order__created_at'))
            .values('day').annotate(total=Count('id'))
            )
        return Response({
            'counts': count,
            'products': serializers.ProductSerializer(self.products_for_order().all(), many=True).data
        })

    @list_route(methods=['get'])
    def count(self, *args):
        count = (self.get_queryset().aggregate(total=Count('id')))
        return Response({
            'counts': count,
            'products': serializers.ProductSerializer(self.products_for_order().all(), many=True).data
        })

    @list_route(methods=['get'])
    def countSeats(self, *args):
        count = (self.get_queryset().aggregate(total=Sum('product__seats')))
        return Response({
            'counts': count,
            'products': serializers.ProductSerializer(self.products_for_order().all(), many=True).data
        })


class OrdersSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrdersViewSet(CustomSerializerViewSet, viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    custom_serializer_classes = {
        'list': serializers.OrdersListSerializer
    }
    pagination_class = OrdersSetPagination
    permission_classes = [permissions.IsEventManager]

    def get_queryset(self):
        base = Order.objects.filter(
            event__organizer__membership__user=self.request.user) | Order.objects.filter(
            event__membership__user=self.request.user)
        if 'status' in self.request.GET:
            status = self.request.GET.get('status', '')
            if status == 'accountable':
                base = base.filter(id__in=Order.accountable_orders())
            elif status == 'validated':
                base = base.filter(status=Order.STATUS_VALIDATED)
            elif status == 'any':
                base = base
        else:
            if self.action == 'list':
                base = base.filter(status=Order.STATUS_VALIDATED)
        if 'search' in self.request.GET:
            search = self.request.GET.get('search', '').split(' ')
            for word in search:
                base = base.filter(Q(client__first_name__icontains=word) |
                                   Q(client__last_name__icontains=word) |
                                   Q(client__email__icontains=word) |
                                   Q(transaction__mercanet__transactionReference=word))
        base = base.order_by('created_at').reverse()
        return base

    def products_for_order(self):
        return Product.objects.filter(event=self.allowed_events(),
                                      id__in=self.request.GET.get('products', '').split(','))

    def allowed_events(self):
        return (Event.objects.filter(organizer__membership__user=self.request.user) |
                Event.objects.filter(membership__user=self.request.user))


class QuestionsViewSet(CustomSerializerViewSet, viewsets.ModelViewSet):
    serializer_class = serializers.QuestionSerializer
    custom_serializer_classes = {
        'list': serializers.QuestionSerializer
    }
    pagination_class = OrdersSetPagination
    permission_classes = [permissions.IsEventManager]

    def get_queryset(self):
        base = Question.objects.filter(id__in=Question.objects.filter(
            Q(option__event__organizer__membership__user=self.request.user) |
            Q(product__event__organizer__membership__user=self.request.user) |
            Q(option__event__membership__user=self.request.user) |
            Q(product__event__membership__user=self.request.user)))
        return base


class AnswersViewSet(CustomSerializerViewSet, viewsets.ModelViewSet):
    serializer_class = serializers.AnswerSerializer
    custom_serializer_classes = {
        'list': serializers.AnswerSerializer
    }
    permission_classes = [permissions.IsEventManager]

    def get_queryset(self):
        base = Answer.objects.filter(question__in=Question.objects.filter(
            Q(option__event__organizer__membership__user=self.request.user) |
            Q(product__event__organizer__membership__user=self.request.user) |
            Q(option__event__membership__user=self.request.user) |
            Q(product__event__membership__user=self.request.user)))
        if 'question' in self.request.GET:
            question = self.request.GET.get('question', '')
            base = base.filter(question=question)
        if 'status' in self.request.GET:
            status = self.request.GET.get('status', '')
            if status == 'accountable':
                base = base.filter(order__in=Order.accountable_orders())
            elif status == 'validated':
                base = base.filter(order__status=Order.STATUS_VALIDATED)
            elif status == 'any':
                base = base
        else:
            if self.action == 'list':
                base = base.filter(order__status=Order.STATUS_VALIDATED)
        return base
