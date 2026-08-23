from django.shortcuts import render,redirect
from .models import UploadFile,Comment
from .forms import UploadFileForm,CommentForm
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
import openai,os
from dotenv import load_dotenv
from openai import OpenAI
import environ
# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

load_dotenv(override=True)
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# api_key = os.getenv("OPENAI_API_KEY",None)

# openai.api_key = api_key
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# client = OpenAI(api_key=api_key)

# response = client.chat.completions.create(model="gpt-3.5turbo-", messages=[{"role": "user", "content": "count 1 to 10"}])
# print(response.choices[0].message.content)
# response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "mention five words"}], temperature=0.1)
# print(response.choices[0].message.content)


def ask_question(request):
    pass
    
    # answer = None
    # if request.method == "POST":
    #     question = request.POST.get("question")
    #     uploadfiles = UploadFile.objects.all()
    #     document_content = ""
    #     for uploadfile in uploadfiles:
    #         if uploadfile.file:
    #             with uploadfile.file.open("r") as file:
    #                 content = file.read()
    #                 document_content += content + "\n\n"
    #     answer = ask_llm(question,document_content)
    # return render(request,"uploads/upload.html",{"answer": answer,})


def upload_file(request):
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "count 1 to 10"}])
    # print(response.choices[0].message.content)
    answer=None
    form=UploadFileForm()
    uploadfiles=UploadFile.objects.all()
    if request.method=="POST":
        question = request.POST.get("question")
        print(1)
        if question is not None:
            document_content = ""
            print(2)
            for uploadfile in uploadfiles:
                print(3)
                for uploadfile in uploadfiles:
                    print(4)
                    if uploadfile.file:
                        print(5)
                        with uploadfile.file.open(mode="r") as file:
                            content = file.read()
                            document_content += content + "\n\n"
                            print(6)
                            print(document_content)
            # answer = ask_llm(question,document_content)
            answer = document_content
            print(answer)
            try:
                response = client.responses.create(model="gpt-5.6-mini",input=answer)
                print(20,response)
                # response = client.responses.create(model="gpt-5.6-luna",input=answer)
                response1 = client.responses.create(model="gpt-5.6",input=answer)
                print(11,response1)
                context={
                'answer':response,
                }
                return render(request,'uploads/upload.html',context)  
            except Exception as e:
                error=str(e)
                context={'error':error}
                return render(request,'uploads/upload.html',context)      
        form=UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            form2=form.save(commit=False)
            form2.author = request.user
            form2.save()
            return redirect('llm:upload_file')
    else:
        uploadfiles=UploadFile.objects.all()
        form=UploadFileForm()
        context={
            'form':form,
            'uploadfiles':uploadfiles,
        }
        return render(request,'uploads/upload.html',context)

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
        # if os.path.isfile(uploadfile.file):
        #     os.remove(uploadfile.file.path)
            uploadfile.delete()
            return redirect('llm:upload_file')
        # else:
        #     return HttpResponse("not found file path")
    else:
        return HttpResponse("error")
        



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