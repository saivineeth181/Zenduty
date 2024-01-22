from django.contrib import admin

from models.author import Author
from models.book import Book
from models.member import Member
from models.checkout import Checkout
from models.reservation import Reservation


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, AuthorAdmin)
admin.site.register(Member, AuthorAdmin)
admin.site.register(Checkout, AuthorAdmin)
admin.site.register(Reservation, AuthorAdmin)
