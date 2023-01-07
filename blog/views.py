from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm
from .models import Post

# View for all posts
def post_list(request):
    post_list=Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page',1)
    
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        #if Page index out of range go to last page
        posts=paginator.page(1)
    except EmptyPage:
        #if Page index out of range go to last page
        posts=paginator.page(paginator.num_pages)

    return render(request,
                'blog/post/list.html',
                {'posts': posts})


def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def post_share(request,post_id):
    #retreive post by id
    post=get_object_or_404(Post.published,id=post_id)
    sent=False
    if request.method == 'POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}" 
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',[cd['to']])
        sent = True
    else:
        form=EmailPostForm()
    return render(request,'blog/post/share.html',{'form':form})

class PostListView(ListView):
    #Alternative post list view
    queryset=Post.published.all()
    template_name = 'blog/post/list.html'
    paginate_by=3
    context_object_name='posts'
