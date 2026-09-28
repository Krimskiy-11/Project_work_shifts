import requests


class APIClient:

    def __init__(self, base_url="http://127.0.0.1:8000/api"):
        self.base_url = base_url
        self.token = None

    def login(self, username, password):
        """Получение авторизационного токена по логину и паролю."""
        url = f"{self.base_url}/api-token-auth/"
        response = requests.post(
            url, json={"username": username, "password": password}
        )
        if response.status_code == 200:
            self.token = response.json().get("token")
            return True
        return False

    def _get_headers(self):
        return {"Authorization": f"Token {self.token}"} if self.token else {}

    def get_tasks(self):
        """Получить список задач (зависит от роли на сервере)."""
        url = f"{self.base_url}/tasks/"
        response = requests.get(url, headers=self._get_headers())
        return response.json() if response.status_code == 200 else []

    def create_task(self, title, description, assigned_to_id, due_date=None):
        """Создание задачи менеджментом."""
        url = f"{self.base_url}/tasks/"
        payload = {
            "title": title,
            "description": description,
            "assigned_to": assigned_to_id,
            "status": "NEW",
        }
        if due_date:
            payload["due_date"] = due_date

        response = requests.post(url, json=payload, headers=self._get_headers())
        return response.status_code == 201

    def update_task(self, task_id, **kwargs):
        """PATCH: Частичное обновление задачи (статус, исполнитель, описание и т.д.)."""
        url = f"{self.base_url}/tasks/{task_id}/"
        try:
            response = requests.patch(
                url, json=kwargs, headers=self._get_headers()
            )
            return response.status_code in [200, 204]
        except requests.exceptions.RequestException as e:
            print(f"[API Error] Ошибка обновления задачи #{task_id}: {e}")
            return False

    def update_task_status(self, task_id, new_status):
        """Обновление статуса задачи сотрудником."""
        url = f"{self.base_url}/tasks/{task_id}/"
        payload = {"status": new_status}
        response = requests.patch(
            url, json=payload, headers=self._get_headers()
        )
        return response.status_code == 200

    def delete_task(self, task_id):
        """DELETE: Удаление задачи."""
        url = f"{self.base_url}/tasks/{task_id}/"
        try:
            response = requests.delete(url, headers=self._get_headers())
            return response.status_code in [200, 204]
        except requests.exceptions.RequestException as e:
            print(f"[API Error] Ошибка удаления задачи #{task_id}: {e}")
            return False

    def get_current_user_info(self):
        """Запрос профиля текущего авторизованного пользователя."""
        url = f"{self.base_url}/users/me/"
        try:
            response = requests.get(url, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            pass
        return None

    def get_users(self):
        """Запрос списка пользователей для выпадающего списка QComboBox."""
        url = f"{self.base_url}/users/"
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=5)
            if response.status_code == 200:
                return response.json()
            print(f"[API Error] Не удалось получить пользователей: {response.status_code} {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"[API Error] Ошибка соединения: {e}")
        return []

    def get_departments(self):
        """
        Получение списка всех отделов с бэкенда.
        """
        url = f"{self.base_url}/departments/"
        try:
            response = requests.get(url, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка получения отделов (статус {response.status_code}): {response.text}")
        except Exception as e:
            print(f"Ошибка соединения при запросе отделов: {e}")
        return []