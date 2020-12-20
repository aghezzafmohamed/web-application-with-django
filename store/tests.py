from django.test import TestCase
from django.urls import reverse

from .models import Car, Contact, Rental


class IndexPageTestCase(TestCase):

    # test that index returns a 200
    # must start with `test`
    def test_index_page(self):
        # name of index view: `name="index"`
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):

    # ran before each test.
    def setUp(self):
        _ = Car.objects.create(title="Transmission Impossible")
        self.car = Car.objects.get(title='Transmission Impossible')

    # test that detail page returns a 200 if the item exists
    def test_detail_page_returns_200(self):
        car_id = self.car.id
        response = self.client.get(reverse('store:detail', args=(car_id,)))
        self.assertEqual(response.status_code, 200)

    # test that detail page returns a 404 if the items does not exist
    def test_detail_page_returns_404(self):
        car_id = self.car.id + 1
        response = self.client.get(reverse('store:detail', args=(car_id,)))
        self.assertEqual(response.status_code, 404)

class RentalPageTestCase(TestCase):

    def setUp(self):
        Contact.objects.create(name="Medo", mail="medo@live.fr", phone_number="0600000000")
        _ = Car.objects.create(title="Transmission Impossible")
        self.car = Car.objects.get(title='Transmission Impossible')
        self.contact = Contact.objects.get(name='Medo')

    # test that a new rentaling is made
    def test_new_rental_is_registered(self):
        old_rentalings = Rental.objects.count()
        car_id = self.car.id+1
        name = self.contact.name
        mail = self.contact.mail
        phone_number = self.contact.phone_number
        _ = self.client.post(reverse('store:detail', args=(car_id,)), {
            'name': name,
            'email': mail,
            'phone_number': phone_number
        })
        new_rentalings = Rental.objects.count()
        self.assertEqual(new_rentalings, old_rentalings+1)

    # test that a booking belongs to a contact
    def test_new_rental_belongs_to_a_contact(self):
        car_id = self.car.id
        name = self.contact.name
        mail =  self.contact.mail
        phone_number = self.contact.phone_number
        _ = self.client.post(reverse('store:detail', args=(car_id,)), {
            'name': name,
            'mail': mail,
            'phone_number': phone_number
        })
        booking = Rental.objects.first()
        self.assertEqual(self.contact, booking.contact)

    # test that a booking belong to an car
    def test_new_rental_belongs_to_an_car(self):
        car_id = self.car.id
        name = self.contact.name
        mail =  self.contact.mail
        phone_number = self.contact.phone_number
        _ = self.client.post(reverse('store:detail', args=(car_id,)), {
            'name': name,
            'mail': mail,
            'phone_number': phone_number
        })
        booking = Rental.objects.first()
        self.assertEqual(self.car, booking.car)

    # test that an car is not available after a booking is made
    def test_car_not_available_if_rentaled(self):
        car_id = self.car.id
        name = self.contact.name
        mail =  self.contact.mail
        phone_number = self.contact.phone_number
        _ = self.client.post(reverse('store:detail', args=(car_id,)), {
            'name': name,
            'mail': mail,
            'phone_number': phone_number
        })
        # Make the query again, otherwise `available` will still be set at `True`
        self.car.refresh_from_db()
        self.assertFalse(self.car.available)