from django.shortcuts import render, redirect
import requests
from .forms import UserRegisterForm
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import get_info_by_title
from dateutil import parser
from datetime import datetime as dt
from datetime import timedelta


def home(request):
    is_logged = request.user.is_authenticated
    return render(request, 'main/home.html', {'is_logged': is_logged})


def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Вы успешно зарегистрировались')
            form.save()
            return redirect('login')
        else:
            return render(request, 'main/registration.html', {'form': form})

    form = UserRegisterForm()
    return render(request, 'main/registration.html', {'form': form})


def logout(request):
    logout_user(request)
    return redirect('home')


@login_required()
def demand(request):
    img_salary_all, table_salary_all, img_salary_qa, table_salary_qa = get_info_by_title('salary_by_year')
    img_count_all, table_count_all, img_count_qa, table_count_qa = get_info_by_title('count_by_year')

    return render(request, 'main/demand.html', {
        'is_logged': request.user.is_authenticated,
        'img_salary_all': img_salary_all,
        'table_salary_all': table_salary_all,
        'img_salary_qa': img_salary_qa,
        'table_salary_qa': table_salary_qa,
        'img_count_all': img_count_all,
        'table_count_all': table_count_all,
        'img_count_qa': img_count_qa,
        'table_count_qa': table_count_qa
    })


@login_required()
def geography(request):
    img_salary_all, table_salary_all, img_salary_qa, table_salary_qa = get_info_by_title('salary_by_city')
    img_count_all, table_count_all, img_count_qa, table_count_qa = get_info_by_title('count_by_city')

    return render(request, 'main/geography.html',  {
        'is_logged': request.user.is_authenticated,
        'img_salary_all': img_salary_all,
        'table_salary_all': table_salary_all,
        'img_salary_qa': img_salary_qa,
        'table_salary_qa': table_salary_qa,
        'img_count_all': img_count_all,
        'table_count_all': table_count_all,
        'img_count_qa': img_count_qa,
        'table_count_qa': table_count_qa
    })


@login_required()
def skills(request):
    img_skills_all, table_skills_all, img_skills_qa, table_skills_qa = get_info_by_title('top_skills')
    table_skills_all = list(map(lambda s: (s[0], tuple(s[1].items())), list(table_skills_all)))
    table_skills_qa = list(map(lambda s: (s[0], tuple(s[1].items())), list(table_skills_qa)))

    return render(request, 'main/skills.html',  {
        'is_logged': request.user.is_authenticated,
        'img_skills_all': img_skills_all,
        'table_skills_all': table_skills_all,
        'img_skills_qa': img_skills_qa,
        'table_skills_qa': table_skills_qa,
    })


@login_required()
def last_vacancies(request):

    def get_value_by_keys(obj, *keys, no_info_msg='Не указано'):
        try:
            result = obj
            for key in keys:
                result = result[key]
            return result
        except:
            return no_info_msg

    def prepare_data(obj):
        vacancy_id = obj['id']
        response = requests.get(f'https://api.hh.ru/vacancies/{vacancy_id}').json()
        description = get_value_by_keys(response, 'description')

        all_skills = ', '.join(map(lambda d: d['name'], response['key_skills']))
        if not all_skills:
            all_skills = 'Не указано'

        currency = get_value_by_keys(obj, 'salary', 'currency', no_info_msg='')
        published_at = dt.strftime(parser.parse(obj['published_at']), '%d.%m.%Y %H:%M')
        address = get_value_by_keys(obj, 'address', 'city')
        avg_salary = get_value_by_keys(obj, 'salary', 'from')
        employer_name = get_value_by_keys(obj, 'employer', 'name')

        return {
            **obj,
            'published_at': published_at,
            'address': address,
            'salary': {
                'currency': currency,
                'avg_salary': avg_salary,
            },
            'employer_name': employer_name,
            'description': description,
            'all_skills': all_skills
        }

    time = (dt.utcnow() - timedelta(hours=24)).isoformat()
    synonyms = 'QA OR Тестировщик OR "quality assurance" OR test OR qa'
    url = f'https://api.hh.ru/vacancies?text={synonyms}&search_field=name&date_from={time}&order_by=publication_time&per_page=10'
    response = requests.get(url)
    vacancies = response.json()['items']
    vacancies = list(map(prepare_data, vacancies))

    return render(request, 'main/last_vacancies.html',  {
        'is_logged': request.user.is_authenticated,
        'vacancies': vacancies
    })
