from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


def get_translated_field(obj, lang: str, field_base_name: str):
    # Ma'lumotlar obyektining tilga bog‘liq maydonini qaytarish
    field_name = f"{field_base_name}_{lang}"  # Masalas: "category_name_uz" yoki "category_name_ru"
    return getattr(obj, field_name, None)  # Agar maydon bo‘lmasa, None qaytaradi


def fetch_orginfo_by_inn(inn: str):
    search_url = f"https://orginfo.uz/search?q={inn}"
    req = Request(search_url, headers={"User-Agent": "Mozilla/5.0"})
    html = urlopen(req).read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find('a', href=True, text="Batafsil")
