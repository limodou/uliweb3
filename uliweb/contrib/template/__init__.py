def startup_installed(sender):
    from uliweb.core import template
    from .tags import link, use, htmlmerge
    
    template.default_namespace['_tag_link'] = link
    template.default_namespace['_tag_use'] = use
    template.default_namespace['_tag_htmlmerge'] = htmlmerge

