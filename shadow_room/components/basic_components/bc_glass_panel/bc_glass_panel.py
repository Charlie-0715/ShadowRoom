from django_components import Component, register

@register("bc_glass_panel")
class BCGlassPanel(Component):
    template_name = "bc_glass_panel.html"
    css_file = "bc_glass_panel.css"

    def get_context_data(self, class_name=""):
        return {
            "class_name": class_name,
        }