from django_components import Component, register

@register("fc_featured_section")
class FCBackGround(Component):
    template_name = "fc_featured_section.html"
    css_file = "fc_featured_section.css"
    def get_context_data(self, 
                         section_title = None, 
                         section_link = None,
                         medias = None):
      return {
            "section_title":section_title,
            "section_link":section_link,
            "medias": medias
        }