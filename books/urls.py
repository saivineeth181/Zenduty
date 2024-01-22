from django.urls import path

from books.views import BookReservation, BooksOverdue, BooksAnalytics, BookCheckout
urlpatterns = [
    path('reservation/', BookReservation.as_view()),
    path('overdue/', BooksOverdue.as_view()),
    path('analytics/', BooksAnalytics.as_view()),
    path('checkout/', BookCheckout.as_view()),
]


