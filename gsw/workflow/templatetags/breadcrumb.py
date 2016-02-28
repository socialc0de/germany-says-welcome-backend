from django import template

register = template.Library()

@register.inclusion_tag('breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    if hasattr(context['view'], "crumbs"):
        return getattr(context['view'], "crumbs")
    else:
        path = context['request'].path
        crumbs_parts = path.split("/")
        crumbs_parts = list(filter(None, crumbs_parts))
        crumbs = []
        for i,value in enumerate(crumbs_parts):
            url = "/"+"/".join(crumbs_parts[:i+1])+"/"
            crumbs.append({"name":value, "url":url})
            #import pdb;pdb.set_trace()
        return {"crumbs":crumbs}