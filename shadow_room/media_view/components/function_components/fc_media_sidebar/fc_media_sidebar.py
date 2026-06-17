from django_components import Component, register

@register("fc_media_sidebar")
class FCMediaSidebar(Component):
    template_name = "fc_media_sidebar.html"
    css_file = "fc_media_sidebar.css"
    def get_context_data(self):
      pass