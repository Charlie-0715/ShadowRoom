from django_components import Component, register

@register("bc_link_list")
class BCLinkList(Component):
    template_name = "bc_link_list.html"
    # css_file = "bc_glass_panel.css"

    def get_context_data(self, target_data=None):
        return {
            "target_data": target_data,
        }