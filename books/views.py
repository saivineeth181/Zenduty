from datetime import datetime, timedelta, timezone

from django.http.response import JsonResponse
from django.db.models import Count
from rest_framework.generics import ListAPIView, CreateAPIView

from models.reservation import Reservation
from models.checkout import Checkout
from models.book import Book
from books.serializers import BookSerializer


class BookReservation(CreateAPIView):
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        request_data = request.data
        try:
            book_id = request_data['book_id']
            member_id = request_data['member_id']
            reservations = Reservation.objects.filter(book_id=book_id,
                                                      member_id=member_id,
                                                      allotted=0)
            if reservations.exists():
                return JsonResponse(
                    {'status': True,
                     'message': 'reservation with same book_id and member_id already exists'})
            else:
                reservation = Reservation.objects.create(book_id=book_id,
                                                         member_id=member_id)
                checkout_books = Checkout.objects.filter(book_id=book_id,
                                                         returned=0)
                book = Book.objects.get(pk=book_id)
                if checkout_books.exists():
                    if book.copies > len(checkout_books):
                        Checkout.objects.create(
                            book_id=book_id,
                            member_id=member_id)
                        reservation.allotted = 1
                        reservation.save()
                        return JsonResponse(
                            {'status': True,
                             'message': f"{book.title} is allotted to "
                                        f"{member_id}"})
                    else:
                        return JsonResponse(
                            {'status': True, 'message': "all books are "
                                                        "allotted"})
                else:
                    Checkout.objects.create(
                        book_id=book_id,
                        member_id=member_id)
                    reservation.allotted = 1
                    reservation.save()
                    return JsonResponse(
                        {'status': True,
                         'message': f"{book.title} is allotted to "
                                    f"{member_id}"})

        except Exception as error:
            return JsonResponse(
                {'status': False, 'error': str(error)})


class BooksOverdue(ListAPIView):

    def get(self, request, *args, **kwargs):
        try:
            checkout_books = Checkout.objects.filter(returned=0)
            check_date = datetime.now(timezone.utc) - timedelta(days=7)
            checkout_books = checkout_books.filter(created_at__lt=check_date)
            response = {}
            for checkout in checkout_books:
                print(checkout.member.name, response.get(checkout.member.name))
                if response.get(checkout.member.name) is None:
                    response[checkout.member.name] = (check_date - checkout.created_at).days * 50
                else:
                    response[checkout.member.name] = response[checkout.member.name] + (
                                                               check_date - checkout.created_at).days * 50
            return JsonResponse(
                {'status': True, 'data': response})
        except Exception as error:
            return JsonResponse(
                {'status': False, 'error': str(error)})


class BooksAnalytics(ListAPIView):

    def get(self, request, *args, **kwargs):
        try:
            popular_book = Reservation.objects.values('book__title').annotate(
                book_count=Count('book__title')).order_by('-book_count')[:10]
            popular_book = list(popular_book)
            checkout_books = Checkout.objects.filter(returned=1)
            checkout_sum = checkout_avg = 0
            if checkout_books.exists():
                for checkout in checkout_books:
                    checkout_sum += (checkout.updated_at - checkout.created_at).days
                checkout_avg = checkout_sum/len(checkout_books)
            active_members = Reservation.objects.values('member__name').annotate(
                member_count=Count('member__name')).order_by('-member_count')[:10]
            active_members = list(active_members)
            response = {
                'popular_book': popular_book,
                'checkout_avg': checkout_avg,
                'active_members': active_members
            }
            return JsonResponse(
                {'status': True, 'data': response})

        except Exception as error:
            return JsonResponse(
                {'status': False, 'error': str(error)})


class BookCheckout(CreateAPIView):
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        request_data = request.data
        try:
            book_id = request_data['book_id']
            member_id = request_data['member_id']
            checkout_books = Checkout.objects.filter(book_id=book_id,
                                                     member_id=member_id,
                                                     returned=0)
            if checkout_books.exists():
                checkout_books = checkout_books.first()
                checkout_books.returned = 1
                checkout_books.save()

                reservation = Reservation.objects.filter(book_id=book_id,
                                                         allotted=0).order_by('id')
                if reservation.exists():
                    reservation = reservation.first()
                    reservation.allotted = 1
                    reservation.save()
                    Checkout.objects.create(
                        book_id=book_id,
                        member_id=member_id)
                return JsonResponse(
                    {'status': True, 'message': 'Returned!'})
            else:
                return JsonResponse(
                    {'status': True, 'message': 'not Exists'})
        except Exception as error:
            return JsonResponse(
                {'status': False, 'error': str(error)})