from pyexpat import model

from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Alias(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class MediaModels(models.Model):
        
    TYPES = [
        ('movie', '电影'),
        ('tv', '电视剧'),
        ('animation', '动漫'),
        ('animated_film', '剧场版')
    ]

    type = models.CharField(
        max_length=100,
        choices=TYPES,
        verbose_name='类型'
    )

    douban_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='豆瓣ID'
    )

    title = models.CharField(
        max_length=255,
        verbose_name='名称'
    )
    
    douban_url = models.URLField(
        max_length=200,
        verbose_name='豆瓣链接'
    )

    douban_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name='豆瓣评分'
    )

    director = models.ManyToManyField(
        Person,
        blank=True,
        related_name='directed_medias',
        verbose_name='导演'
    )

    writers = models.ManyToManyField(
        Person,
        blank=True,
        related_name='written_medias',
        verbose_name='编剧'
    )

    actors = models.ManyToManyField(
        Person,
        blank=True,
        related_name='acted_medias',
        verbose_name='主演'
    )

    genres = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='类型'
    )

    countries = models.ManyToManyField(
        Country,
        blank=True,
        verbose_name='制片国家/地区'
    )
    
    # 大致分为，华语，欧美，日韩，东南亚
    area = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="片区"
    )

    alias = models.ManyToManyField(
        Alias,
        blank=True,
        verbose_name='又名'
    )
    
    imdb_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='IMDb'
    )

    summary = models.TextField(
        blank=True,
        verbose_name='剧情简介'
    )

    poster_locate = models.ImageField(
        upload_to='posters/',
        blank=True,
        verbose_name='海报位置'
    )

    episodes = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='集数'
    )

    seasons = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='季数'
    )

    # 只用来显示
    release_date_with_locations =  models.JSONField(
        default=list, 
        blank=True, 
        verbose_name='上映日期（地点）')
    
    runtime = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='时长(分钟)'
    )

    # 如有多个 只取第一个, 都存一个，这样查询起来快一些
    release_years = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name='上映年份'
    )

    release_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='上映日期'
    )

    release_ear = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='上映年代'
    )

    class Meta:
        verbose_name = '影视'
        verbose_name_plural = '影视'
        ordering = ['-douban_rating']

    # def genre_list(self):
    #     return [g.strip() for g in self.genres.split(',') if g.strip()]

    def __str__(self):
        return self.title
