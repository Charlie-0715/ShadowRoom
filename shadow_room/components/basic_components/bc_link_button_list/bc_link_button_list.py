from django_components import Component, register

@register("bc_link_button_list")
class BCLinkButtonList(Component):
    template_name = "bc_link_button_list.html"
    css_file = "bc_link_button_list.css"

    def get_context_data(self, target_data=None):
        return {
            "target_data": target_data,
        }