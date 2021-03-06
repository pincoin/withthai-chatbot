import json

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from golf import models as golf_models
from . import forms
from . import viewmixins


class SampleView(viewmixins.LiffContextMixin, generic.TemplateView):
    app_name = 'sample'

    template_name = 'liff/sample.html'

    def get_context_data(self, **kwargs):
        context = super(SampleView, self).get_context_data(**kwargs)
        context['title'] = _('Sample')
        return context


class GolfBookingCreateFormView(viewmixins.LiffContextMixin, generic.FormView):
    app_name = 'request'

    template_name = 'liff/golf_booking_create_form.html'

    form_class = forms.GolfBookingForm

    def get_form_kwargs(self):
        kwargs = super(GolfBookingCreateFormView, self).get_form_kwargs()

        kwargs['request'] = self.request
        kwargs['golf_club'] = self.golf_club

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(GolfBookingCreateFormView, self).get_context_data(**kwargs)
        context['title'] = _('New Booking')
        context['golf_club'] = self.golf_club

        cache_key = f'liff.views.GolfBookingCreateFormView.fees({self.golf_club.id})'
        cache_time = settings.CACHES['default']['TIMEOUT86400']

        fees = cache.get(cache_key)

        if not fees:
            fees = golf_models.GreenFee.objects \
                .select_related('season', 'timeslot', 'customer_group') \
                .filter(season__golf_club=self.golf_club,
                        timeslot__golf_club=self.golf_club,
                        customer_group__golf_club=self.golf_club) \
                .order_by('season__season_start',
                          'timeslot__day_of_week',
                          'timeslot__slot_start',
                          'customer_group__position')
            cache.set(cache_key, fees, cache_time)

        cache_key = f'liff.views.GolfBookingCreateFormView.holidays({self.golf_club.id})'

        holidays = cache.get(cache_key)

        if not holidays:
            holidays = golf_models.Holiday.objects \
                .filter(holiday__gte=timezone.make_aware(timezone.localtime().today()))
            cache.set(cache_key, holidays, cache_time)

        # Build JSON data
        data = {
            'golf_club': {
                'slug': self.golf_club.slug,
                'min_pax': self.golf_club.min_pax,
                'max_pax': self.golf_club.max_pax,
                'caddie_compulsory': self.golf_club.caddie_compulsory,
                'cart_compulsory': self.golf_club.cart_compulsory,
                'weekdays_min_in_advance': self.golf_club.weekdays_min_in_advance,
                'weekdays_max_in_advance': self.golf_club.weekdays_max_in_advance,
                'weekend_min_in_advance': self.golf_club.weekend_min_in_advance,
                'weekend_max_in_advance': self.golf_club.weekend_max_in_advance,
                'weekend_booking_on_monday': self.golf_club.weekend_booking_on_monday,
                'business_hour_start': self.golf_club.business_hour_start.strftime('%H:%M'),
                'business_hour_end': self.golf_club.business_hour_end.strftime('%H:%M'),
                'customer_group': self.golf_club.customer_group_id,
            },
            'fees': [],
            'holidays': [],
        }

        for fee in fees:
            data['fees'].append({
                'season_start': fee.season.season_start.strftime('%Y-%m-%d'),
                'season_end': fee.season.season_end.strftime('%Y-%m-%d'),
                'weekday': fee.timeslot.day_of_week,
                'slot_start': fee.timeslot.slot_start.strftime('%H:%M'),
                'slot_end': fee.timeslot.slot_end.strftime('%H:%M'),
                'green_fee': int(fee.selling_price),
                'caddie_fee': int(fee.season.caddie_fee_selling_price),
                'cart_fee': int(fee.season.cart_fee_selling_price),
                'customer_group': fee.customer_group_id,
            })

        for holiday in holidays:
            data['holidays'].append(holiday.holiday.strftime('%Y-%m-%d'))

        context['json'] = json.dumps(data)

        return context


class GolfBookingSettingsFormView(viewmixins.LiffContextMixin, generic.FormView):
    app_name = 'settings'

    template_name = 'liff/golf_booking_settings_form.html'

    form_class = forms.GolfBookingSettingsForm

    def get_context_data(self, **kwargs):
        context = super(GolfBookingSettingsFormView, self).get_context_data(**kwargs)

        context['title'] = _('Settings')
        context['json'] = json.dumps({
            'golf_club': {
                'slug': self.golf_club.slug,
            }
        })

        return context


class GolfPriceTableTemplateView(viewmixins.LiffContextMixin, generic.TemplateView):
    app_name = 'price'

    template_name = 'liff/golf_price_table.html'

    def get_context_data(self, **kwargs):
        context = super(GolfPriceTableTemplateView, self).get_context_data(**kwargs)

        cache_key = f'liff.views.GolfPriceTableTemplateView.green_fees({self.golf_club.id})'
        cache_time = settings.CACHES['default']['TIMEOUT86400']

        green_fees = cache.get(cache_key)

        if not green_fees:
            green_fees = golf_models.GreenFee.objects \
                .select_related('season', 'timeslot', 'customer_group') \
                .filter(season__golf_club=self.golf_club,
                        timeslot__golf_club=self.golf_club,
                        customer_group__golf_club=self.golf_club) \
                .order_by('season__season_start',
                          'timeslot__day_of_week',
                          'timeslot__slot_start',
                          'customer_group__position')
            cache.set(cache_key, green_fees, cache_time)

        cache_key = f'liff.views.GolfPriceTableTemplateView.seasons({self.golf_club.id})'

        seasons = cache.get(cache_key)

        if not seasons:
            seasons = golf_models.Season.objects \
                .filter(golf_club=self.golf_club) \
                .order_by('season_start')
            cache.set(cache_key, seasons, cache_time)

        cache_key = f'liff.views.GolfPriceTableTemplateView.timeslots({self.golf_club.id})'

        timeslots = cache.get(cache_key)

        if not timeslots:
            timeslots = golf_models.Timeslot.objects \
                .filter(golf_club=self.golf_club) \
                .order_by('day_of_week', 'slot_start')
            cache.set(cache_key, timeslots, cache_time)

        cache_key = f'liff.views.GolfPriceTableTemplateView.customer_groups({self.golf_club.id})'

        customer_groups = cache.get(cache_key)

        if not customer_groups:
            customer_groups = golf_models.CustomerGroup.objects \
                .filter(golf_club=self.golf_club) \
                .order_by('position')
            cache.set(cache_key, customer_groups, cache_time)

        price_table = {}
        for green_fee in green_fees:
            if green_fee.season_id not in price_table:
                price_table[green_fee.season_id] = {}

            if green_fee.timeslot_id not in price_table[green_fee.season_id]:
                price_table[green_fee.season_id][green_fee.timeslot_id] = {}

            price_table[green_fee.season_id][green_fee.timeslot_id][green_fee.customer_group_id] = green_fee.list_price

        context['title'] = _('Price Table')

        context['seasons'] = seasons
        context['timeslots'] = timeslots
        context['customer_groups'] = customer_groups

        context['price_table'] = price_table

        return context


class GolfScorecardTemplateView(viewmixins.LiffContextMixin, generic.TemplateView):
    app_name = 'scorecard'

    template_name = 'liff/golf_scorecard.html'

    def get_context_data(self, **kwargs):
        context = super(GolfScorecardTemplateView, self).get_context_data(**kwargs)

        context['title'] = _('Scorecard')
        context['hole'] = range(1, self.golf_club.scorecard['hole'] + 1)
        context['scorecard'] = self.golf_club.scorecard

        return context
