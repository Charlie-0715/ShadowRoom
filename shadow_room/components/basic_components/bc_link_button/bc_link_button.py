from django_components import Component, register

@register("bc_link_button")
class BCLinkButton(Component):
    template_name = "bc_link_button.html"
    css_file = "bc_link_button.css"

    def get_context_data(self, target_url=None, target_active=""):
        return {
            "target_url": target_url,
            "target_active": target_active,
        }