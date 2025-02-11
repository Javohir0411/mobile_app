def get_translated_field(obj, lang: str, field_base_name: str):
    # Ma'lumotlar obyektining tilga bog‘liq maydonini qaytarish
    field_name = f"{field_base_name}_{lang}"  # Masalas: "category_name_uz" yoki "category_name_ru"
    return getattr(obj, field_name, None)  # Agar maydon bo‘lmasa, None qaytaradi
