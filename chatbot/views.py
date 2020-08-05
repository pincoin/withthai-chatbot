import linebot
from django.conf import settings
from django.http import (
    HttpResponse, HttpResponseForbidden
)
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from linebot import models
from linebot.exceptions import InvalidSignatureError

from .models import WebhookLog

line_bot_api = linebot.LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = linebot.WebhookHandler(settings.LINE_CHANNEL_SECRET)


@method_decorator(csrf_exempt, name='dispatch')
class CallbackView(generic.View):
    def post(self, request, *args, **kwargs):
        if 'X-Line-Signature' in request.headers:
            signature = request.headers['X-Line-Signature']
            body = request.body.decode('utf-8')

            log = WebhookLog()
            log.request_header = request.headers
            log.request_body = body
            log.save()

            try:
                handler.handle(body, signature)
            except InvalidSignatureError:
                return HttpResponseForbidden()

            return HttpResponse('OK')

        return HttpResponseForbidden()


@handler.add(models.MessageEvent, message=models.TextMessage)
def handle_message(event):
    text = event.message.text

    if text == 'profile':
        if isinstance(event.source, models.SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    models.TextSendMessage(text='Display name: ' + profile.display_name),
                    models.TextSendMessage(text='Status message: ' + str(profile.status_message))
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                models.TextSendMessage(text="Bot can't use profile API without user ID"))
    elif text == 'quota':
        quota = line_bot_api.get_message_quota()
        line_bot_api.reply_message(
            event.reply_token, [
                models.TextSendMessage(text='type: ' + quota.type),
                models.TextSendMessage(text='value: ' + str(quota.value))
            ]
        )
    elif text == 'quota_consumption':
        quota_consumption = line_bot_api.get_message_quota_consumption()
        line_bot_api.reply_message(
            event.reply_token, [
                models.TextSendMessage(text='total usage: ' + str(quota_consumption.total_usage)),
            ]
        )
    elif text == 'push':
        line_bot_api.push_message(
            event.source.user_id, [
                models.TextSendMessage(text='PUSH!'),
            ]
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            models.TextSendMessage(text=text)
        )
