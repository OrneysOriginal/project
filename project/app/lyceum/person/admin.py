from django.contrib import admin
import person


@admin.register(person.models.Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = (
        person.models.Profile.bio.field.name,
        person.models.Profile.birthday.field.name,
    )


__all__ = []
