from api import PetFriends
from settings import valid_email, valid_pass
import os

pf = PetFriends()

def test_apikey_for_invalid_user(email="test@mail.ru", password="testtest"):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    #Проверка ожидаемого ответа с фактическим
    assert status == 403

def test_get_list_with_incorrect_auth_key(filter = 'my_pets'):
    """ Проверяем что нельзя получить список питомцев, если api key неверный. Должен вернуться код 403
    Доступное значение параметра filter - 'my_pets' либо '' """

    #Передаем значение неверного auth_key
    auth_key = ('ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729')

    #Получаем список питомцев
    status, result = pf.get_list_with_incorrect_auth_key(auth_key, filter)

    #Подвердаем код 403
    assert status == 403

def test_add_pet_without_pic(name='Smiley', animal_type='dog', age='3'):
    """Проверяем что можно добавить питомца без фотографии"""
    _, auth_key = pf.get_api_key(valid_email, valid_pass)

    # Добавляем питомца
    status, result = pf.add_pet_without_pic(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_set_photo(pet_photo='images/dog.jpg'):
    """Проверяем возможность добавления фото питомца по ID"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
    else:
    # если спиок питомцев пустой, то выходит исключение с текстом об отсутствии своих питомцев
        raise Exception("There are no my pets")

def test_add_pet_with_empty_info_unsuccessful(name=" ", animal_type=' ', age=' '):
    """Проверяем что нельзя добавить питомца без имени. Тест должен вывести ошибку 400"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_pass)

    # Добавляем питомца
    status, result = pf.add_pet_without_pic(auth_key, name, animal_type, age)

    assert status == 400
    assert result['name'] == name

def test_add_pet_with_incorrect_data_unsuccessful(name="*&^%^&*", animal_type='*&&^$#@#$%', age='444444'):
    """Проверяем некорректный возраст в поле age. Тест должен вывести ошибку 400"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_pass)

    # Добавляем питомца
    status, result = pf.add_pet_without_pic(auth_key, name, animal_type, age)

    assert status == 400
    assert result['name'] == name

def test_update_pet_with_empty_data_unsuccessful(name = " ", animal_type = " ", age = " "):
    """Проверяем ввод некорректных данных для обновления информации о питомце. Тест должен вывести ошибку 400"""

        #Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

            #Проверяем ожидаемый результат
        assert status == 400
        assert result['name'] == name

    else:
        raise Exception("There are no my pets")

def test_update_pet_with_incorrect_data_unsuccessful(name = "*&^%$%^&", animal_type = ")(*&^%^", age = "^&*&^"):
    """Проверяем ввод некорректных данных для обновления информации о питомце. Тест должен вывести ошибку 400"""

        #Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_pass)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

            #Проверяем ожидаемый результат
        assert status == 400
        assert result['name'] == name

    else:
        raise Exception("There are no my pets")

def test_add_pet_with_incorrect_auth_key(name='Smiley', animal_type='dog', age='3'):
    """Проверяем что нельзя добавить питомца с неверным auth_key. Выходит ошибка 404"""
    auth_key = 'ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729'

    # Добавляем питомца
    status, result = pf.add_pet_with_incorrect_auth_key(auth_key, name, animal_type, age)
    #Проверяем ожидаемый результат
    assert status == 403

