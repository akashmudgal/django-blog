from django.shortcuts import render,get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm,CommentForm
from .models import Post,Comment

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
    #Get the post
    post=get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    
    #comments on the post
    comments=post.comments.filter(active=True)
    #form for users to post Comments
    form=CommentForm()
    #render the template with the data
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,'comments':comments,'form':form})

def post_share(request,post_id):
    #retreive post by id
    post=get_object_or_404(Post.published,id=post_id)
    sent=False
    if request.method == 'POST':
        #Create form from request data
        form=EmailPostForm(request.POST)
        #Check if form is valid
        if form.is_valid():
            #Clean the form data
            cd = form.cleaned_data
            #Build absolute url for the post
            post_url = request.build_absolute_uri(post.get_absolute_url())
            #email subject
            subject = f"{cd['name']} recommends you read {post.title}" 
            #email message
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            #Send te email
            send_mail(subject, message, 'your_account@gmail.com',[cd['to']])
        sent = True
    else:
        form=EmailPostForm()
    return render(request,'blog/post/share.html',{'post': post,'form':form,'sent':sent})

@require_POST
def post_comment(request,post_id):
    post=get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    form=CommentForm(data=request.POST)
    
    if form.is_valid():
        comment=form.save(commit=False)
        comment.post=post
        comment.save()
    
    return render(request,'blog/post/comment.html',{'post':post,'form': form,'comment': comment})

class PostListView(ListView):
    #Alternative post list view
    queryset=Post.published.all()
    template_name = 'blog/post/list.html'
    paginate_by=3
    context_object_name='posts'
