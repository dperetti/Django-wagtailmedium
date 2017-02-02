from __future__ import absolute_import, unicode_literals

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel

from django.db.models.signals import post_save
from django.dispatch import receiver

import logging
logger = logging.getLogger('medium_dev')  # #QldS5#


class HomePage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph_hallo', blocks.RichTextBlock()),
        ('paragraph_medium', blocks.RichTextBlock(editor='medium')),
    ], blank=True)
    hallo = RichTextField(blank=True)
    medium = RichTextField(editor='medium', blank=True)  # #sPKlq#


HomePage.content_panels = [
    FieldPanel('title'),
    FieldPanel('medium'),
    FieldPanel('hallo'),
    StreamFieldPanel('body'),
]


@receiver(post_save, sender=HomePage, dispatch_uid="just_test")
def test(sender, instance, **kwargs):
    logger.debug("Saved into %s, medium field:\n%s" % (instance, instance.medium))  # #rTJqG#
