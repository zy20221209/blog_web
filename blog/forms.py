from django import forms
from .models import Post, Tag,Comment


from django.forms.widgets import TextInput
from .models import Tag

class TagWidget(TextInput):
    """自定义 Widget：显示为文本输入框"""
    def __init__(self, attrs=None):
        default_attrs = {'placeholder': '输入标签，用英文逗号分隔'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

class TagField(forms.CharField):
    """自定义字段：处理逗号分隔的标签字符串"""
    widget = TagWidget

    def __init__(self, *args, **kwargs):
        self.is_required = kwargs.get('required', False)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        """将输入字符串转换为 Tag 对象列表"""
        if not value:
            return []
        # 分割并清理标签名
        tag_names = [name.strip() for name in value.split(',') if name.strip()]
        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(
                name=name.lower()  # 统一小写，避免重复
            )
            tags.append(tag)
        return tags

    def prepare_value(self, value):
        """将已有标签转换为逗号分隔的字符串（用于表单回显）"""
        if isinstance(value, list):
            return ', '.join([str(tag.name) for tag in value])
        if hasattr(value, 'all'):
            return ', '.join([tag.name for tag in value.all()])
        return value

class PostForm(forms.ModelForm):
    tags = TagField(
        required=False,
        help_text="输入标签，用逗号分隔。",
        label="标签"
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