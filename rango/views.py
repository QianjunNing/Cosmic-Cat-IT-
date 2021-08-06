from django.shortcuts import render

from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm

from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.webhose_search import run_query
from rango.models import Category, UserComment, UserProfile

# def index(request):
#     return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>")

def index(request):
    # request.session.set_test_cookie()  
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]


    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    
    # response = render(request, 'rango/index.html', context=context_dict)
    visitor_cookie_handler(request)
    
    response = render(request, 'rango/index.html', context=context_dict)
    return response




def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')

        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None
    
  
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)  
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 
            'rango/register.html', 
            context={'user_form': user_form, 
                     'profile_form': profile_form, 
                     'registered': registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit', str(datetime.now()))    
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')


    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits

def search(request):
    """use search API to search"""
    result_list = []
    query = ''

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)
    
    return render(request, 'rango/search.html', {'result_list': result_list, 'query': query})

def search_category(request):
    """search category in the current database """
    result_list = ''
    search_category = ''
    indexs = 0
    if request.method == 'POST':
        search_category = request.POST['search_category'].strip()

        if search_category:
            result_list = Category.objects.filter(slug=search_category)

    context_dict = {}
    context_dict['categories'] = result_list
   
    visitor_cookie_handler(request)
    
    response = render(request, 'rango/search_category.html', context=context_dict)
    return response

def view_all(request):
    """view all categories"""
    response = render(request, 'rango/view_all.html')
    return response

def add_comment(request):
    # get information from request.POST
    content = request.POST.get('content')
    user = UserProfile.objects.filter(user_id=request.POST.get('user_id'))[0]
    category = Category.objects.filter(id=request.POST.get('category_id'))[0]
    ob = UserComment(content=content, user=user, category=category)
    # update to database
    ob.save()
    # reload current page
    return redirect('/rango/category/'+category.slug.lower())

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        # pass the data of comments about this category
        comments = UserComment.objects.filter(category=category)
        context_dict['comments'] = comments

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    
    return render(request, 'rango/category.html', context=context_dict)
