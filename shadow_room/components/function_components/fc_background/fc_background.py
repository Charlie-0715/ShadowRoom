from django_components import Component, register

@register("fc_background")
class FCBackGround(Component):
    template_name = "fc_background.html"
    css_file = "fc_background.css"