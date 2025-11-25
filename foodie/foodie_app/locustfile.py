from locust import HttpUser, task, between

class FoodieUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def test_send_message(self):
        headers = {"x-requested-with": "XMLHttpRequest"}
        data = {"message": "Hello from Locust!"}
        self.client.post("send_message", data=data, headers=headers)

    @task
    def test_upload_image(self):
        # Sukuriame validų JPG failą
        files = {
            "image": ("test.jpg", b"fake-jpeg-data", "image/jpeg")
        }
        self.client.post("upload_image", files=files)
