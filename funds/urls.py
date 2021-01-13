from django.urls import path, include
from rest_framework.routers import DefaultRouter
from funds import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'accounts', views.AccountsViewset)
router.register(r'categories', views.CategoriesViewset)
router.register(r'postings', views.PostingsViewset)
router.register(r'transactions', views.TransactionsViewset)
router.register(r'budgets', views.BudgetsViewset)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
