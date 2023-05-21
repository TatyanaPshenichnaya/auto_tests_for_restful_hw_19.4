import json
import requests

from settings import valid_email, valid_password
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'



    def add_new_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={'name': name,
                    'animal_type': animal_type,
                    'age': age})
        headers = {'accept': 'application/json',
                   'auth_key': auth_key['key'],
                   'Content-Type' : data.content_type } #'multipart/form-data' }


        response = requests.post(f'{self.base_url}api/create_pet_simple',
                                headers=headers,
                                data=data)


        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        return status, result

    def get_api_key(self, email: str, password: str) -> json:
        """метод делает запрос к API сервера и возвращест статус запроса и результ в формате JSON
        с ункакльным ключом пользователя, найденного по указанным email и пароля   """
        #print(email)

        response = requests.get(f'{self.base_url}api/key',
                   headers = {'accept': 'application/json',
                              'email': email, #valid_email,
                              'password': password}) #valid_password })
        status = response.status_code
        #result = response.json()
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        return status, result

    def list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """метод делает запрос к API сервера и возвращест статус запроса и результ в формате JSON
        со списком найденных питомцев, совпадающих с фильтром. На данный момент фильр может иметь либо пустое
        значение - получить список всех питомцев, либо - 'my_pets' получить список собственных питомцев
        """
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        response = requests.get(f'{self.base_url}api/pets',
                                headers = headers,
                                params = filter)

        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        return status, result


    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str ) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""
        data = MultipartEncoder(
            fields={'name': name,
                    'animal_type': animal_type,
                    'age': age,
                    'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')})
        headers = {'accept': 'application/json',
                   'auth_key': auth_key['key'],
                   'Content-Type' : data.content_type } #'multipart/form-data' }


        response = requests.post(f'{self.base_url}api/pets',
                                headers=headers,
                                data=data)


        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        return status, result

    def add_photo(self, auth_key: json, pet_id: str , pet_photo: str ) -> json:


        #pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg') })
        headers = {'accept': 'application/json',
                   'auth_key': auth_key['key'],
                   'Content-Type': data.content_type}

        response = requests.post(f'{self.base_url}api/pets/set_photo/{pet_id}',
                                 headers=headers,
                                 data=data)

        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        return status, result

    def delete_pet(self, auth_key: json, pet_id: str ) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
               статус запроса и результат в формате JSON """
        headers = {'accept': 'application/json',
                   'auth_key': auth_key['key']}
        response = requests.delete(f'{self.base_url}api/pets/{pet_id}',
                                headers=headers)

        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        return status, result

    def update_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет запрос на сервер о обновлении данных питомца по указанному ID и
               возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""
        data = MultipartEncoder(
            fields={'name': name,
                    'animal_type': animal_type,
                    'age': age})
        headers = {'accept': 'application/json',
                   'auth_key': auth_key['key'],
                   'Content-Type': data.content_type}  # 'multipart/form-data' }

        response = requests.put(f'{self.base_url}api/pets/{pet_id}',
                                 headers=headers,
                                 data=data)

        status = response.status_code

        if status == 200:
            print('ok')
            result = 'the pet was removed from database successfully'
        else:
            result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        return status, result



test_pet = PetFriends()
print(test_pet.get_api_key(valid_email, valid_password))  # 5e3c2378ada84027517f36062ea603cf8da9e71b136756f46757b589
#print(test_pet.list_of_pets( test_pet.get_api_key(valid_email, valid_password)[1] ), 'my_pets')
#print(test_pet.add_new_pet(test_pet.get_api_key(valid_email, valid_password)[1] ,'Fansy','unicorrn', '2', "tests/images/fancy.jpg"))
#print(test_pet.update_pet(test_pet.get_api_key(valid_email, valid_password)[1] , '78a384a2-c660-4a09-80b4-8fa33b34afd9', 'Fanccy', 'unicorn', '12'))
#print(test_pet.delete_pet({'key':'5e3c2378ada84027517f36062ea603cf8'}, 'a9821f8d-d37f-479f-b23c-2890d8662799'))#test_pet.get_api_key(valid_email, valid_password)[1] , 'fe57f9c0-4bbf-81a0-683fd67b9bec'))
#print(test_pet.add_new_pet_simple(test_pet.get_api_key(valid_email, valid_password)[1] ,'Fancy','unicorn', '11'))
#print(test_pet.add_photo(test_pet.get_api_key(valid_email, valid_password)[1] , '2696c2ee-4557-4f54-9f3f-afc85c79370f', 'tests/images/fancy.jpg'))
#print(test_pet.get_api_key('mail@mail.ru', valid_password))
#print(test_pet.delete_pet({'key':'468tftdfyxfch6578hgf'}, 'af978284-4375-45c8-b2bc-c5e5bbb9fe57'))