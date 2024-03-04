from django.contrib import admin
from reviews.models import (
    CustomUser,
    Category,
    Genre,
    Title,
    Review,
    Comment,
    GenreTitle
)

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(GenreTitle)
