from django_components import Component, register

@register("fc_filter_panel")
class FCFilterPanel(Component):
    template_name = "fc_filter_panel.html"
    css_file = "fc_filter_panel.css"
    def get_context_data(self):
      pass