import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page


def populate():
    cat_pages = [
        {'title': 'American Curl',
         'url':'https://en.wikipedia.org/wiki/American_Curl',
         'views': 200,},
        {'title':'Pixie-bob',
         'url':'https://rdweb.wvd.microsoft.com/arm/webclient/index.html',
         'views': 72},
        {'title':'Ragdoll',
         'url':'https://en.wikipedia.org/wiki/Ragdoll',
         'views': 220},
        {'title':'Dragon Li',
         'url':'https://en.wikipedia.org/wiki/Dragon_Li',
         'views': 220},
        ]
    
    fairytale_pages = [
        {'title':'Snow White and the Seven Dwarfs',
         'url':'https://www.storyberries.com/fairy-tales-little-snow-white-by-brothers-grimm/',
         'views': 240},
        {'title':'The Little Mermaid',
         'url':'https://www.storyberries.com/fairy-tales-the-little-mermaid-by-hans-christian-andersen/',
         'views': 12},
        {'title':'The Twelve Dancing Princesses',
         'url':'https://www.storyberries.com/fairy-tales-the-twelve-dancing-princesses-by-brothers-grimm/',
         'views': 128 },
         {'title':'The Little Elder Tree Mother',
         'url':'https://www.storyberries.com/fairy-tales-the-little-elder-tree-mother-by-hans-christian-andersen/',
         'views': 128 }, ]
    
    other_pages = [
        {'title':'Planets – NASA Solar System Exploration',
         'url':'https://solarsystem.nasa.gov/planets/overview/',
          'views': 54},
        {'title':'HEAVY RAIN at Night 10 Hours for Sleeping, Relax, Study, insomnia, Reduce Stress. Heavy Rain Sounds',
         'url':'https://www.youtube.com/watch?v=9QneqUhCVtU',
         'views': 14} ]
    
    cats = {'CAT': {'pages': cat_pages, 'views': 215, 'likes': 59},
            'Fairy Tale': {'pages': fairytale_pages, 'views': 64, 'likes': 32},
            'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16} }
    
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], views=p['views'])
    
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

if __name__ == '__main__':
    print('Starting  population script...')
    populate()