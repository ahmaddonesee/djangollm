from django.contrib import admin

from django.urls import reverse
from .models import UploadFile,Comment
from .services import ask_question
from django.urls import path
from django.shortcuts import render
from django.db.models import Q
from .services import ask_question
from django.utils.html import format_html

from openai import OpenAI
import openai,os
from dotenv import load_dotenv
import environ





# Initialize environment variables
env = environ.Env()
environ.Env.read_env()
from django.db.models import Q

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
    # name__icontains="django"
    exclude = ["author"]
    site_header = "Monty Python administration"
    list_display = ('name','author','file','download_button') #,'file_content'
    search_fields = ['name','author__username']
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
        pass
        # success_count = 0
        # for obj in queryset:
        #     try:
        #         content_file = obj.file

        #         with content_file.open("rb") as f:
        #             content = f.read().decode("utf-8", errors="ignore")
        #         response = client.chat.completions.create(
        #             model="gpt-4o-mini",
        #             messages=[
        #                 {"role": "system", "content": "Summarize this text concisely."},
        #                 {"role": "user", "content":content}
        #             ]
        #         )
                
        #         obj.ai_summary = response.choices[0].message.file
        #         obj.save()
        #         success_count += 1
        #     except Exception as e:
        #         self.message_user(request, f"Error on {obj.pk}: {e}", level="error")
        
        # if success_count:
        #     self.message_user(request, f"Successfully updated {success_count} items with OpenAI.")

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

        super().save_model(request, obj, form,change)
    
    def has_delete_permission(self, request, obj=None):

        if obj is None:
            return True

        return obj.author == request.user
    
    def get_search_results(self, request, queryset, search_term):

        # First let Django perform the normal search
        queryset, use_distinct = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        if not search_term:
            return queryset, use_distinct

        related_files = []

        # Search inside the uploaded .txt files
        for uploadfile in UploadFile.objects.all():

            if not uploadfile.file:
                continue

            try:
                with uploadfile.file.open("r") as file:
                    content = file.read()

            except Exception:
                continue

            # Check whether search term exists in file content
            if search_term.lower() in content.lower():

                related_files.append(uploadfile.pk)

        # Add files found by content search
        queryset = UploadFile.objects.filter(
            Q(pk__in=related_files) |
            Q(name__icontains=search_term)
        )

        return queryset, use_distinct
   


    def file_content(self, obj):

        if not obj.file:
            return "-"

        try:
            with obj.file.open("r") as f:
                content = f.read()

            # Show only first 500 characters
            content = content[:500]

            return format_html(
                "<pre style='white-space: pre-wrap;'>{}</pre>",
                content,
            )

        except Exception as e:
            return f"Error: {e}"

    file_content.short_description = "Content"

    def changelist_view(self, request, extra_context=None):

        search_term = request.GET.get("q", "").strip()

        answer = None
        related_documents = []

        if search_term:

            documents = []

            for obj in UploadFile.objects.all():

                if not obj.file:
                    continue

                try:
                    with obj.file.open("r") as file:
                        content = file.read()

                except Exception:
                    continue

                # Search inside filename OR file content
                if (
                    search_term.lower() in (obj.name or "").lower()
                    or search_term.lower() in content.lower()
                ):

                    related_documents.append(obj)

                    documents.append(
                        f"""
                        FILE NAME: {obj.name}
                        FILE ID: {obj.id}

                        CONTENT:
                        {content}
                        """
                    )

            if documents:

                document_content = "\n\n".join(documents)

                answer = ask_question(
                    search_term,
                    document_content,
                )

            else:
                answer = "No relevant documents were found."

        extra_context = extra_context or {}

        extra_context.update({
            "llm_answer": answer,
            "related_documents": related_documents,
            "search_term": search_term,
        })

        return super().changelist_view(
            request,
            extra_context=extra_context,
        )


    def download_button(self, obj):
        if not obj.file:
            return "-"

        url = reverse(
            "llm:download_file",
            args=[obj.id]
        )

        return format_html(
            '<a class="button" href="{}">Download</a>',
            url
        )

    download_button.short_description = "Download"


