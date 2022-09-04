from django import forms
from django.forms import CheckboxSelectMultiple, ModelForm, widgets
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'featured_image', 'demo_link', 'source_link', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'input'}),
            'featured_image': forms.FileInput(attrs={'class': 'input'}),
            'demo_link': forms.TextInput(attrs={'class': 'input'}),
            'source_link': forms.TextInput(attrs={'class': 'input'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'input'}),
        }
    
    #     widgets = {
    #         'tags' : forms.CheckboxSelectMultiple(),
    #     }

    # def __init__(self, *args, **kwargs):
    #     super(ProjectForm, self).__init__(*args, **kwargs)

    #     # self.fields['title'].widget.attrs.update({'class': 'input'})
        
        
    #     for name, field in self.fields.items():
    #         field.widget.attrs.update({'class': 'input'})
 

