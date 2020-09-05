from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import generic

from golf import models as golf_models
from . import forms
from . import viewmixins


class HomeView(generic.TemplateView):
    template_name = 'console/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context


class GolfBookingOrderListView(viewmixins.EnglishContextMixin, generic.ListView):
    template_name = 'console/golf_booking_order_list.html'

    context_object_name = 'orders'

    def get_queryset(self):
        queryset = golf_models.GolfBookingOrder.objects \
            .select_related('customer_group') \
            .filter(golf_club__slug=self.kwargs['slug'])

        if 'order_status' in self.request.GET and self.request.GET['order_status']:
            if self.request.GET['order_status'].strip() == 'open':
                queryset = queryset \
                    .filter(order_status=golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open)
            elif self.request.GET['order_status'].strip() == 'accepted':
                queryset = queryset \
                    .filter(order_status=golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.accepted)

        if 'payment_status' in self.request.GET and self.request.GET['payment_status']:
            if self.request.GET['payment_status'].strip() == 'unpaid':
                queryset = queryset \
                    .filter(payment_status=golf_models.GolfBookingOrder.PAYMENT_STATUS_CHOICES.unpaid)
            elif self.request.GET['payment_status'].strip() == 'refund_requests':
                queryset = queryset \
                    .filter(payment_status=golf_models.GolfBookingOrder.PAYMENT_STATUS_CHOICES.refund_requests)

        if 'day' in self.request.GET and self.request.GET['day']:
            if self.request.GET['day'].strip() == 'today':
                queryset = queryset \
                    .filter(round_date=timezone.datetime.today())
            elif self.request.GET['day'].strip() == 'tomorrow':
                queryset = queryset \
                    .filter(round_date=timezone.datetime.today() + timezone.timedelta(days=1))

        return queryset.order_by('-round_date', 'round_time')

    def get_context_data(self, **kwargs):
        context = super(GolfBookingOrderListView, self).get_context_data(**kwargs)

        block_size = 5
        start_index = int((context['page_obj'].number - 1) / block_size) * block_size
        end_index = min(start_index + block_size, len(context['paginator'].page_range))

        context['slug'] = self.kwargs['slug']

        context['page_range'] = context['paginator'].page_range[start_index:end_index]

        return context

    def get_paginate_by(self, queryset):
        # items per page
        return 10


class GolfBookingOrderDetailView(viewmixins.EnglishContextMixin, generic.DetailView):
    template_name = 'console/golf_booking_order_detail.html'

    context_object_name = 'order'

    confirm_form_class = forms.ConfirmForm
    offer_form_class = forms.OfferForm
    reject_form_class = forms.RejectForm

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = golf_models.GolfBookingOrder.objects \
            .select_related('customer_group', 'golf_club') \
            .filter(order_no=self.kwargs['uuid'])

        return get_object_or_404(queryset, order_no=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(GolfBookingOrderDetailView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']

        context['confirm_form'] = self.confirm_form_class()
        context['offer_form'] = self.offer_form_class()
        context['reject_form'] = self.reject_form_class()
        return context


class GolfBookingOrderConfirmView(viewmixins.OrderChangeContextMixin, generic.FormView):
    form_class = forms.ConfirmForm

    def __init__(self):
        super(GolfBookingOrderConfirmView, self).__init__()
        self.object = None

    def form_valid(self, form):
        if self.object.order_status in [golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open,
                                        golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.accepted]:
            self.object.round_time = form.cleaned_data['round_time']
            self.object.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.confirmed
            self.object.save()

        return super(GolfBookingOrderConfirmView, self).form_valid(form)


class GolfBookingOrderOfferView(viewmixins.OrderChangeContextMixin, generic.FormView):
    form_class = forms.OfferForm

    def __init__(self):
        super(GolfBookingOrderOfferView, self).__init__()
        self.object = None

    def form_valid(self, form):
        print(form.cleaned_data)
        print(form.cleaned_data['tee_off_times'])

        if self.object.order_status in [golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open, ]:
            self.object.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.offered
            self.object.save()

        return super(GolfBookingOrderOfferView, self).form_valid(form)


class GolfBookingOrderRejectView(viewmixins.OrderChangeContextMixin, generic.FormView):
    form_class = forms.RejectForm

    def __init__(self):
        super(GolfBookingOrderRejectView, self).__init__()
        self.object = None

    def form_valid(self, form):
        if self.object.order_status in [golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.open, ]:
            self.object.order_status = golf_models.GolfBookingOrder.ORDER_STATUS_CHOICES.closed
            self.object.save()

        return super(GolfBookingOrderRejectView, self).form_valid(form)
