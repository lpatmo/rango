from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.template import RequestContext #added extra
# Create your views here.



def index(request): 
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    return render(request, 'rango/index.html', context_dict)

def category(request, category_name_slug):
	context_dict = {}
	try:
	    category = Category.objects.get(slug=category_name_slug)
	    context_dict['category_name'] = category.name

	    pages = Page.objects.filter(category=category)

	    context_dict['pages'] = pages
	    context_dict['category'] = category

	except Category.DoesNotExist:
		pass
	return render(request, 'rango/category.html', context_dict)

def about(request):
    # Request the context.
    context = RequestContext(request)
    context_dict = {}
    cat_list = get_category_list()
    context_dict['cat_list'] = cat_list
    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.

    count = request.session.get('visits',0)

    context_dict['visit_count'] = count

    # Return and render the response, ensuring the count is passed to the template engine.
    return render_to_response('rango/about.html', context_dict , context)


def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        #do we have a valid form?
        if form.is_valid():
            form.save(commit=True)

        #now call the index() view.
        #the user will be shown the homepage.
            return index(request)
        else: 
        #the supplied form contained errors. print errors to terminal.
            print form.errors
    else:
        # if the request was not a POST, display the form to enter details.
        form = CategoryForm()

    #bad form (or form details), no form supplied...

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):

    try: 
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else: 
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)




