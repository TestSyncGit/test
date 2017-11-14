from django.conf.urls import url, include
from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()
router.register(r'events', views.EventsViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include('rest_framework.urls', namespace='rest_framework')),
    url(r'products/list/(?P<event>[0-9]+)',views.products_list, name="product-list"),
    url(r'products/(?P<id>[0-9]+)',views.products_by_id,name="product-by-id"),
    url(r'options/list_by_product/(?P<product_id>[0-9]+)',views.option_by_product,name="option-by-product"),
    url(r'products/can_buy_one_more/(?P<product_id>[0-9]+)',views.canBuyOneMore,name="can-buy-one"),
]
