from __future__ import absolute_import, unicode_literals

from django.utils.html import escape, format_html_join
from django.templatetags.static import static
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Page
from wagtail.wagtaildocs.models import get_document_model


@hooks.register('insert_editor_js')  # #6V2Vv#
def insert_editor_js():
    js_files = [
        'wagtailmedium/wagtailmedium.js',
    ]
    js_includes = format_html_join(
        '\n',
        '<script src="{0}"></script>',
        ((static(filename),) for filename in js_files)
    )
    return js_includes


class MediumPageLinkHandler(object):
    """
    Taken from : https://github.com/torchbox/wagtail/blob/c6666c6de5e83bf94d18324858c121e6584ba47d/wagtail/wagtailcore/rich_text.py#L21

    PageLinkHandler will be invoked whenever we encounter an <a> element in HTML content
    with an attribute of data-linktype="page". The resulting element in the database
    representation will be:
    <a linktype="page" id="42">hello world</a>
    """
    @staticmethod
    def get_db_attributes(tag):  # #CGfgq#
        """
        Given an <a> tag that we've identified as a page link embed (because it has a
        data-linktype="page" attribute), return a dict of the attributes we should
        have on the resulting <a linktype="page"> element.
        """
        attrs = {'id': tag['data-id']}
        fragment = tag.get('data-fragment')
        if fragment is not None:
            attrs['fragment'] = fragment
        return attrs

    @staticmethod
    def expand_db_attributes(attrs, for_editor):  # #yfK6n#
        """
        Add the data-linktype, data-id and data-parent attributes like the default PageLinkHandler does,
        but also add our data-title and data-fragment.
        """
        try:
            page = Page.objects.get(id=attrs['id'])

            if for_editor:
                editor_attrs = 'data-linktype="page" data-id="%d" data-title="%s"' % (page.id, page.title)
                if attrs.get('fragment'):
                    editor_attrs += ' data-fragment="%s" ' % attrs.get('fragment')
                parent_page = page.get_parent()
                if parent_page:
                    editor_attrs += 'data-parent-id="%d" ' % parent_page.id
            else:
                editor_attrs = ''

            fragment = ''
            if attrs.get('fragment'):
                fragment = '#%s' % attrs.get('fragment')
            return '<a %shref="%s%s">' % (editor_attrs, escape(page.url), fragment)
        except Page.DoesNotExist:
            return "<a>"


class MediumDocumentLinkHandler(object):
    """
    Taken from : https://github.com/torchbox/wagtail/blob/c6666c6de5e83bf94d18324858c121e6584ba47d/wagtail/wagtailcore/rich_text.py#L21

    PageLinkHandler will be invoked whenever we encounter an <a> element in HTML content
    with an attribute of data-linktype="page". The resulting element in the database
    representation will be:
    <a linktype="page" id="42">hello world</a>
    """
    @staticmethod
    def get_db_attributes(tag):
        return {'id': tag['data-id']}

    @staticmethod
    def expand_db_attributes(attrs, for_editor):
        Document = get_document_model()
        try:
            doc = Document.objects.get(id=attrs['id'])

            if for_editor:
                editor_attrs = 'data-linktype="document" data-id="%d" data-title="%s" ' % (doc.id, doc.title)
            else:
                editor_attrs = ''

            return '<a %shref="%s">' % (editor_attrs, escape(doc.url))
        except Document.DoesNotExist:
            return "<a>"


@hooks.register('register_rich_text_link_handler')  # #b54WU#
def register_rich_text_link_handler():
    """
    This will replace wagtail's default PageLinkHandler
    https://github.com/torchbox/wagtail/blob/c6666c6de5e83bf94d18324858c121e6584ba47d/wagtail/wagtailcore/rich_text.py#L56
    """
    return ('page', MediumPageLinkHandler)


@hooks.register('register_rich_text_link_handler')
def register_rich_text_document_link_handler():
    """
    This will replace wagtail's default DocumentLinkHandler
    https://github.com/torchbox/wagtail/blob/c6666c6de5e83bf94d18324858c121e6584ba47d/wagtail/wagtaildocs/rich_text.py#L8
    """
    return ('document', MediumDocumentLinkHandler)
