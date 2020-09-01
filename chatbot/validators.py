from django.utils import timezone

from . import utils


def validate_round_date(round_date, **kwargs):
    golf_club = kwargs['golf_club']

    holiday = utils.is_holiday(round_date)

    next_day = 0

    now = timezone.localtime()

    if golf_club.business_hour_end.hour <= now.hour < 24:
        next_day += 1

    min_date = now + timezone.timedelta(days=golf_club.weekdays_min_in_advance + next_day)

    if holiday:
        if golf_club.weekend_booking_on_monday:
            thursday = None
            if now.weekday() in [0, 1, 2]:
                # Booking day = Mon(0), Tue(1), Wed(2) -> Round day = Until Thu of NEXT week
                thursday = now + timezone.timedelta(3 - now.weekday() + 7)
            elif now.weekday() in [3, 4, 5, 6]:
                # Booking day = Thu(3), Fri(4), Sat(5), Sun(6) -> Round day Until Thu of this week
                thursday = now + timezone.timedelta(10 - now.weekday())

            if timezone.make_aware(round_date) > thursday:
                return False

        else:
            if (timezone.make_aware(round_date) < min_date
                    or timezone.make_aware(round_date) - now
                    > timezone.timedelta(days=golf_club.weekend_max_in_advance)):
                return False
    else:
        if (timezone.make_aware(round_date) < min_date
                or timezone.make_aware(round_date) - now
                > timezone.timedelta(days=golf_club.weekdays_max_in_advance)):
            return False

    return True


def validate_round_time():
    return True


def validate_pax(pax, **kwargs):
    golf_club = kwargs['golf_club']

    if golf_club.min_pax <= pax <= golf_club.max_pax:
        return True

    return False


def validate_cart(cart, **kwargs):
    golf_club = kwargs['golf_club']

    min_pax = 0

    if golf_club.cart_compulsory == 0:
        min_pax = 0
    elif golf_club.cart_compulsory == 1:
        min_pax = golf_club.min_pax
    elif golf_club.cart_compulsory > 1:
        if golf_club.cart_compulsory > 1 and golf_club.cart_compulsory > golf_club.min_pax > 1:
            min_pax = golf_club.min_pax
        else:
            min_pax = 0

    if cart > golf_club.max_pax or cart < min_pax:
        return False

    return True


def validate_customer_name():
    return True
