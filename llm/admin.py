from django.contrib import admin
from .models import UploadFile,Comment
from django.utils.safestring import mark_safe
from .forms import UploadFileForm
from openai import OpenAI
import openai,os
from dotenv import load_dotenv
import environ
# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# class MyAdminSite(admin.AdminSite):
#     site_header = "Monty Python administration"
#     def has_delete_permission(self, request, obj=None):

#         # اگر obj وجود نداشته باشد،
#         # اجازه کلی حذف بررسی می‌شود
#         if obj is None:
#             return True

#         # فقط صاحب فایل می‌تواند آن را حذف کند
#         return obj.uploaded_by == request.user



# admin_site = MyAdminSite(name="myadmin")
# admin_site.register(UploadFile)


@admin.register(UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    site_header = "Monty Python administration"
    list_display = ('name','author','file')
    search_fields = ['name','author']
    fieldset=[
        (
            "Basic options",
            {
                "fields": ["author","name", "text", "file"],
            }
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields": ["registration_required", "template_name"],
            },
        ),
    ]
    actions = ["generate_openai_summary"]
    
    @admin.action(description="Generate AI summary via OpenAI")
    def generate_openai_summary(self, request, queryset):
        success_count = 0
        for obj in queryset:
            try:
                content_file = obj.file

                with content_file.open("rb") as f:
                    content = f.read().decode("utf-8", errors="ignore")
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Summarize this text concisely."},
                        {"role": "user", "content":content}
                    ]
                )
                
                obj.ai_summary = response.choices[0].message.file
                obj.save()
                success_count += 1
            except Exception as e:
                self.message_user(request, f"Error on {obj.pk}: {e}", level="error")
        
        if success_count:
            self.message_user(request, f"Successfully updated {success_count} items with OpenAI.")

    def summary_preview(self, obj):
        return obj.ai_summary[:50] if obj.ai_summary else "-"
    summary_preview.short_description = "AI Summary"


    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.author == request.user
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user

        super().save_model(request, obj, form)
        # return obj.author == request.user
    
    def has_delete_permission(self, request, obj=None):

        if obj is None:
            return True

        return obj.author == request.user
    
    
    

    