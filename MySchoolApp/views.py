from django.shortcuts import render,redirect,HttpResponse,get_object_or_404,HttpResponseRedirect
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.

def home(request):
    slides = HomeBenner.objects.all()
    notification = notificationModel.objects.all()
    query = request.GET.get('search', '')
    news_session = News_session.objects.filter(news_title__icontains=query) if query else News_session.objects.all()
    event_model = Events.objects.all()

    paginator = Paginator(news_session,2)
    #get the current page number from the request
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'slides' :slides,
        'notification':notification,
        'event_model':event_model,
        'page_obj':page_obj,
        'query': query,

    }
    return render(request,'index.html',context)



def NewsView(request ,slug = None):
    news_session = get_object_or_404(News_session,slug=slug)
    return render(request,'news_post.html',{'news_session':news_session})

def add_comment(request,id):
    if request.method == 'POST':
        news_post = get_object_or_404(News_session,id=id)
        author = request.POST.get('author')
        comment_text = request.POST.get('comment_text')
        Comment.objects.create(news_post=news_post, author=author, comment_text=comment_text)
        return redirect('NewsView', slug=news_post.slug)
    
def archive(request,slug):
    archive = get_object_or_404(Archive,slug=slug)
    return HttpResponse('do not have more information',{'archive':archive})
 


# about view section


def about_view(request,slug=None):
    if slug:
        notification = get_object_or_404(notificationModel, slug=slug)
        is_multiple = False
    else:
        notification = notificationModel.objects.all()
        is_multiple = True
    history = SchoolHistory.objects.last()
    mission = SchoolMission.objects.last()
    vision = SchoolVision.objects.last()
    core_values = CoreValues.objects.all()
    staff_members = StaffMember.objects.all() 
    facilities = Facility.objects.all()

    context = {
        'history': history,
        'mission': mission,
        'vision': vision,
        'core_values': core_values,
        'notification':notification,
        'is_multiple': is_multiple,
        'staff_members': staff_members,
        'facilities': facilities,
    }
    return render(request,'about.html',context)


#accademic view session
def academic_view(request):
    curriculem = Curriculm.objects.all()
    class_obj = Class.objects.all()
    timetables = TimetableEntry.objects.all()
    context = {
        'class_obj':class_obj,
        'curriculem':curriculem,
        'timetables':timetables,
    }
    return render(request,'academics.html',context)

def Class_timetable(request,id):
    class_obj = get_object_or_404(Class,id=id)
    timetable_entries = TimetableEntry.objects.filter(class_assigned = class_obj).order_by('day_of_week','start_time')
    context  = {
        'class_obj':class_obj,
        'timetable_entries':timetable_entries,
    }
    return render(request,'class_timetable.html',context)
