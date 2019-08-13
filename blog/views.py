from django.views.generic import ListView, DetailView
from django.http import HttpResponse, Http404
from .models import BlogModel
from product.models import AlegroGoods, CatSubRus
from django.core.paginator import Paginator
from django.db.models import Q

class Blog(ListView):
    model = BlogModel
    template_name = 'blog/blog.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = BlogModel.objects.all().order_by('-publish')
        paginator = Paginator(queryset, 10)  # Show 25 contacts per page

        page = self.request.GET.get('page')
        context['object_list'] = paginator.get_page(page)
        context['resents']     = BlogModel.objects.all()[:3]
        # Нужно доделпть логику поиска здесь Запилить метод, который будет разбирать название статьи
        # на части и затем подставлять их в поиск для тегов, категорий и подкатегорий
        context['products']     = AlegroGoods.objects.filter(Q(name__icontains='blotn') | Q(name__icontains='filtr'))[:5]
        context['tags'] = CatSubRus.objects.filter(Q(pk__lt=604) & (Q(rus_name__icontains='освещен') | Q(rus_name__icontains='элект')))[:10]
        context['cats'] = CatSubRus.objects.filter(Q(pk__gt=604) & Q(pk__lt=1018) & (Q(rus_name__icontains='освещен') | Q(rus_name__icontains='элект')))[:10]
        return context



class BlogDetailSlugView(DetailView):
    queryset = BlogModel.objects.all()
    #template_name = 'products/product_detail_view.html'
    template_name = 'blog/blog_details.html'



    def get_context_data(self, *, object_list=None, **kwargs):
        slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['blog'] = BlogModel.objects.get(slug=slug)
        context['related']     = BlogModel.objects.filter(Q(description__icontains='шин') | Q(description__icontains='колес'))[:3]
        context['resents'] = BlogModel.objects.all().order_by('-publish')[:3]
        # Нужно доделпть логику поиска здесь Запилить метод, который будет разбирать название статьи
        # на части и затем подставлять их в поиск для тегов, категорий и подкатегорий
        context['products']      = AlegroGoods.objects.filter(Q(name__icontains='blotn') | Q(name__icontains='filtr'))[:5]
        #context['tags']          = CatSubRus.objects.filter(Q(pk__lt=604) & (Q(rus_name__icontains='освещен') | Q(rus_name__icontains='элект')))[:10]
        context['cats']          = CatSubRus.objects.filter(Q(pk__lt=604)  & (Q(rus_name__icontains='освещен') | Q(rus_name__icontains='элект')))[:10]
        return context


    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = BlogModel.objects.get(slug=slug)
        except BlogModel.DoesNotExist:
            raise Http404('Not found')
        except BlogModel.MultipleObjectsReturned:
            qs = BlogModel.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404('Hmmm...')
        return instance

