# 📁 项目目录结构与架构说明

本项目基于 Django 框架开发，采用了**混合模板管理模式（Hybrid Template Mode）**以及**组件化前端开发（Django Components）**架构。以下为项目的核心目录树结构及详细说明，供后期维护参考。

## 🌳 目录树结构

```text
.
├── README.md                           # 项目说明文档
└── shadow_room/                        # 项目核心根目录（包含所有源码）
    ├── manage.py                       # Django 命令行工具入口
    ├── db.sqlite3                      # 本地开发数据库（SQLite）
    ├── media/                          # 用户上传的媒体文件目录（如图片、视频等）
    ├── static/                         # 网站全站静态资源（CSS, JS, Images）
    │
    ├── shadow_room/                    # 项目全局配置主目录
    │   ├── settings.py                 # 全局核心配置文件（包含安装应用、数据库、中间件等）
    │   ├── urls.py                     # 全局主路由分发器
    │   ├── wsgi.py / asgi.py           # 异步/同步服务器网关接口配置
    │   └── __init__.py
    │
    ├── templates/                      # ─── 模式 A：全站全局模板目录 ───
    │   └── base.html                   # 全站公共基础骨架（包含 <html>, <head>, <body> 结构）
    │
    ├── components/                     # ─── 模式 B：全局通用组件目录 ───
    │   └── bc_frosted_glass_div.html   # 全局基础组件：毛玻璃样式基础区块
    │
    ├── media_view/                     # ─── 业务应用：核心音视频/媒体展示模块 ───
    │   ├── apps.py                     # 应用配置文件
    │   ├── models.py                   # 媒体、分类等数据库模型定义（如 Person 等）
    │   ├── views.py                    # 业务视图逻辑控制
    │   ├── urls.py                     # 路由映射（命名空间：media）
    │   │
    │   ├── components/                 # ─── 应用级专属组件目录 ───
    │   │   └── fc_navbar/              # 功能导航栏组件
    │   │       ├── __init__.py
    │   │       ├── fc_navbar.py        # 组件注册及后端逻辑控制（@component.register）
    │   │       └── fc_navbar.html      # 组件前端 HTML 模板
    │   │
    │   └── templates/                  # ─── 模式 C：应用专属模板目录 ───
    │       └── media/                  # 独立业务页面目录（防止模板重名冲突）
    │           ├── index.html          # 暗影室首页
    │           ├── category_list.html  # 分类列表页
    │           ├── media_list.html     # 媒体流列表页
    │           └── media_detail.html   # 媒体详情播放页
    │
    └── share/                          # ─── 业务应用：社交分享/公共数据模块 ───
        ├── models.py                   # 分享、评论或点赞等相关模型
        ├── views.py                    # 分享业务视图
        └── components/                 # 预留的公共共享组件扩展目录

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