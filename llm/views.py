from django.shortcuts import render,redirect
from .models import UploadFile,Comment
from .forms import UploadFileForm,CommentForm,SignUpForm
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse,Http404,FileResponse
from django.core.files.storage import default_storage
import openai,os
from dotenv import load_dotenv
from openai import OpenAI
import environ,time,requests
from .services import ask_question #get_batch


# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

load_dotenv()
load_dotenv(override=True)
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))







def download_file(request, id):
    try:
        uploadfile = UploadFile.objects.get(id=id)
    except UploadFile.DoesNotExist:
        raise Http404("File not found")

    if not uploadfile.file:
        raise Http404("No file available")

    return FileResponse(
        uploadfile.file.open("rb"),
        as_attachment=True,
        filename=uploadfile.file.name.split("/")[-1],
    )


def upload_file(request):
    answer = None
    question = ""
    form = UploadFileForm()
    uploadfiles = UploadFile.objects.all()

    if request.method == "POST":

        question = request.POST.get("question", "").strip()

        if question:
            related_documents = []

            for uploadfile in uploadfiles:

                if not uploadfile.file:
                    continue

                with uploadfile.file.open(mode="r") as file:
                    content = file.read()

                # Check if search text exists in file name or content
                if (
                    question.lower() in (uploadfile.name or "").lower()
                    or question.lower() in content.lower()
                ):
                    related_documents.append({
                        "id": uploadfile.id,
                        "name": uploadfile.name,
                        "content": content,
                    })

            # Send ONLY related documents to OpenRouter
            document_content = "\n\n".join(
                f"""
                FILE NAME: {doc['name']}
                FILE ID: {doc['id']}

                CONTENT:
                {doc['content']}
                """
                for doc in related_documents
            )

            if related_documents:
                answer = ask_question(
                    question,
                    document_content
                )
            else:
                answer = "No relevant information was found in the documents."

            context = {
                "form": form,
                "uploadfiles": uploadfiles,
                "answer": answer,
                "documents": related_documents,
                "related_documents": related_documents,
                "question": question,
            }

            return render(
                request,
                "uploads/upload.html",
                context
            )

        # Upload a new file
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            form2 = form.save(commit=False)
            form2.author = request.user
            form2.save()

            return redirect("llm:upload_file")
    
    else:
        form = UploadFileForm()

        return render(
            request,
            "uploads/upload.html",
            {
                "form": form,
                "uploadfiles": uploadfiles,
                "answer": answer,
                "question": question,
                "related_documents": [],
                "documents": [],
            }
        )



def edite_file(request,id):
    uploadfile=UploadFile.objects.get(id=id)
    form=UploadFileForm()
    if request.method=="POST":
        form=UploadFileForm(request.POST,request.FILES,instance=uploadfile)
        # uploadfile1=uploadfile.file
        if form.is_valid():
            # form2=form.file
            form2=form.save(commit=False)
            form2.author = request.user
            file =form.cleaned_data["file"]
            newupload=UploadFile(name=form.cleaned_data["name"],text=form.cleaned_data["text"],file=file,author=request.user)
            newupload.save()
            form2.save()
            uploadfile.delete()
            return redirect("llm:upload_file")
        else:
            return HttpResponse("error")
            
    else:
        form=UploadFileForm()
        uploadfile=UploadFile.objects.get(id=id)
        context={
            "form":form,
            'uploadfile':uploadfile,
            # 'content':content
        }
        return render(request,"uploads/edite.html",context)


def delete_file(request,id):
    uploadfile=UploadFile.objects.get(id=id)
    user=User.objects.get(username=request.user.username)
    if user==uploadfile.author or request.user.is_superuser :
        # delete file from media
        file_path = uploadfile.file.name 
        if file_path and default_storage.exists(file_path):
            default_storage.delete(file_path)
        # delete oject from database
        uploadfile.delete()
        return redirect('llm:upload_file')
    else:
        return HttpResponse("you don't have permission to delet this item")
        


def read_file(request, id):
    uploadfile = UploadFile.objects.get(id=id)

    with uploadfile.file.open(mode='r') as file:
        content = file.read()
        # print(999999999999999999999999999999999999)
        # print(content)
        # print(999999999999999999999999999999999)
        # content.close()
    
    return render(
        request,
        'uploads/read.html',
        {
            'uploadfile': uploadfile,
            'content': content,
        }
    )


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(form.cleaned_data["password"])

            user.save()

            return redirect("login")

    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})



# def upload_file(request):
#     answer=None
#     form=UploadFileForm()
#     uploadfiles=UploadFile.objects.all()
#     if request.method=="POST":
#         question = request.POST.get("question").strip()
#         related_documents = []
#         documents = []
#         if question is not None:
#             document_content = ""
#             for uploadfile in uploadfiles:
#                     if uploadfile.file:
#                         with uploadfile.file.open(mode="r") as file:
#                             content = file.read()
#                             document = {
#                             "id": uploadfile.id,
#                             "name": uploadfile.name,
#                             "content": content,
#                             }

#                     documents.append(document)

#                     # # Find related documents
#                     if question.lower() in content.lower():
#                         related_documents.append(document)
#                         documents.append({
#                                 "id": uploadfile.id,
#                                 "name": uploadfile.name,
#                                 "content": content,
#                         })
#                             # documents.append(f"""File name: {uploadfile.name} Content:{content}""") 
#             # document_content = "\n\n".join(documents)
#             documents.append(document)

#                     # Find related documents
#             if question.lower() in content.lower():
#                 related_documents.append(documents)
#             document_content = "\n\n".join(
#                 f"""
#             FILE NAME: {doc['name']}
#             FILE ID: {doc['id']}

#             CONTENT:
#             {doc['content']}
#             """
#                 for doc in documents
#             )
#             answer = ask_question(question,document_content)
            
#             context = {
#             "form": form,
#             "uploadfiles": uploadfiles,
#             "answer": answer,
#             "documents": documents,
#             "related_documents": documents,
#             "question": question,
#             "related_documents": related_documents,

#             }
#             return render(request,'uploads/upload.html',context)
            
#         form=UploadFileForm(request.POST,request.FILES)
#         if form.is_valid():
#             form2=form.save(commit=False)
#             form2.author = request.user
#             form2.save()
#             return redirect('llm:upload_file')
#     else:
        # uploadfiles=UploadFile.objects.all()
        # form=UploadFileForm()
        # context={
        #     'form':form,
        #     'uploadfiles':uploadfiles,
        # }
        # return render(request,'uploads/upload.html',context)