from django import forms
from .models import Post,Comment


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control'}),
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.instance.post_type = 'blog'

class ImagePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','image','image_caption']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'image_caption':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.instance.post_type = 'image'
        self.fields['image'].required = True

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content':forms.Textarea(attrs={'class':'form-control','rows':3}),
        }
