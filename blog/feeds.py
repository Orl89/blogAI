from django.db.models.base import Model
import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from .models import Post
from django.urls import reverse_lazy

class LatestPostsFeed(Feed):
    title = 'Info Blog'
    link  = reverse_lazy('blog:post_list')
    description = 'Articles récents de mon Blog'


    def items(self):
        return Post.published.all()[:6]
    

    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)
    
    def item_update(self, item):
        return item.publish