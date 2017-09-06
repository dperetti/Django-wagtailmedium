from __future__ import absolute_import, unicode_literals

import json
import six

from django.forms import widgets
from wagtail.utils.widgets import WidgetWithScript
from wagtail.wagtailcore.rich_text import DbWhitelister
from wagtail.wagtailcore.rich_text import expand_db_html
from wagtail.wagtailcore.whitelist import attribute_rule

ALLOWED_ATTR = dict.fromkeys(
    ['border', 'cellpadding', 'cellspacing', 'style', 'width', 'colspan', 'margin-left', 'margin-right', 'height', 'class',
     'border-color', 'text-align', 'background-color', 'vertical-align', 'scope', 'font-family', 'rowspan', 'valign'],
    True)


default_attribute_rule = attribute_rule(ALLOWED_ATTR)


def build_medium_js_config(options):
    """
        The idea is to build a javascript object like this one :

        {
            "anchorPreview": false,
            extensions: {
                test: new (MediumEditor.MediumButtonFactory({"className": "test", "contentFA": "<i class=\"fa fa-code\"></i>", "tag": "span", "contentDefault": "<b>Test</b>", "name": "test"}))(),
                code: new (MediumEditor.MediumButtonFactory({"className": "code", "contentFA": "<i class=\"fa fa-code\"></i>", "tag": "code", "contentDefault": "<b>Code</b>", "name": "code"}))(),
                link: new MediumEditor.LinkButton(), linkdoc: new MediumEditor.LinkDocButton(), 'link-preview': new MediumEditor.LinkPreview()
            }
            "toolbar": {
                "buttons": ["bold", "italic", "underline", "code", "test", "link", "linkdoc", "h2", "h3", "orderedlist", "unorderedlist", "strikethrough"]
            },
        }
    """
    extensions = []
    custom_buttons = options.get('custom_buttons')
    for name, config in six.iteritems(custom_buttons):
        config.update(dict(name=name))
        extensions.append("""
            %s: new (MediumEditor.MediumButtonFactory(%s))()
        """ % (name, json.dumps(config)))
    medium_config = options.get('medium')
    buttons = medium_config.get('toolbar').get('buttons')
    has_wagtail_link_button = False
    for button in buttons:
        if button == 'link':
            extensions.append('link: new MediumEditor.LinkButton()')
            has_wagtail_link_button = True
        if button == 'linkdoc':
            extensions.append('linkdoc: new MediumEditor.LinkDocButton()')
            has_wagtail_link_button = True
        if button not in ['bold', 'italic', 'underline', 'code', 'h2', 'h3', 'orderedlist', 'unorderedlist', 'strikethrough']:
            pass
    # if the toolbar contains wagtail link buttons, we want to disable Medium's default anchorPreview because we'll be using our own
    if has_wagtail_link_button:
        medium_config['anchorPreview'] = False
        extensions.append("'link-preview': new MediumEditor.LinkPreview()")

    medium_config_string = json.dumps(medium_config)
    return "{%s, extensions: {%s}}" % (medium_config_string[1:-1], ", ".join(extensions))


# class DbWhitelister(Whitelister):
#     """
#     Modified version of wagtail's wagtail.wagtailcore.rich_text.DbWhitelister
#     """
#     has_loaded_custom_whitelist_rules = False
#
#     @classmethod
#     def clean(cls, html):
#         if not cls.has_loaded_custom_whitelist_rules:
#             for fn in hooks.get_hooks('construct_whitelister_element_rules'):
#                 cls.element_rules = cls.element_rules.copy()
#                 cls.element_rules.update(fn())
#             cls.has_loaded_custom_whitelist_rules = True
#         print html
#         return super(DbWhitelister, cls).clean(html)
#
#     @classmethod
#     def clean_tag_node(cls, doc, tag):
#         if 'data-embedtype' in tag.attrs:
#             embed_type = tag['data-embedtype']
#             # fetch the appropriate embed handler for this embedtype
#             embed_handler = get_embed_handler(embed_type)
#             embed_attrs = embed_handler.get_db_attributes(tag)
#             embed_attrs['embedtype'] = embed_type
#
#             embed_tag = doc.new_tag('embed', **embed_attrs)
#             embed_tag.can_be_empty_element = True
#             tag.replace_with(embed_tag)
#         elif tag.name == 'a' and 'data-linktype' in tag.attrs:
#             # first, whitelist the contents of this tag
#             for child in tag.contents:
#                 cls.clean_node(doc, child)
#             link_type = tag['data-linktype']
#             # use wagtail's default link handler
#             link_handler = get_link_handler(link_type)
#             link_attrs = link_handler.get_db_attributes(tag)
#
#             # amend it so our attributes can pass through
#             link_attrs['linktype'] = tag['data-linktype']
#             fragment = tag.get('data-fragment', False)
#             if fragment:
#                 link_attrs['fragment'] = tag.get('data-fragment')
#             tag.attrs.clear()
#             tag.attrs.update(**link_attrs)
#             print tag
#         else:
#             if tag.name == 'div':
#                 tag.name = 'p'
#
#             super(DbWhitelister, cls).clean_tag_node(doc, tag)


class MediumRichTextArea(WidgetWithScript, widgets.Textarea):
    """
    Cf https://github.com/torchbox/wagtail/blob/master/wagtail/wagtailadmin/rich_text.py#L15
    """

    def __init__(self, attrs=None, **kwargs):
        super(MediumRichTextArea, self).__init__(attrs)
        # Get the options from django settings provided by Wagtail.
        self.options = kwargs.get('options')  # #2frJM#

    def render(self, name, value, attrs=None):  # #NJSrc#
        if value is None:
            translated_value = None
        else:
            translated_value = expand_db_html(value, for_editor=True)
        return super(MediumRichTextArea, self).render(name, translated_value, attrs)

    # def render(self, name, value, attrs=None):
    #     translated_value = None
    #     if value is not None:
    #         # We'll find links to wagtail pages in the html.
    #         # Those links have data-linktype="page" and data-id attributes.
    #         # We'll look into the database, read the page title and embed it in the link, so
    #         # the Medium editor link preview can display it on hover.
    #         print value
    #         translated_value = expand_db_html(value, for_editor=True)
    #         print translated_value
    #         soup = BeautifulSoup(translated_value)
    #         wagtail_links = soup.find_all('a', {'data-linktype': 'page'})
    #         for link in wagtail_links:
    #             try:
    #                 link['data-fragment'] = link['fragment']
    #             except Exception:
    #                 pass
    #             try:
    #                 page = Page.objects.get(id=link['data-id'])
    #                 # Add the link as an attribute.
    #                 link['data-title'] = page.title
    #             except Exception:
    #                 pass
    #         wagtaildocs_links = soup.find_all('a', {'data-linktype': 'document'})
    #         for link in wagtaildocs_links:
    #             try:
    #                 doc = Document.objects.get(id=link['data-id'])
    #                 # Add the link as an attribute.
    #                 link['data-title'] = doc.title
    #             except Exception:
    #                 pass
    #         if soup.body.contents:
    #             translated_value = soup.body.encode('utf-8')[6:][:-7]
    #
    #     return super(MediumRichTextArea, self).render(name, translated_value, attrs)

    def render_js_init(self, id_, name, value):  # #BCbeK#
        medium_config_string = build_medium_js_config(self.options)
        return "new MediumEditor.MediumEditor({0}, {1})".format(json.dumps('#' + id_), medium_config_string)

    def value_from_datadict(self, data, files, name):  # #W7MnV#
        """
        This method is called by Wagtail when the page is saved.
        Cf https://github.com/torchbox/wagtail/blob/master/wagtail/wagtailadmin/rich_text.py#L29
        """
        original_value = super(MediumRichTextArea, self).value_from_datadict(data, files, name)

        if original_value is None:
            return None

        return DbWhitelister.clean(original_value)
