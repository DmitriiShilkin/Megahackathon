from django.core.exceptions import ValidationError
# from django.core.validators import URLValidator


def validate_size_image(file_obj):
    """ Проверка размера файла
    """
    megabyte_limit = 2
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Максимальный размер файла {megabyte_limit}MB")


# проверка вводимого значения на sql-инъекцию
def validate_sql_injections(value):
    if ("'" in value) or ('"' in value) or ("=" in value) or (";" in value):
        raise ValidationError(
            'Введено не допустимое значение.',
        )

# class OptionalSchemeURLValidator(URLValidator):
#     def __call__(self, value):
#         if '://' not in value:
#             # Validate as if it were http://
#             value = f'https://{value}'
#         super(OptionalSchemeURLValidator, self).__call__(value)
