from django_components import Component, register


@register("fc_navbar")
class Navbar(Component):
    template_name = "fc_navbar.html"
    list_data=[['media_view:index', 'home', '首页'],
                 ['media_view:movie_list', 'movie', '电影'],
                 ['media_view:tv_list', 'tv', '电视剧'],
                 ['media_view:animated_film_list', 'animated_film', '剧场版'],
                 ['media_view:animation_list', 'animation', '动漫'],
                 ['media_view:documentary_list', 'documentary', '纪录片'],
                 ['media_view:category_list', 'category', '分类'],]
    def get_context_data(self):
        return {
            "list_data": self.list_data,
        }