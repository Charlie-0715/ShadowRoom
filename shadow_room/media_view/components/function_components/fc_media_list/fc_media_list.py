from django_components import Component, register

@register("fc_media_list")
class FCMediaList(Component):
    template_name = "fc_media_list.html"
    css_file = "fc_media_list.css"
    def get_context_data(self):
      pass