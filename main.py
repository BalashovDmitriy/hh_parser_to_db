import json

from utils.utils import get_vacancies

companies = {
    1776381: "CATAPULTO.RU",
    2324020: "Точка",
    864086: "getmatch.ru",
    2723603: "aerodisk.ru",
    3407499: "hwschool.online",
    80660: "boxberry",
    1008541: "mipt.ru",
    2970204: "otus.ru",
    4759060: "hrprime.ru",
    5569859: "arktech.ai"
}

if __name__ == '__main__':
    print(json.dumps(get_vacancies(companies), indent=2, ensure_ascii=False))
