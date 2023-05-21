from api import PetFriends
from settings import valid_email, valid_password

class TestPets:
    def setup(self):
        self.pets = PetFriends
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def test_get_api_key(self, email=valid_email, password=valid_password):
       """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

       # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
       status, result = self.pets.get_api_key(self, email, password)

       # Сверяем полученные данные с нашими ожиданиями
       assert status == 200
       assert 'key' in result

    def test_list_pets(self, filter=''):
        """ Проверяем что запрос всех питомцев возвращает не пустой список.
            Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
            запрашиваем список всех питомцев и проверяем что список не пустой.
            Доступное значение параметра filter - 'my_pets' либо '' """

        _, auth_key = self.pets.get_api_key(self, valid_email, valid_password)
        status, result = self.pets.list_of_pets(self, auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

    def test_adding_success(self, name='Fansya', animal_type='unicorn', age='2', pet_photo='images/fancy.jpg'):
        """Проверяем, что можно добавить питомца с корректными данными"""

        _, auth_key = self.pets.get_api_key(self, valid_email, valid_password)
        status, result = self.pets.add_new_pet(self, auth_key,
                                               name, animal_type, age, pet_photo)

        # проверяем, что имя в результате совпадает с именем добавляемого питомца
        assert status == 200
        assert result['name'] == name

    def test_update_pet(self, name='Liana', animal_type='unicorn', age='2'):
        """Проверяем возможность обновления информации о питомце"""

        # Получаем ключ auth_key и список своих питомцев
        _, auth_key = self.pets.get_api_key(self, valid_email, valid_password)
        _, my_pets = self.pets.list_of_pets(self, auth_key, "my_pets")

        # Если список не пустой, то пробуем обновить у первого питомца его имя, тип и возраст
        if len(my_pets['pets']) > 0:
            status, result = self.pets.update_pet(self, auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

            # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
            assert status == 200
            assert result['name'] == name
        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")

    def test_successful_delete_self_pet(self):
        """Проверяем возможность удаления питомца"""

        # Получаем ключ auth_key и запрашиваем список своих питомцев
        _, auth_key = self.pets.get_api_key(self, valid_email, valid_password)
        _, my_pets = self.pets.list_of_pets(self, auth_key, "my_pets")

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            self.pets.add_new_pet(auth_key, "Ladybug", "bug", "16", "images/babochka.jpg")
            _, my_pets = self.pets.list_of_pets(self, auth_key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на удаление
        first_pet_id = my_pets['pets'][0]['id']
        status, _ = self.pets.delete_pet(self, auth_key, first_pet_id)

        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = self.pets.list_of_pets(self, auth_key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert first_pet_id not in my_pets.values()

    def test_get_api_invalid_email(self, email='ttt@mail.ru',
                                   password=valid_password):  # , email='ttt@mail.ru', password=valid_password):
        """1 Проверяем возможность получение api ключа с невалидным email"""
        status, result = self.pets.get_api_key(self, email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403
        assert 'Forbidden' in result

    def test_get_api_invalid_password(self, email=valid_email, password='123456'):
        """2 Проверяем возможность получение api ключа с невалидным паролем"""
        status, result = self.pets.get_api_key(self, email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403
        assert 'Forbidden' in result

    def test_list_pets_unvalid_api_key(self, filter=''):
        """3 Проверяем возможность получение списка всех питомцев с недействительным api ключом"""

        #_, auth_key = self.pets.get_api_key(self, valid_email, valid_password)
        status, result = self.pets.list_of_pets(self, {'key': '468tftdfyxfch6578hgf'}, filter)
        assert status == 403
        assert 'Forbidden' in result

    def test_adding_unsuccess_unvalid_age(self):
        """4 Проверяем что можно добавить питомца с некорректными данными возраста (вместо строки словарь)"""

        _, auth_key = self.pets.get_api_key(self, valid_email, valid_password)

        try:
            status, result = self.pets.add_new_pet(self, auth_key,
                                                   'Lia', 'unicorn', {'15':'uni'}, 'images/fancy.jpg')
        except AttributeError:
            print('provided data is incorrect')

    def test_adding_unsuccess_unvalid_photo_path(self):
        """5 Проверяем что можно добавить питомца с некорректными данными фото (не существует в указанной директории)"""

        _, auth_key = self.pets.get_api_key(self, valid_email, valid_password)
        try:
            status, result = self.pets.add_new_pet(self, auth_key,
                                                   'Fancy', 'unicorn', '2', 'images/aaaaa.jpg')

            assert status == 200
            assert result['name'] == 'Fancy'
        except FileNotFoundError:
            print('File is not found')


    def test_delete_unvalid_api_key(self):
        """6 Проверяем возможность удаления питомца с неверным api key"""

        _, auth_key = self.pets.get_api_key(self, valid_email, valid_password)
        _, my_pets = self.pets.list_of_pets(self, auth_key, "my_pets")

        # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            self.pets.add_new_pet(auth_key, "Ladybug", "bug", "16", "images/babochka.jpg")
            _, my_pets = self.pets.list_of_pets(self, auth_key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на удаление
        first_pet_id = my_pets['pets'][0]['id']
        try:
            status, _ = self.pets.delete_pet(self, {'key': '468tftdfyxfch6578hgf'}, first_pet_id)

            # Ещё раз запрашиваем список своих питомцев
            _, my_pets = self.pets.list_of_pets(self, auth_key, "my_pets")

            # Проверяем что статус ответа равен 200 и в списке питомцев рисутствует id первого питомца
            assert status == 403
            assert first_pet_id in my_pets.values()
        except:
            print('Wrong parameters!')

    def test_update_pet_unvalid_pet_id(self):
        """7 Проверяем возможность обновления информации о питомце с неверным id"""
        # Получаем ключ auth_key и список своих питомцев
        _, auth_key = self.pets.get_api_key(self, valid_email, valid_password)
        _, my_pets = self.pets.list_of_pets(self, auth_key, "my_pets")

        status, result = self.pets.update_pet(self, auth_key, '123456', 'Ola', 'cat', '3')

        # проверяем, что питомец с таким id не найден
        assert status == 400
        assert 'Pet with this id wasn&#x27;t found!' in result

    def test_update_pet_unvalid_age(self):
        """8 Проверяем возможность обновления информации о питомце с отсутствующем возрастом"""
        # Получаем ключ auth_key и список своих питомцев
        _, auth_key = self.pets.get_api_key(self, valid_email, valid_password)
        _, my_pets = self.pets.list_of_pets(self, auth_key, "my_pets")

        # Если список не пустой, то пробуем обновить у первого питомца его имя, тип и возраст
        try:
            if len(my_pets['pets']) > 0:
                status, result = self.pets.update_pet(self, auth_key, my_pets['pets'][0]['id'], 'Ali', 'cat' )
            # Проверяем что статус ответа = 200, т.к. параметр возраст не является обязательным
                assert status == 400
                assert 'incorrect' in result
        except TypeError:
            print('Не хватает аргумента')

    def test_update_pet_photo_unvalid_pet_id(self):
        """9 Проверяем возможность добавления фото питомца с неверным id"""
        _, auth_key = self.pets.get_api_key(self, valid_email, valid_password)

        try:
            status, result = self.pets.add_photo(self, auth_key, '123456',
                                                 'tests/images/fancy.jpg')
            assert status == 200
        except FileNotFoundError:
            print('File is not found')

    def test_update_pet_photo_unvalid_path(self):
        """10 Проверяем возможность добавления фото питомца с некорректными данными фото (не существует в указанной директории)"""
        _, auth_key = self.pets.get_api_key(self, valid_email, valid_password)
        _, my_pets = self.pets.list_of_pets(self, auth_key, "my_pets")

        if len(my_pets['pets']) > 0:
            try:
                status, result = self.pets.add_photo(self, auth_key, my_pets['pets'][0]['id'],
                                                     'tests/images/123456.jpg')

                # Проверяем что статус ответа = 400
                assert status == 400
                assert 'directory' in result
            except FileNotFoundError:
                print('File is not found')
        else:
            # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
            raise Exception("There is no my pets")







