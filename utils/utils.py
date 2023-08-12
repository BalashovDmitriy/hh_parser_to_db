import json

import requests
import psycopg2
from tqdm import tqdm

URL_HH = 'https://api.hh.ru/vacancies'


def get_vacancies(companies) -> list:
    """Получаем вакансии от компаний"""
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
                'company_id': vacancy['employer']['id'],
                'company_name': vacancy['employer']['name'],
                'vacancy_name': vacancy['name'],
                'vacancy_salary_from': vacancy['salary']['from'],
                'vacancy_salary_to': vacancy['salary']['to'],
                'vacancy_url': vacancy['url']
            })
        vacancies.clear()
    with open('vacancies.json', 'w') as f:
        f.write(json.dumps(the_list, indent=2, ensure_ascii=False))
    return the_list


def create_db(db_name, params):
    """Создаём базу данных"""
    connection = psycopg2.connect(dbname='postgres', **params)
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
    cursor.execute(f"CREATE DATABASE {db_name};")

    cursor.close()
    connection.close()


def create_tables(cursor, script_file):
    """Создаём таблицы с данными"""
    with open(script_file, 'r') as f:
        script = f.read()
    cursor.execute(script)


def fill_table_companies(cursor, companies):
    """Заполняем таблицу с данными компаний"""
    for company_id, company in companies.items():
        cursor.execute("INSERT INTO companies (company_id, company) VALUES (%s, %s)", (company_id, company))


def fill_table_vacancies(cursor, vacancies):
    """Заполняем таблицу с вакансиями"""
    for vacancy in vacancies:
        cursor.execute("INSERT INTO vacancies (company_id, vacancy_name, salary_from, "
                       "salary_to, url) VALUES (%s, %s, %s, %s, %s)",
                       (vacancy['company_id'], vacancy['vacancy_name'], vacancy['vacancy_salary_from'],
                        vacancy['vacancy_salary_to'], vacancy['vacancy_url']))
