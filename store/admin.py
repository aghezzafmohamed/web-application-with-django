from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.contrib.contenttypes.models import ContentType

from store.models import Contact, Car, Rental


class AdminURLMixin(object):
    def get_admin_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj.__class__)
        return reverse("admin:store_%s_change" % (
            content_type.model),
            args=(obj.id,))

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin, AdminURLMixin):
    list_filter = ['created_at', 'contacted']
    fields = ["created_at", "contact_link", 'car_link', 'contacted']
    readonly_fields = ["created_at", "contact_link", "car_link", "contacted"]

    def has_add_permission(self, request):
        return False

    def contact_link(self, rentaling):
        url = self.get_admin_url(rentaling.contact)
        return mark_safe("<a href='{}'>{}</a>".format(url, rentaling.contact.name))

    def car_link(self, rentaling):
        url = self.get_admin_url(rentaling.car)
        return mark_safe("<a href='{}'>{}</a>".format(url, rentaling.car.title))

class RentalInline(admin.TabularInline, AdminURLMixin):
    model = Rental
    extra = 0
    readonly_fields = ["created_at", "car_link", "contacted"]
    fields = ["created_at", "car_link", "contacted"]
    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"


    def car_link(self, rentaling):
        url = self.get_admin_url(rentaling.car)
        return mark_safe("<a href='{}'>{}</a>".format(url, rentaling.car.title))
    car_link.short_description = "Car"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inlines = [RentalInline,]

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    search_fields = ['petrol', 'title']