# views.py
from django.shortcuts import render, get_object_or_404, redirect  # ✅
from django.http import HttpResponse, Http404
from django.urls import reverse
from .models import Result
from .forms import ResultSearchForm
from .utils import generate_result_pdf
import csv
import json
from io import TextIOWrapper
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

def result_search(request):
    if request.method == 'POST':
        form = ResultSearchForm(request.POST)
        if form.is_valid():
            roll_no = form.cleaned_data['roll_no']
            try:
                result = Result.objects.get(roll_no=roll_no)
                return render(request, 'results/result_detail.html', {'result': result})
            except Result.DoesNotExist:
                return render(request, 'results/search.html', {
                    'form': form,
                    'error': 'No result found for the provided credentials'
                })
        return render(request, 'results/search.html', {'form': form})
    else:
        form = ResultSearchForm()
    return render(request, 'Results/search.html', {'form': form})

def result_detail(request, roll_no):
    try:
        result = get_object_or_404(Result, roll_no=roll_no)
        return render(request, 'Results/result_detail.html', {'result': result})
    except Result.DoesNotExist:
        raise Http404("Result not found")

def result_pdf(request, roll_no):
    result = get_object_or_404(Result, roll_no=roll_no)
    response = generate_result_pdf(result)
    return response

# views.py
# upload csv file function

def handle_csv_upload(csv_file):
    decoded_file = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    
    created_count = 0
    updated_count = 0
    errors = []

    for row_num, row in enumerate(reader, start=2):  # Row numbers start from 2 (header is row 1)
        try:
            # Convert stringified JSON to Python dict
            row['subject_details'] = json.loads(row['subject_details'].replace("'", '"'))
            
            # Convert exam_year to integer
            row['exam_year'] = int(row['exam_year'])
            
            # Create or update record
            obj, created = Result.objects.update_or_create(
                roll_no=row['roll_no'],
                defaults={
                    'name': row['name'],
                    'father_name': row['father_name'],
                    'mother_name': row['mother_name'],
                    'year_sem': row['year_sem'],
                    'exam_month': row['exam_month'],
                    'exam_year': row['exam_year'],
                    'subject_details': row['subject_details'],
                }
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1
                
        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
    
    return created_count, updated_count, errors

ALLOWED_MIME_TYPES = ['text/csv', 'application/vnd.ms-excel']

@staff_member_required
def upload_results(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Invalid file format')
            
            return redirect(reverse('upload_results'))
        
        try:
            # Validate MIME type
            if csv_file.content_type not in ['text/csv', 'application/vnd.ms-excel']:
                messages.error(request, 'Invalid file type')
                
            return redirect('upload_results')
            
            created, updated, errors = handle_csv_upload(csv_file)
            
            msg = [
                f"Successfully uploaded!",
                f"New records: {created}",
                f"Updated records: {updated}",
            ]
            
            if errors:
                msg.append(f"Errors: {len(errors)}")
                messages.warning(request, '<br>'.join(msg))
                request.session['upload_errors'] = errors
            else:
                messages.success(request, '<br>'.join(msg))
                
            return redirect('upload_results')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('upload_results')
    
    errors = request.session.pop('upload_errors', None)
    return render(request, 'Results/upload.html', {'errors': errors})  # Fixed template path