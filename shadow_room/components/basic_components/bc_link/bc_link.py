from django_components import Component, register

@register("bc_link")
class BCLink(Component):
    template_name = "bc_link.html"
    # css_file = "bc_glass_panel.css"

    def get_context_data(self, target_url=None, target_class=""):
        return {
            "target_url": target_url,
            "class_name": target_class,
        }