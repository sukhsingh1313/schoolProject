from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    admission_year = models.PositiveIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )

    class Meta:
        ordering = ['-admission_year', 'roll_no']  # Fixed here
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"

    def __str__(self):
        return f"{self.roll_no} - {self.user.get_full_name()}"  # Fixed here

class Result(models.Model):
    EXAM_TYPE_CHOICES = [
        ('REGULAR', 'Regular'),
        ('BACK', 'Back Paper'),
        ('SPECIAL', 'Special Exam'),
    ]

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='results',
    )

    year_sem = models.CharField(
        max_length=10,
        help_text="Current academic year/semester"
    )

    exam_month = models.CharField(max_length=20)
    exam_year = models.PositiveIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )
    exam_type = models.CharField(
        max_length=10,
        choices=EXAM_TYPE_CHOICES,
        default='REGULAR'
    )

    subject_details = models.JSONField(
        help_text="Stores subject codes with marks and grades in JSON format"
    )

    marks_obtained = models.PositiveIntegerField(editable=False)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        editable=False
    )
    result_status = models.CharField(
        max_length=20,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student Result"
        verbose_name_plural = "Student Results"
        indexes = [
            models.Index(fields=['student', 'exam_year']),
        ]
        ordering = ['-exam_year', 'student__roll_no']  # Fixed here
        unique_together = ['student', 'exam_year', 'exam_type']

    def __str__(self):
        return f"{self.student.roll_no} - {self.exam_year} {self.exam_type}"  # Fixed here

    def save(self, *args, **kwargs):
        self.calculate_results()
        self.full_clean()
        super().save(*args, **kwargs)

    def calculate_results(self):
        subjects = self.subject_details.values()
        total_marks = sum(int(subj['marks']) for subj in subjects)
        total_subjects = len(subjects)

        if total_subjects == 0:
            raise ValueError("At least one subject must be provided")

        self.marks_obtained = total_marks
        self.percentage = (total_marks / (total_subjects * 100)) * 100
        self.result_status = 'PASS' if self.percentage >= 40.0 else 'FAIL'

    @property
    def formatted_percentage(self):
        return f"{self.percentage:.2f}%"

    @property
    def total_marks(self):
        return len(self.subject_details) * 100

    @property
    def subject_list(self):
        return [
            {
                'code': code,
                'name': details.get('subject_name', code),
                'marks': details['marks'],
                'grade': details['grade']
            }
            for code, details in self.subject_details.items()
        ]
