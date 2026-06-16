from django_components import component

@component.register("bc_frosted_glass_div")
class FrostedGlassDivComponent(component.Component):
    # 指定该组件对应的 HTML 模板路径
    template_name = "bc_frosted_glass_div/bc_frosted_glass_div.html"

    # 也可以在组件中直接关联 CSS，django-components 会自动在页面中渲染它
    class Media:
        css = "bc_frosted_glass_div/bc_frosted_glass_div.css"

    def get_context_data(self, blur=12, opacity=0.15, rounded="16px", border_color="rgba(255, 255, 255, 0.2)", extra_classes="", **kwargs):
        """
        获取组件上下文数据，支持通过模板参数自定义外观：
        :param blur: 模糊半径（单位：px），默认 12px
        :param opacity: 白色背景不透明度（0 到 1），默认 0.15
        :param rounded: 圆角大小，默认 16px
        :param border_color: 边框颜色，默认微亮的半透明白色
        :param extra_classes: 额外注入的 Tailwind CSS 或自定义 CSS 类名
        """
        return {
            "blur": blur,
            "opacity": opacity,
            "rounded": rounded,
            "border_color": border_color,
            "extra_classes": extra_classes,
            "content": kwargs.get("content", ""), # 容器内承载的 HTML 内容
        }