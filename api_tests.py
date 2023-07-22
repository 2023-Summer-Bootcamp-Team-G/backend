import uuid
import unittest
import requests


class TestAPI(unittest.TestCase):
    # BASE_URL = "http://0.0.0.0:8000"
    BASE_URL = "http://localhost:8000"
    POLL_ID = 1
    CHARACTER_ID = 1

    RUN_POST_TESTS = True

    def setUp(self):
        self.session = requests.Session()

        self.USER_ID = self.generate_user_id()  # 검토
        self.PASSWORD = self.USER_ID

        # self.register(self.USER_ID, self.PASSWORD)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_register_post(self):
        response = self.register(self.generate_user_id(), self.PASSWORD)
        self.assertEqual(response.status_code, 201)

    def test_login_post(self):
        data = {
            # "user_id": self.USER_ID,
            # "password": self.PASSWORD,
            "user_id": "test",
            "password": "test1234",
        }
        response = self.session.post(f"{self.BASE_URL}/api/login", json=data)

        self.assertEqual(response.status_code, 200)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_question_post(self):
        data = {"user_id": "test", "questions": ["Question 1", "Question 2"]}
        response = self.session.post(f"{self.BASE_URL}/api/questions", json=data)
        self.assertEqual(response.status_code, 201)

    def test_question_get(self):
        params = {
            "poll_id": self.POLL_ID,
        }
        response = self.session.get(f"{self.BASE_URL}/api/questions", params=params)
        self.assertEqual(response.status_code, 200)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_characters_post(self):
        data = {
            "poll_id": self.POLL_ID,
            "creatorName": "Test",
            "answers": ["Answer 1", "Answer 2"],
        }
        response = self.session.post(f"{self.BASE_URL}/api/characters", json=data)
        self.assertEqual(response.status_code, 201)

    def test_characters_get(self):
        params = {
            # "user_id": self.USER_ID,
            "user_id": "test",
        }
        response = self.session.get(f"{self.BASE_URL}/api/characters", params=params)
        self.assertEqual(response.status_code, 200)

    def test_characters_id_get(self):
        response = self.session.get(
            f"{self.BASE_URL}/api/characters/{self.CHARACTER_ID}"
        )
        self.assertEqual(response.status_code, 200)

    def test_characters_chart_get(self):
        params = {
            # "user_id": self.USER_ID,
            "user_id": "test",
        }
        response = self.session.get(
            f"{self.BASE_URL}/api/characters/chart", params=params
        )
        self.assertEqual(response.status_code, 200, response.text)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_characters_duplicate_post(self):
        data = {
            "user_id": "test",  # test1234
            # "user_id": "576eec54-2564-4074-b74a-e1f70d04b7a9",
        }

        self.session.cookies.update(
            {
                "sessionid": "de5ocno6a5v067ciu8dq23k6zw8c2xe2",
            }
        )

        print("Session cookies:", self.session.cookies.get_dict())

        response = self.session.post(
            f"{self.BASE_URL}/api/characters/duplicate", json=data
        )

        self.assertEqual(response.status_code, 201, response.text)

    def generate_user_id(self):
        # Generate a UUID and convert it to a string
        user_id = str(uuid.uuid4())
        return user_id

    def register(self, user_id, password):
        data = {
            "nick_name": "test",
            "user_id": user_id,
            "password": password,
        }

        response_register = self.session.post(
            f"{self.BASE_URL}/api/register", json=data
        )

        # del data["nick_name"]
        data = {
            "user_id": "test",
            "password": "test1234",
        }

        self.session.post(f"{self.BASE_URL}/api/login", json=data)
        print("Session cookies from initial login:", self.session.cookies.get_dict())

        return response_register


if __name__ == "__main__":
    unittest.main(verbosity=2, failfast=False, exit=False)

    # unittest.TextTestRunner().run(
    #     unittest.FunctionTestCase(TestAPI("test_characters_duplicate_post"))
    # )
