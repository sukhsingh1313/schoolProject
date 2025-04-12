from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

# Home


class HomeBenner(models.Model):
    titlefirst = models.CharField(max_length=100,null=True,blank=True)
    highlightwords = models.CharField(max_length=50,null=True,blank=True)
    titlesecond = models.CharField(max_length=100,null=True,blank=True)
    video = models.FileField(upload_to='slides/videos/', blank=True, null=True)
    image = models.ImageField(upload_to="", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titlefirst


class notificationModel(models.Model):
    name  = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    notify_img  = models.ImageField(upload_to="")
    url = models.URLField(null= True, blank=True)
    # new_old = models.CharField( max_length=50 ,null=True,blank=True)
    updated = models.DateTimeField(auto_now_add=True,auto_created=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(notificationModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Events(models.Model):
    name = models.CharField(max_length=100)
    event_link = models.URLField(blank=True,null=True)
    description = models.TextField(null=True,blank=True)
    event_location = models.CharField(max_length=100,null=True,blank=True)
    event_day = models.IntegerField( blank=True,null=True)
    event_month = models.CharField(max_length=20,blank=True,null=True)
    image = models.ImageField(upload_to="",blank=True,null=True)
    updated = models.DateTimeField(auto_now_add=True,auto_created=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Events, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class News_session(models.Model):
    news_title = models.CharField(max_length=100)
    short_post_text = models.TextField(max_length=1000)
    news_post_quote = models.TextField(null=True,blank=True)
    news_post_text = models.TextField(null=True,blank=True)
    post_author = models.CharField(max_length=50,blank=True,null=True)
    news_day = models.IntegerField( blank=True,null=True)
    news_month = models.CharField(max_length=20,blank=True,null=True)
    news_image = models.ImageField(upload_to="")
    news_url = models.URLField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.news_title}")
        super(News_session, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.post_author} {self.news_day}"
 
     # Latest post logic
    @classmethod
    def get_latest_post(cls):
        return cls.objects.latest('created_at')
    

class Comment(models.Model):
    news_post = models.ForeignKey(News_session, related_name="comments", on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author}"
    




class Archive(models.Model):
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    news_session = models.ForeignKey(News_session, on_delete=models.CASCADE,related_name="archives")
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.month}-{self.year}")
        super(Archive, self).save(*args, **kwargs)

    def __str__(self):
        return f"Archive for {self.month} {self.year}"





#about models
class SchoolHistory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='school_history/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
class SchoolMission(models.Model):
    title = models.CharField(max_length=255)
    mission_statement = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class SchoolVision(models.Model):
    title = models.CharField(max_length=255)
    vision_statement = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class CoreValues(models.Model):
    value_name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value_name
    


#show staff detail in about page ==>

class deppartment(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name






class StaffMember(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='', null=True, blank=True)
    deppartment = models.ForeignKey(deppartment,on_delete= models.CASCADE,related_name='staff_details')
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.designation}"



class Facility(models.Model):
    name = models.CharField(max_length=100)  # Facility name (e.g., Library, Sports Ground)
    description = models.TextField()  # Details about the facility
    image = models.ImageField(upload_to='', null=True, blank=True)  # Optional facility image

    def __str__(self):
        return self.name
    




#academic models:-
class Class(models.Model):
    name  = models.CharField(max_length=50) #Example : 10th,12th
    section = models.CharField(max_length=10,blank=True,null=True) #example : 'A',"B"

    def __str__(self):
        return f"{self.name} - {self.section if self.section else "" }"
    

class Subject(models.Model):
    name = models.CharField(max_length=100)  # Subject name (e.g., Mathematics,
    code = models.CharField(max_length=20, unique=True)
    # class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="subjects")

    def __str__(self):
     return f"{self.name} ({self.code})"

class Teacher(models.Model):
    name  = models.ForeignKey(StaffMember,on_delete= models.CASCADE,related_name="teacher_name")
    subject = models.ManyToManyField(Subject, related_name="teachers")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,blank=True,null=True)

    def __str__(self):
        return str(self.name)
    


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

#pass is complete
class Curriculm(models.Model):
    class_assigned = models.ForeignKey(Class,on_delete=models.CASCADE,related_name="curriculums")
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='curriculum_images/', blank=True, null=True)  # optional image field
    document = models.FileField(upload_to='curriculum_documents/', blank=True, null=True)

    def __str__(self):
        return f"Curriculum for {self.class_assigned.name} - {self.subject.name}"
    

class TimetableEntry(models.Model):
    class_assigned = models.ForeignKey(Class,on_delete=models.CASCADE, related_name='timetable_entries')
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='timetable_entries')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='timetable_entries')
    day_of_week = models.CharField(max_length=10,choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday')
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    # slug = models.SlugField()

    def __str__(self):
        return f"{self.class_assigned.name} - {self.subject.name} ({self.day_of_week})"
  



