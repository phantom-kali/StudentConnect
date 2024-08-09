from django import forms
from .models import Story
from django.core.exceptions import ValidationError
import magic
from django.template.defaultfilters import filesizeformat
from django.conf import settings

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['content', 'caption']
        widgets = {
            'content': forms.FileInput(attrs={'accept': 'image/*,video/*', 'class': 'form-control-file'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content:
            file_size = content.size
            if file_size > settings.MAX_UPLOAD_SIZE:
                raise ValidationError(f"The maximum file size that can be uploaded is {filesizeformat(settings.MAX_UPLOAD_SIZE)}")

            file_type = magic.from_buffer(content.read(1024), mime=True)
            if file_type.startswith('video/'):
                import cv2
                video = cv2.VideoCapture(content.temporary_file_path())
                duration = video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)
                if duration > 30:
                    raise ValidationError("Video duration should not exceed 30 seconds.")
            elif not file_type.startswith('image/'):
                raise ValidationError("File type not supported. Please upload an image or video.")

        return content