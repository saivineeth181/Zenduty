from django.urls import path

from bulk_upload.views import (BooksBulkUpload, AuthorBulkUpload,
                               MemberBulkUpload)
urlpatterns = [
    path('book/', BooksBulkUpload.as_view()),
    path('author/', AuthorBulkUpload.as_view()),
    path('member/', MemberBulkUpload.as_view()),
]


