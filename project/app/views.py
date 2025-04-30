from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .notes import get_youtube_transcript, neutralize_text, summarize_text, extract_key_points, generate_word
from docx import Document
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index.html')

def results(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        languages = ['en', 'fr', 'hi']
        transcript = get_youtube_transcript(video_url, languages)
        if "Error" not in transcript and "Invalid" not in transcript:
            notes = neutralize_text(transcript)
            summary = summarize_text(transcript)
            key_points = extract_key_points(transcript)
            context = {
                'notes': notes,
                'summary': summary,
                'key_points': key_points,
            }
            return render(request, 'results.html', context)
        else:
            context = {
                'error': transcript
            }
            return render(request, 'results.html', context)
    return render(request, 'results.html')

@csrf_exempt  # Disable CSRF for simplicity (use cautiously in production)
def generate_word_file(request):
    if request.method == 'POST':
        text = request.POST.get('text', 'No content provided')  # Get text from the POST request
        word_file = generate_word(text)  # Use the generate_word function from notes.py

        # Create an HTTP response with the Word file as an attachment
        response = HttpResponse(word_file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="generated_file.docx"'

        return response
    return HttpResponse("Invalid request method", status=405)


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def features(request):
    return render(request, 'features.html')
