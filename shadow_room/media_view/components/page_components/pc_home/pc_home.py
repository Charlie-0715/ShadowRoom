from django_components import Component, register

@register("pc_home")
class PCHome(Component):
    template_name = "pc_home.html"
    css_file = "pc_home.css"
    def get_context_data(self):
      pass