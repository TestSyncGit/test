from django.core.mail import EmailMultiAlternatives
from django.core.signing import TimestampSigner
from django.template.loader import get_template

from django.conf import settings
from django.urls import reverse


class InvitationEmail(EmailMultiAlternatives):

    def __init__(self, invitation, **kwargs):
        """

        :param invitation:Invitation
        :param kwargs:
        """
        self.invitation = invitation
        super().__init__("Invitation pour l'évènement {}".format(invitation.event.name), self.generate_text(), **kwargs)
        self.attach_alternative(self.generate_html(), 'text/html')

    def generate_text(self):
        return get_template('mail/invitation/text.txt').render(self.get_context())

    def generate_html(self):
        return get_template('mail/invitation/html.html').render(self.get_context())

    def get_context(self):
        return {
            'invitation': self.invitation,
            'link': "{}/invitation/{}".format(settings.BILLEVENT['FRONTEND_URL'], self.invitation.token)
        }


class TicketsEmail(EmailMultiAlternatives):
    def __init__(self, order, request=None, **kwargs):
        self.order = order
        self.request = request
        super().__init__("Billets pour l'évènement {}".format(order.event.name), self.generate_text(), **kwargs)
        self.attach_alternative(self.generate_html(), 'text/html')

    def generate_text(self):
        return get_template('mail/tickets/text.txt').render(self.get_context())

    def generate_html(self):
        return get_template('mail/tickets/html.html').render(self.get_context())

    def get_context(self):
        location = reverse('ticket-print', kwargs={'id': TimestampSigner().sign(self.order.id)})
        if self.request:
            link = self.request.build_absolute_uri(location)
        else:
            link = settings.BILLEVENT['API_URL'] + location
        return {
            'order': self.order,
            'link': link
        }
