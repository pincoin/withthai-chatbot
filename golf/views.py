from django.http import JsonResponse
from django.views import generic

from . import models
from .utils import get_profile


class GolfClubFeeJson(generic.TemplateView):
    def render_to_response(self, context, **response_kwargs):
        data = {
            'club': {},
            'rates': [],
            'holidays': [],
        }

        return JsonResponse(
            data,
            json_dumps_params={'ensure_ascii': False},
            **response_kwargs
        )


class GolfClubScorecardJson(generic.TemplateView):
    def render_to_response(self, context, **response_kwargs):
        data = {
        }

        return JsonResponse(
            data,
            json_dumps_params={'ensure_ascii': False},
            **response_kwargs
        )


class GolfClubLineUser(generic.TemplateView):
    def render_to_response(self, context, **response_kwargs):
        profile = get_profile(self.request.GET['access_token'])

        data = {}

        if profile:
            try:
                membership = models.LineUserMembership \
                    .objects.get(line_user__line_user_id=profile['userId'],
                                 customer_group__golf_club__slug=self.kwargs['slug'])
                data = {
                    'customer_group_id': membership.customer_group_id,
                    'customer_group_title_english': membership.customer_group.title_english,
                    'fullname': membership.line_user.fullname,
                    'phone': membership.line_user.phone,
                    'email': membership.line_user.email,
                    'lang': membership.line_user.lang,
                }
            except models.LineUserMembership.DoesNotExist:
                pass

        return JsonResponse(
            data,
            json_dumps_params={'ensure_ascii': False},
            **response_kwargs
        )
