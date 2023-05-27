import re
import logging

from urllib.parse import urljoin
import requests_cache
from bs4 import BeautifulSoup
from requests import RequestException
from tqdm import tqdm

from outputs import control_output
from constants import (
    BASE_DIR,
    MAIN_DOC_URL,
    PEP_DOC_URL,
    EXPECTED_STATUS,
    AMOUNT_STATUS,
)
from configs import configure_argument_parser, configure_logging
from utils import get_response, find_tag


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, "whatsnew/")
    session = requests_cache.CachedSession()
    response = get_response(session, whats_new_url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, features="lxml")
    main_div = find_tag(soup, "section", attrs={"id": "what-s-new-in-python"})
    div_with_ul = find_tag(main_div, "div", attrs={"class": "toctree-wrapper"})
    sections_by_python = div_with_ul.find_all("li",
                                              attrs={"class": "toctree-l1"})
    result = [("Ссылка на статью", "Заголовок", "Редактор, Автор")]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find("a")
        href = version_a_tag["href"]
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, features="lxml")
        h1 = find_tag(soup, "h1").getText()
        dl = soup.find("dl").text.replace("\n", " ")
        result.append((version_link, h1, dl))
    return result


def latest_versions(session):
    session = requests_cache.CachedSession()
    response = get_response(session, MAIN_DOC_URL)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    sidebar = soup.find("div", {"class": "sphinxsidebarwrapper"})
    ul_tags = sidebar.find_all("ul")
    for ul in ul_tags:
        if "All versions" in ul.text:
            a_tags = ul.find_all("a")
            break
    else:
        raise RequestException("Не найден список c версиями Python")
    result = [("Ссылка на документацию", "Версия", "Статус")]
    pattern = r"Python (?P<version>\d\.\d+) \((?P<status>.*)\)"
    for a_tag in a_tags:
        link = a_tag["href"]
        text_match = re.search(pattern, a_tag.text)
        version, status = text_match.groups() if text_match else a_tag.text, ""
        result.append((link, version, status))
    return result


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, "download.html")
    downloads_dir = BASE_DIR / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    session = requests_cache.CachedSession()
    response = session.get(downloads_url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    main_tag = soup.find("div", {"role": "main"})
    table_tag = main_tag.find("table", {"class": "docutils"})
    pdf_a4_tag = table_tag.find("a", {"href": re.compile(r".+pdf-a4\.zip$")})
    pdf_a4_link = pdf_a4_tag["href"]
    archive_url = urljoin(MAIN_DOC_URL, pdf_a4_link)
    filename = archive_url.split("/")[-1]
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, "wb") as file:
        file.write(response.content)
    logging.info(f"Архив был загружен и сохранён: {archive_path}")
    print(archive_url)


def pep(session):
    session = requests_cache.CachedSession()
    response = session.get(PEP_DOC_URL)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    main_tag = soup.find_all("table", {"class": "pep-zero-table"})
    result = [("Статус", "Количество")]
    for table in main_tag:
        tr_tag = table.find_all("tr", {"class": re.compile(r"^row-.*")})
        for tr in tr_tag:
            abbr_tag = tr.find("abbr")
            links = tr.find("a", {"class": "pep"})
            if abbr_tag is None or links is None:
                continue
            href = links["href"]
            pep_link = urljoin(PEP_DOC_URL, href)
            pep_response = session.get(pep_link)
            if pep_response is None:
                continue
            pep_response.encoding = "utf-8"
            pep_soup = BeautifulSoup(pep_response.text, features="lxml")
            status = find_tag(pep_soup, "abbr")
            if status.text not in EXPECTED_STATUS[abbr_tag.text[1:]]:
                logging.info("Несовпадающие статусы:")
                logging.info(f"{pep_link}")
                logging.info(f"Статус в карточке: {str(status.text)}")
                logging.info(
                    (f"Ожидаемые статусы:",
                     f" {EXPECTED_STATUS[abbr_tag.text[1:]][0]}")
                )
                continue
            AMOUNT_STATUS[abbr_tag.text[1:]] = (
                AMOUNT_STATUS[abbr_tag.text[1:]] + 1
            )
    total = 0
    for keys, values in AMOUNT_STATUS.items():
        total = total + int(values)
        result.append((keys, values))
    result.append(("Total", total))
    return result


MODE_TO_FUNCTION = {
    "whats-new": whats_new,
    "latest-versions": latest_versions,
    "download": download,
    "pep": pep,
}


def main():
    configure_logging()
    logging.info("Парсер запущен!")
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f"Аргументы командной строки: {args}")
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    result = MODE_TO_FUNCTION[parser_mode](session)
    if result is not None:
        control_output(result, args)
    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
