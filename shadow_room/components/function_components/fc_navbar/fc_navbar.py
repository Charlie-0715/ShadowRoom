from django_components import Component, register


@register("fc_navbar")
class Navbar(Component):
    template_name = "fc_navbar.html"