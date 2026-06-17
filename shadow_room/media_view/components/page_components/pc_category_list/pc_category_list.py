from django_components import Component, register

@register("pc_category_list")
class PCCategoryList(Component):
    template_name = "pc_category_list.html"
    css_file = "pc_category_list.css"
    def get_context_data(self):
      pass