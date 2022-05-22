from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from ..models import TipModel


@receiver(m2m_changed, sender=TipModel)
def recalculate_points(sender, **kwargs):
    print(sender)
    print(kwargs)
