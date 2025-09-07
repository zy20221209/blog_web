from django import forms
from .models import Post, Tag,Comment

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
                    'title': forms.TextInput(attrs={
                        'class': 'form-control form-control-lg',
                    }),
                    'content': forms.Textarea(attrs={
                        'class': 'form-control form-control-lg',
                        'rows': 10,
                    }),
                    'tags': forms.TextInput(attrs={
                        'class': 'form-control form-control-lg',
                        'placeholder': '输入标签，用逗号分隔，例如：python,django,web'
                    }),
                }
        help_texts = {
                    'tags': '支持中文标签，多个标签用英文逗号“,”分隔。',
                }
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError("标题至少5个字符")
        return title
    
class CommentForm(forms.ModelForm):
    """
    评论表单
    用于用户提交对文章的评论
    """
    class Meta:
        model = Comment
        fields = ['content']  # 只允许用户编辑评论内容
        widgets = {
            'content': forms.Textarea(attrs={
                'maxlength':500,
                'rows': 4,
                'placeholder': '写下你的评论...',
                'class': 'form-control'
            }),
        }
        labels = {
            'content': ''
        }

    def clean_content(self):
        """
        自定义验证：确保评论内容有意义
        """
        content = self.cleaned_data['content'].strip()
        if len(content) < 1:
            raise forms.ValidationError("评论内容至少需要1个字符。")
        if len(content) > 1000:
            raise forms.ValidationError("评论内容不能超过1000个字符。")
        return content