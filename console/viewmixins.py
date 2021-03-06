from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import translation

from golf import models as golf_models


class EnglishContextMixin:
    def dispatch(self, request, *args, **kwargs):
        print(self.request)
        translation.activate('en')
        self.request.LANGUAGE_CODE = 'en'
        return super(EnglishContextMixin, self).dispatch(request, *args, **kwargs)


class OrderChangeContextMixin:
    def post(self, request, *args, **kwargs):
        self.object = golf_models.GolfBookingOrder.objects \
            .select_related('customer_group', 'golf_club', 'user', 'line_user') \
            .get(order_no=self.kwargs['uuid'])

        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('console:golf-booking-order-detail',
                                            args=(self.object.golf_club.slug, self.object.order_no)))

    def get_success_url(self):
        return reverse('console:golf-booking-order-detail',
                       args=(self.object.golf_club.slug, self.object.order_no))


class PageableMixin:
    def get_context_data(self, **kwargs):
        context = super(PageableMixin, self).get_context_data(**kwargs)

        block_size = 5
        start_index = int((context['page_obj'].number - 1) / block_size) * block_size
        end_index = min(start_index + block_size, len(context['paginator'].page_range))

        context['page_range'] = context['paginator'].page_range[start_index:end_index]

        return context

    def get_paginate_by(self, queryset):
        # items per page
        return 10


class GolfClubStaffRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        # Login required
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Group required
        try:
            membership = golf_models.GolfClubStaffMembership.objects \
                .select_related('golf_club', 'user') \
                .get(user=request.user, golf_club__slug=kwargs['slug'])
        except golf_models.GolfClubStaffMembership.DoesNotExist:
            return self.handle_no_permission()

        # Permission required
        for permission in self.permission_required:
            if not hasattr(membership, permission):
                return self.handle_no_permission()

            if not getattr(membership, permission):
                return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
