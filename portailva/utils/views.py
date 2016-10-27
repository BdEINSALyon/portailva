from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from portailva.utils.forms import PlaceForm
from portailva.utils.models import Place


# Create your views here.
class PlaceListView(ListView):
    template_name = 'utils/place/list.html'
    model = Place

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('utils.can_admin_place'):
            raise PermissionDenied
        return super(PlaceListView, self).get(request, *args, **kwargs)


class PlaceNewView(CreateView):
    template_name = 'utils/place/new.html'
    model = Place
    form_class = PlaceForm
    success_url = reverse_lazy('place-list')


class PlaceUpdateView(UpdateView):
    template_name = 'utils/place/update.html'
    model = Place
    form_class = PlaceForm
    success_url = reverse_lazy('place-list')


class PlaceDeleteView(DeleteView):
    template_name = 'utils/place/delete.html'
    model = Place
    success_url = reverse_lazy('place-list')
