from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Blog, Comment, Social_Media, Contact , Company , FAQ
from .forms import CommentForm, ContactForm
from django.contrib import messages
from UserManagement.models import CustomUser 
from JobPortal.models import Candidate  , Job_Posting

# Create your views here.
social_medias = Social_Media.objects.all()

def blog(request):
    try:
        latest_blog = Blog.objects.first()
        blogs = Blog.objects.all().exclude(id = latest_blog.id)
    except:
        latest_blog  = None
        blogs = None
    
    paginator = Paginator(blogs, 9)
    page_number = request.GET.get('page')
    try: page = paginator.get_page(page_number)
    except: page = None

    print('>>>', blogs)


    context = {
        'social_medias' : social_medias,
        'latest_blog' : latest_blog,
        'blogs' : page,
        
    }
    return render(request, 'Company/blog.html', context)

def single_blog(request, slug):
    blog = Blog.objects.filter(slug = slug).first()
    latest_post = Blog.objects.all().exclude(slug = slug)[:4]
    comments =  Comment.objects.filter(blog__pk = blog.pk)
   
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            messages.success(request, 'Your comment has been successfully sent!')
            form = CommentForm()

    context = {
        'social_medias' : social_medias,
        'blog' : blog,
        'latest_posts' : latest_post,
        'form' : form,
        'comments' : comments
    }
    return render(request, 'Company/blog-details.html', context)

def contact(request):
    contact = Contact.objects.all().first()
    if request.method == 'POST':
        form = ContactForm(request.POST)  
        if form.is_valid():
            form.save()
            messages.success(request, 'Your request has been successfully sent')
            form = ContactForm()
    else:
        form = ContactForm()


    context = {
        'social_medias' : social_medias,
        'contact' : contact,
        'form' : form
    }
    return render(request, 'Company/contact.html', context)

def about(request):
    users = CustomUser.objects.all().count()
    candidate = Candidate.objects.all().count()
    jobs = Job_Posting.objects.all().count()
    company = Company.objects.all().count()

    context = {
        "users" : users,
        "candidate" : candidate,
        "jobs" : jobs,
        "company" : company,
        'social_medias' : social_medias,
    }
    return render(request, 'Company/about.html',context)

def privacy_and_policy(request):
    context = {
        'social_medias' : social_medias,
    }
    return render(request, 'Company/privacy-policy.html', context)

def faqs(request):
    faqs = FAQ.objects.all()
    total_faqs = faqs.count()
    half_point = total_faqs // 2
    
    faq1 = faqs[:half_point]
    faq2 = faqs[half_point:]
    context = {
        'social_medias' : social_medias,
        "faq1" : faq1,
        "faq2" : faq2

    }
    return render(request, 'Company/faqs.html',context)