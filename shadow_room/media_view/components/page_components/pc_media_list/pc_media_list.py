from django_components import Component, register

@register("pc_media_list")
class PCMediaList(Component):
    template_name = "pc_media_list.html"
    css_file = "pc_media_list.css"
    def get_context_data(self):
      pass