import re
import requests
from bs4 import BeautifulSoup
from app.db.schemas import ShopInfoBase


def get_translated_field(obj, lang: str, field_base_name: str):
    field_name = f"{field_base_name}_{lang}"
    return getattr(obj, field_name, None)


headers = {
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64, x64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/120.0.0.0"
                  " Safari/531.36",
    "Accept_Language": "uz-UZ, uz;q=0.5",
    "Referer": "https://orginfo.uz",
    "Connection": "keep-alive"
}


def send_request(inn: int):
    base_url = f"https://orginfo.uz/search?q={inn}"
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        org_link = soup.find("a", href=True, class_="text-decoration-none og-card")
        if org_link:
            org_url = f"https://orginfo.uz{org_link['href']}"
            org_response = requests.get(org_url, headers=headers)
            org_soup = BeautifulSoup(org_response.text, 'html.parser')
            return soup, org_url, org_soup
    else:
        raise Exception("Ma'lumot olishda xatolik yuz berdi !")


def get_company_name(soup):
    org_name_tag = soup.find("h6")
    return org_name_tag.text.strip() if org_name_tag else "Tashkilot topilmadi !"


def get_location(soup):
    location_tag = soup.find("p", class_="text-body-tertiary")
    if location_tag:
        return re.sub(r"\s+", " ", location_tag.text.replace('location', '').strip())
    return "Address-ni olib bo'lmadi !"


def get_founders(org_url):
    response = requests.get(org_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        founders = soup.find_all("a", href=True, class_="text-success text-body-hover text-decoration-none")
        return [founder.text.strip() for founder in founders] if founders else ["Taʼsischilar topilmadi"]
    return ["URL ochilmadi"]


def get_authorized_fund(organization_page_ur):
    response = requests.get(organization_page_ur, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    auth_fund = soup.find_all("span", class_="bg-success bg-opacity-10 text-success px-2 py-1 rounded-3")
    if len(auth_fund) > 1:
        return re.sub(r"\s+", " ", auth_fund[1].text.strip())
    return "Ustav fondi topilmadi !"


def get_register_date(soup):
    reg_str_tag = soup.find_all("span", string="Дата регистрации")
    if reg_str_tag:
        for tag in reg_str_tag:
            register_date = tag.find_parent("div").find_next_sibling("div").find("span").text.strip()
            if register_date:
                return register_date
    return "Ro'yxatdan o'tilgan sana topilmadi !"


def get_org_status(soup):
    org_status_tag = soup.find("span", string="Статус")
    if org_status_tag:
        parent_div = org_status_tag.find_parent("div")
        if parent_div:
            next_sibling = parent_div.find_next_sibling("div")
            if next_sibling:
                span_tag = next_sibling.find("span")
                if span_tag:
                    return span_tag.text.strip()
    return "Holat topilmadi"


def get_registration_authority(soup):
    registration_authority = soup.find("span", string="Регистрирующий орган")
    if registration_authority:
        parent_div = registration_authority.find_parent("div")
        if parent_div:
            next_sibling = parent_div.find_next_sibling("div")
            if next_sibling:
                span_tag = next_sibling.find('span')
                if span_tag:
                    return span_tag.text.strip()
    return "Ro'yxatga olish organi topilmadi"


def get_thsht_info(soup):
    thsht = soup.find("span", string="ОПФ")
    if thsht:
        parent_div = thsht.find_parent("div")
        if parent_div:
            next_sibling = parent_div.find_next_sibling("div")
            if next_sibling:
                span_tag = next_sibling.find('span')
                if span_tag:
                    return re.sub(r"\s+", " ", span_tag.text.strip())
    return "THSHT(ОПФ) topilmadi"


def get_dbibt_info(soup):
    dbibt = soup.find("span", string="СООГУ")
    if dbibt:
        parent_div = dbibt.find_parent("div")
        if parent_div:
            next_sibling = parent_div.find_next_sibling("div")
            if next_sibling:
                span_tag = next_sibling.find('span')
                if span_tag:
                    return re.sub(r"\s+", " ", span_tag.text.strip())
    return "DBIBT(СООГУ) topilmadi"


def get_ifut_info(soup):
    ifut = soup.find("span", string="ОКЭД")
    if ifut:
        parent_div = ifut.find_parent("div")
        if parent_div:
            next_sibling = parent_div.find_next_sibling("div")
            if next_sibling:
                span_tag = next_sibling.find('span')
                if span_tag:
                    return re.sub(r"\s+", " ", span_tag.text.strip())
    return "IFUT(ОКЭД) topilmadi"


def extract_email_from_html(soup):
    email_tag = soup.find("a", class_="__cf_email__")
    if email_tag:
        cfemail = email_tag.get("data-cfemail")
        if cfemail:
            hex_data = bytes.fromhex(cfemail)
            key = hex_data[0]
            decoded_chars = [chr(b ^ key) for b in hex_data[1:]]
            return ''.join(decoded_chars)
    return "Email topilmadi"


def get_inn_number(inn: int):
    return inn


def get_phone_number(soup):
    phone_number_tag = soup.find('a', class_='text-decoration-none text-body-hover text-success')
    if phone_number_tag:
        return phone_number_tag.find("span").text.strip()
    return "Telefon raqam topilmadi"


def get_shop_info(inn: int) -> ShopInfoBase:
    soup, org_url, org_soup = send_request(inn)
    shop_info = ShopInfoBase(
        register_date=get_register_date(org_soup),
        org_status=get_org_status(org_soup),
        registration_authority=get_registration_authority(org_soup),
        inn_number=inn,
        thsht_info=get_thsht_info(org_soup),
        dbibt_info=get_dbibt_info(org_soup),
        ifut_info=get_ifut_info(org_soup),
        authorized_fund=get_authorized_fund(org_url),
        org_email=extract_email_from_html(org_soup),
        org_phone_number=get_phone_number(org_soup),
        company_name=get_company_name(soup),
        company_address=get_location(soup),
        founders=get_founders(org_url)
    )
    return shop_info
