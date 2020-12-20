from django.shortcuts import render, get_object_or_404
from .models import Car, Rental, Contact
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError
from .forms import ContactForm, ParagraphErrorList

def index(request):
    cars = Car.objects.filter(available=True).order_by('-created_at')[:12]
    context = {
        'cars': cars
    }
    return render(request, 'store/index.html', context)


def listing(request):
    cars_list = Car.objects.filter(available=True)
    paginator = Paginator(cars_list, 9)
    page = request.GET.get('page')
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)
    context = {
        'cars': cars,
        'paginate': True
    }
    return render(request, 'store/listing.html', context)


@transaction.atomic
def detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    context = {
        'car_title': car.title,
        'car_id': car.id,
        'thumbnail': car.picture,
        'car_petrol': car.petrol,
        'car_KM': car.KM
    }
    if request.method == 'POST':
        form = ContactForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            mail = form.cleaned_data['mail']
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']

            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(mail=mail)
                    if not contact.exists():
                        # If a contact is not registered, create a new one.
                        contact = Contact.objects.create(
                            mail=mail,
                            name=name,
                            phone_number=phone_number
                        )
                    else:
                        contact = contact.first()

                    car = get_object_or_404(Car, id=car_id)
                    rental = Rental.objects.create(
                        contact=contact,
                        car=car
                    )
                    car.available = False
                    car.save()
                    context = {
                        'car_title': car.title
                    }
                    return render(request, 'store/thanks.html', context)
            except IntegrityError:
                form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requête."
    else:
        form = ContactForm()

    context['form'] = form
    context['errors'] = form.errors.items()
    return render(request, 'store/detail.html', context)


def search(request):
    query = request.GET.get('query')
    if not query:
        cars = Car.objects.all()
    else:
        # title contains the query is and query is not sensitive to case.
        cars = Car.objects.filter(title__icontains=query)
    if not cars.exists():
        cars = Car.objects.filter(petrol__icontains=query)
    title = "Résultats pour la requête %s"%query
    context = {
        'cars': cars,
        'title': title
    }
    return render(request, 'store/search.html', context)


def contact(request):
    return render(request, 'store/contact.html')


def about(request):
    return render(request, 'store/about.html')















