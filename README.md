# ShadowRoom


## 使用
- 爬取豆瓣电影数据
``` shell
cd spider
scrapy crawl douban_movies_spider -o outputs/movie_info.json
```
- 更新sqlite
``` shell
python manage.py makemigrations
python manage.py migrate  
```
- 将json电影数据导入到sqlite
``` shell
python .\manage.py json_2_sqlite3 --file .\spider\outputs\movie_info.json
```
- run server
``` shell
python .\manage.py runserver 
```

## 项目需求
  1. 激活虚拟环境
  ``` shell
  source .env/bin/activate  
  ```
  2. django
  ``` shell
  python -m pip install Django 
  ```
  3. django-components
  ```

## 使用django-components模块化html文件
  1. 安装
  ```
  python -m pip install django-components
  ```
  2. 系统开启相关设置
  在 settings.py：
  ```python
  INSTALLED_APPS = [
      ...
      "django_components",
  ]
  ```
  并配置：
  ```python
  TEMPLATES = [
      {
          ...
          "OPTIONS": {
              "context_processors": [
                  ...
              ],
              "builtins": [
                  "django_components.templatetags.component_tags",
              ],
          },
      },
  ]
  ```
  3. 编写模块
  `navbar.html`
  ``` html
  <div> </div>
  ```

  4. 注册模块
  推荐目录结构
  ```
  media/
  │
  ├── components/
  │   └── navbar.py
  │
  ├── templates/
  │   └── components/
  │       └── navbar.html
  ```
  `navbar.py`
  ```python
  from django_components import Component, register


  @register("navbar")
  class Navbar(Component):
      template_name = "components/navbar.html"
  ```
  5. 让 Django 加载组件
  `media/apps.py`
  ```python
  from django.apps import AppConfig


  class MediaConfig(AppConfig):
      default_auto_field = "django.db.models.BigAutoField"
      name = "media"

      def ready(self):
          import media.components.navbar
  ```
  6. 使用组件
  ```django
        {% component 'fc_navbar' %}
        {% endcomponent %}
  ```

