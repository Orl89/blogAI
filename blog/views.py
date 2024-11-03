from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.http import Http404
from .models import BlogHead, Post, SendMail, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity

# Create your views here.


def post_list(request, tag_slug=None):
    infos_head = BlogHead.objects.all()

    posts = Post.published.all()
    tag   = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts_list  = paginator.page(page_number)
    except PageNotAnInteger:
        posts_list  = paginator.page(1)
    except EmptyPage:
        posts_list  = paginator.page(paginator.num_pages)

    context={
        'infos_head': infos_head,
        'posts_list' : posts_list,
        'tag': tag,
        }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, day, month, year, post):
    try:
        post = Post.published.get(slug=post, 
                                  publish__day=day, 
                                  publish__month=month, 
                                  publish__year=year)
        
        comments = post.comments.filter(active=True)
        form = CommentForm()

        # List of similars posts
        post_tags_ids = post.tags.values_list('id', flat=True)
        similars_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similars_posts = similars_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    except Post.DoesNotExist:
        raise Http404('Aucun article trouvé...')
    
    return render(request, 'blog/detail.html', {'post': post, 'comments':comments, 'form':form, 'similars_posts': similars_posts})


# sending emails
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email= request.POST.get('email')
        to   = request.POST.get('to')
        comments = request.POST.get('comments')
        
        newMail = SendMail.objects.create(name=name, email=email, to=to, comments=comments)
        newMail.save()

        post_url = request.build_absolute_uri(post.get_absolute_url())
        subject  = f"{name} recommande que tu lises: " \
                    f"{post.title}"
        message  = f"Je t'invite à lire {post.title} via {post_url}\n\n" \
                    f"Le commentaire de {name} sur le sujet:\n {comments}"
        send_mail(subject, message, 'aorlando2889@gmail.com', [to])

        sent=True

        # return redirect('blog:post_list')
   
    return render(request, 'blog/post_share.html', {'post': post, 'sent': sent})
  

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        # assign the post to the comment
        comment.post = post
        comment.save()

    return render(request, 'blog/comment.html', {'post': post, 'form' : form, 'comment' : comment})



def post_search(request):
    form = SearchForm()
    requete = None
    results = []

    if 'requete' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            requete = form.cleaned_data['requete']
            results = Post.published.annotate(
                        similarity=TrigramSimilarity('title', requete),
                        ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request, 'blog/search.html', {'form': form, 'requete':requete, 'results':results})


def contact_whatsapp(request):
    contact_whatsapp = 'https://wa.me/+22892497009'
    context = {
        'contact_whatsapp':contact_whatsapp,
    }
    return render(request, 'blog/whatsapp.html', context)