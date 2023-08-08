import requests
from tqdm import tqdm

URL_HH = 'https://api.hh.ru/vacancies'


def get_vacancies(companies) -> list:
    print(f'\nПолучаем данные с {URL_HH}...')
    vacancies = []
    the_list = []
    for company in tqdm(companies, ncols=100, desc='Получаем вакансии от компаний'):
        # print(f'Получаем данные для компании {companies[company]}...')
        params = {
            'employer_id': company,
            'page': 0,
            'per_page': 100,
            'only_with_salary': True
        }
        response = requests.get(URL_HH, params)
        result_page = response.json()
        vacancies.extend(result_page['items'])
        while len(result_page['items']) == 100:
            params['page'] += 1
            response = requests.get(URL_HH, params)
            result_page = response.json()
            if result_page.get('items'):
                vacancies.extend(result_page['items'])
            else:
                break
        for vacancy in result_page['items']:
            the_list.append({
                'company_name': vacancy['employer']['name'],
                'vacancy_name': vacancy['name'],
                'vacancy_salary_from': vacancy['salary']['from'],
                'vacancy_salary_to': vacancy['salary']['to'],
                'vacancy_url': vacancy['url']
            })
        vacancies.clear()
    print(f'Всего вакансий {len(the_list)} загружено')
    return the_list
