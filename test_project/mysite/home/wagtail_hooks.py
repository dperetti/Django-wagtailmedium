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
