from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from saleboxdjango.models import Analytic


class Command(BaseCommand):
    def handle(self, *args, **options):
        cutoff = now() - timedelta(days=7)
        Analytic.objects.filter(last_seen__lt=cutoff).delete()
