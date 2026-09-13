from django.shortcuts import render
from django.http import HttpResponse

from main.models import Experience, Education

# Create your views here.
# View menangani logika yang akan ditampilkan kepada pengguna. 
def show_main(request):
    context = {
        "name": "Silvia Lalita Damayanti",
        "first_name": "Silvia",
        "nick_name": "Lalita",
        "last_name": "Damayanti",
        "npm": "2506621863",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "I am an undergraduate Computer Science student who enjoys exploring the intersection of design and technology, "
            "with a particular interest in Digital Product Design. I love creating things, learning new skills, and developing innovative and impactful solutions through design."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Silvia Lalita Damayanti",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Silvia Lalita Damayanti",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)