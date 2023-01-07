from django.shortcuts import render,get_object_or_404
from .models import Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView

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

class PostListView(ListView):
    #Alternative post list view
    queryset=Post.published.all()
    template_name = 'blog/post/list.html'
    paginate_by=3
    context_object_name='posts'
