# 📁 项目目录结构与架构说明

本项目基于 Django 框架开发，采用了**混合模板管理模式（Hybrid Template Mode）**以及**组件化前端开发（Django Components）**架构。以下为项目的核心目录树结构及详细说明，供后期维护参考。

## 🌳 目录树结构

```text
.
├── docs
│   └── PROJECT_STRUCTURE.md
├── README.md
├── shadow_room                                                                 # django项目
│   ├── components                                                              # 全局组件
│   │   ├── basic_components                                                    # 基础小组件
│   │   │   └── bc_frosted_glass_div        
│   │   │       ├── bc_frosted_glass_div.css
│   │   │       ├── bc_frosted_glass_div.html
│   │   │       ├── bc_frosted_glass_div.py
│   │   │       ├── __init__.py
│   │   └── function_components                                                 # 组合而成全局框架的功能性组件
│   │       └── fc_navbar
│   │           ├── fc_navbar.html
│   │           ├── fc_navbar.py
│   │           ├── __init__.py
│   ├── db.sqlite3                                                              # 数据库
│   ├── manage.py
│   ├── media                                                                   # 媒体放置位置
│   ├── media_view                                                              # media view app，媒体展示页面
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── components                                                          # 媒体展示功能组件
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── templates                                                           # 媒体展示页面
│   │   │   ├── category_list.html
│   │   │   ├── index.html
│   │   │   ├── media_detail.html
│   │   │   └── media_list.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── shadow_room
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── share
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── components
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── static
│   └── templates                                                               # 全局基本页面
│       └── base.html
└── spider                                                                      # 爬虫脚本库
    ├── scrapy.cfg
    ├── selenium_spider.py
    ├── spider
    │   ├── __init__.py
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-313.pyc
    │   │   ├── items.cpython-313.pyc
    │   │   ├── pipelines.cpython-313.pyc
    │   │   └── settings.cpython-313.pyc
    │   ├── settings.py
    │   └── spiders
    │       ├── douban_spider.py
    │       ├── __init__.py
    │       ├── __pycache__
    │       │   ├── douban_spider.cpython-313.pyc
    │       │   ├── __init__.cpython-313.pyc
    │       │   └── test.cpython-313.pyc
    │       └── test.py
    └── tools
        ├── __pycache__
        │   └── random_wait.cpython-313.pyc
        └── random_wait.py
```

---

## 🛠️ 关键架构设计与维护指南

### 1. 混合模板寻址机制 (Hybrid Templates)

项目为了兼顾“全局复用”和“应用高内聚”，在 `shadow_room/settings.py` 中同时开启了两种模板查找模式：

* **全局查找 (`DIRS`)**：Django 优先去项目根目录下的 `templates/` 寻找。全站共享的骨架（如 `base.html`）存放在此。
* **应用内查找 (`APP_DIRS=True`)**：若全局未找到，Django 会自动扫描各应用下的 `templates/`。业务页面（如 `media_view/templates/media/index.html`）存放在此，并通过 `{% extends 'base.html' %}` 继承全局骨架。

> 📌 **维护注意**：在编写 `views.py` 渲染页面时，请使用带有子路径的相对路径，例如 `render(request, 'media/index.html')`。

### 2. 组件化前端开发 (Django Components)

项目引入了 `django-components` 库，将前端 UI 拆分为可复用的高内聚组件（类似 Vue/React 组件）。

* **规范**：组件必须存放在应用下名为 `components/` 的文件夹中，否则 Django 启动时无法通过自动寻址（Autodiscovery）机制加载。
* **结构**：一个组件由一个文件夹包裹，内部包含同名的 `.py`（注册与数据逻辑）和 `.html`（组件结构）。
* **调用示例**：
在模板中先加载库：`{% load component_tags %}`，然后通过 `{% component "fc_navbar" %}` 即可直接渲染导航栏。

---

## 🚀 后期扩展备忘

1. **新增全局通用组件**：如果建立了类似 `bc_frosted_glass_div` 的全局组件，请确保在 `settings.py` 的 `COMPONENTS` 配置中添加路径 `BASE_DIR / 'components'`，或者将其封装并编写对应的 `.py` 注册文件。
2. **激活应用**：新增任何应用（如当前的 `media_view` 和 `share`）后，必须第一时间将其字符串填入 `settings.py` 的 `INSTALLED_APPS` 中，否则模型（Models）与模板组件将无法生效。