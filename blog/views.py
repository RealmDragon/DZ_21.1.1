from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy,reverse
from blog.models import Blog
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'image')


    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class BlogListView(ListView):
    paginate_by: int = 6
    model = Blog

    def get_queryset(self, *args, **kwargs):
        qyryset = super().get_queryset(*args, **kwargs)
        qyryset = qyryset.filter(is_published=True)
        return qyryset

class BlogDetailView(DetailView):
    model = Blog


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('blog:blog_list')



def is_published(request, pk):
    is_published_blog = get_object_or_404(Blog, pk=pk)
    if is_published_blog:
        is_published_blog = False
    else:
        is_published_blog = True

    is_published_blog.save()

    return redirect(reverse('blog:blog_list'))