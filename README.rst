=====================
Django-WagtailMedium
=====================

Wagtailmedium is a Medium Editor integration for the Wagtail CMS.

.. image:: https://raw.githubusercontent.com/dperetti/Django-wagtailmedium/master/Documentation.codestory/data/1a179310-b817-11e6-9f99-f91930e01b01.png


**Note**: A more detailed documentation is available in `.codestory <http://codestoryapp.com>`_ format, along with a sample project to fiddle with.


Install
-------
1. **Install from pip**::

    pip install django-wagtailmedium

2. **Add wagtailmedium to your apps**::

    INSTALLED_APPS = [
      ...
      'wagtailmedium',
    ]

3. **Add a wagtailmedium widget to ``WAGTAILADMIN_RICH_TEXT_EDITORS``** (implemented by wagtail, undocumented yet)
::

   WAGTAILADMIN_RICH_TEXT_EDITORS = {
        'default': {
            'WIDGET': 'wagtail.wagtailadmin.rich_text.HalloRichTextArea'
        },
        'medium': {
            'WIDGET': 'wagtailmedium.rich_text.MediumRichTextArea',
            'OPTIONS': {
                'custom_buttons': {
                    'code': {
                      'contentDefault': '<b>Code</b>',
                      'contentFA': '<i class="fa fa-code"></i>',
                      'tag': 'code',
                      'className': 'code',  # optional
                    },
                    'test': {
                        'contentDefault': '<b>Test</b>',
                        'contentFA': '<i class="fa fa-code"></i>',
                        'tag': 'span',
                        'className': 'test',  # optional
                    },
                },
                'medium': {  # https://github.com/yabwe/medium-editor#options-example
                    # 'buttonLabels': 'fontawesome',
                    'toolbar': {
                        'buttons': [  # https://github.com/yabwe/medium-editor#all-buttons
                            'bold', 'italic', 'underline',
                            'code',
                            'test',
                            'link',
                            'linkdoc',
                            'h2', 'h3', 'orderedlist', 'unorderedlist', 'strikethrough'
                        ]
                    },
                },
            },
        },
    }


4. **Register whitelister element rules**

This wagtail `hook <http://docs.wagtail.io/en/v1.7/reference/hooks.html#construct-whitelister-element-rules>`_ defines which HTML elements are allowed in rich text areas.

``wagtail_hooks.py``::

    from wagtail.wagtailcore import hooks
    from wagtail.wagtailcore.whitelist import attribute_rule, allow_without_attributes


    # http://docs.wagtail.io/en/v1.7/reference/hooks.html#construct-whitelister-element-rules
    @hooks.register('construct_whitelister_element_rules')  # #7bFcf#
    def whitelister_element_rules():
        return {
            'u': allow_without_attributes,
            'span': attribute_rule({'class': True}),
            'code': allow_without_attributes,
            'blockquote': allow_without_attributes,
        }

5. **Use wagtailmedium in a RichTextField of your model**

``models.py``::

    from wagtail.wagtailcore.models import Page, StreamField, RichTextField

    class HomePage(Page):
        # a default, Hallo editor
        hallo = RichTextField(blank=True)
        # a medium editor
        medium = RichTextField(editor='medium', blank=True)

