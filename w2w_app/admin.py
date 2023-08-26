from django.contrib import admin

from .models import Person, Genre, Platform, Movie, RatingComment


# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Person, PersonAdmin)
admin.site.register(Genre, PersonAdmin)
admin.site.register(Platform, PersonAdmin)
admin.site.register(Movie, PersonAdmin)
admin.site.register(RatingComment, PersonAdmin)
