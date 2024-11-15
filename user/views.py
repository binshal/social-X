from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden,JsonResponse
from django.urls import reverse
from . models import Post,Comment,Like
from .forms import BlogPostForm,CommentForm,ImagePostForm


# Create your views here.
@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            Post = form.save(commit=False)
            Post.author = request.user
            Post.save()
            messages.success(request,'Blog posted successfully!')
            return  redirect('post_detail',pk=Post.pk)
    else:
        form = BlogPostForm()
    return render(request,'user/create_blog_post.html',{'form':form})

@login_required
def create_image_post(request):
    if request.method == 'POST':
        form = ImagePostForm(request.POST,request.FILES)
        if form.is_valid():
            Post = form.save(commit=False)
            Post.author = request.user
            Post.save()
            messages.success(request,'Image posted successfully!')
            return  redirect('post_detail',pk=Post.pk)
    else:
        form = ImagePostForm()
    return render(request,'user/create_image_post.html',{'form':form})

# @login_required
# def edit_post(request,pk):
#     post = get_object_or_404(Post,pk=pk)
#     if request.user != post.author:
#         return HttpResponseForbidden()
    
#     if post.post_type == 'blog':
#         form_class = BlogPostForm
#     else:
#         form_class = ImagePostForm

#     if request.method == 'POST':
#         form = form_class(request.POST,request.FILES,instance=post)
#         if form.is_valid():
#             form.save()
#             messages.success(request,f'{post.get_post_type_display()} updated successfully')
#             return redirect('post_detail',pk=post.pk)
#     else:
#         form = form_class(instance=post)

#     template_name = f'user/edit_{post.post_type}_post.html'
#     return render(request,template_name,{'form':form,'post':post})



@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user has permission to edit
    if request.user != post.author:
        return HttpResponseForbidden("You don't have permission to edit this post.")
    
    # Select the appropriate form based on post type
    form_class = BlogPostForm if post.post_type == 'blog' else ImagePostForm
    
    if request.method == 'POST':
        # Include request.FILES only for image posts
        if post.post_type == 'image':
            form = form_class(
                request.POST, 
                request.FILES, 
                instance=post
            )
            # Keep existing image if no new image is uploaded
            if not request.FILES.get('image') and post.image:
                form.fields['image'].required = False
        else:
            form = form_class(request.POST, instance=post)
        
        if form.is_valid():
            post = form.save(commit=False)
            # Ensure post_type doesn't change
            post.post_type = 'blog' if isinstance(form, BlogPostForm) else 'image'
            post.save()
            
            messages.success(
                request, 
                f'Your {post.get_post_type_display().lower()} has been updated successfully!'
            )
            return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # For GET requests, initialize form with instance
        form = form_class(instance=post)
        # Make image field optional for existing image posts
        if post.post_type == 'image' and post.image:
            form.fields['image'].required = False
    
    context = {
        'form': form,
        'post': post,
        'post_type': post.get_post_type_display(),
        'is_edit': True
    }
    
    template_name = f'user/edit_{post.post_type}_post.html'
    return render(request, template_name, context)




@login_required
def delete_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden()

    post.soft_delete()
    messages.success(request,f'{post.get_post_type_display()} deleted successfully!')
    return redirect('feed')

@login_required
def add_comment(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post =post
            comment.author = request.user
            comment.save()
            messages.success(request, 'comment added succesfully!')
            return redirect('post_detail',pk=pk)
    return redirect('post_detail',pk=pk)

@login_required
def toggle_like(request,pk):
    if request.method == 'POST':
        post = get_object_or_404(Post,pk=pk)
        like,created = Like.objects.get_or_create(post=post,user=request.user)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({
            'liked':liked,
            'likes_count':post.likes.count()
        })
    return JsonResponse({'error':'Invalid_request'}, status =400)

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    comments = post.comments.filter(is_blocked=False)
    Comment_form = CommentForm()
    user_has_liked = request.user.is_authenticated and post.likes.filter(user=request.user).exists()
    context = {
        'post':post,
        'comments':comments,
        'comment_form':Comment_form,
        'user_has_liked':user_has_liked,
    }
    return render(request,'user/post_detail.html',context)

@login_required
def feed(request):
    posts = Post.objects.filter(is_deleted=False,is_blocked=False).order_by('-created_at')
    return render(request,'user/feed.html',{'posts':posts})

@login_required
def user_posts(request,username):
    posts = Post.objects.filter(
        author__username=username,
        is_deleted = False,
        is_blocked = False,
    ).order_by('-created_at')
    return render(request,'user/user_posts.html',{'posts':posts,'username':username})
