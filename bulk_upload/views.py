import csv

from rest_framework.generics import ListAPIView, ListCreateAPIView
from django.http.response import JsonResponse

from models.author import Author
from models.book import Book
from models.member import Member


class BooksBulkUpload(ListCreateAPIView):

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            Book.objects.create(title=row['Title'],
                                author=Author.objects.get(name=row['Author']))
        return JsonResponse({'message': 'Done!'})

    def get(self, request, *args, **kwargs):
        author = Book.objects.all().values('title', 'author')
        # print(list(author))
        return JsonResponse({'data': list(author)})


class AuthorBulkUpload(ListCreateAPIView):

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        print(request.FILES)
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            Author.objects.create(name=row['Author Name'])
        return JsonResponse({'message': 'Done!'})

    def get(self, request, *args, **kwargs):
        author = Author.objects.all().values('name', 'author_id')
        # print(list(author))
        return JsonResponse({'data': list(author)})


class MemberBulkUpload(ListCreateAPIView):

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            Member.objects.create(name=row['Member Name'])
        return JsonResponse({'message': 'Done!'})

    def get(self, request, *args, **kwargs):
        author = Member.objects.all().values('name', 'member_id')
        # print(list(author))
        return JsonResponse({'data': list(author)})


