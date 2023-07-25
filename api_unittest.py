import time
import uuid
import unittest
import requests

RUN_POST_TESTS = True


class TestTeamGAPI(unittest.TestCase):
    base_url = "http://localhost:8000"
    # base_url = "http://3.35.88.150:8000"

    test_user_id = "test"
    test_password = "test1234"
    test_nick_name = "testNickName"

    session = requests.session()

    results = dict()

    # def test_00_test(self):
    #     # TODO: 로그아웃 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
    #     # self.test_05_characters()

    #     data = {
    #         "user_id": self.test_user_id,
    #         "password": self.test_password,
    #     }
    #     response = self.session.post(f"{self.base_url}/api/login", json=data)

    #     self.assertEqual(response.status_code, 200)

    #     data = {
    #         "poll_id": 1,
    #         "creatorName": self.test_nick_name,
    #         "answers": ["Answer 1", "Answer 2"],
    #     }
    #     response = self.session.post(f"{self.base_url}/api/characters", json=data)

    #     TestTeamGAPI.test_task_id = response.json()["task_id"]

    #     self.assertEqual(response.status_code, 201)

    # @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    # def test_01_register(self):
    #     # TODO: 회원가입 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
    #     data = {
    #         "nick_name": self.test_nick_name,
    #         "user_id": str(uuid.uuid4()),
    #         "password": self.test_password,
    #     }

    #     response = self.session.post(f"{self.base_url}/api/register", json=data)

    #     self.assertEqual(response.status_code, 201)

    # def test_02_login(self):
    #     # TODO: 로그인 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
    #     data = {
    #         "user_id": self.test_user_id,
    #         "password": self.test_password,
    #     }
    #     response = self.session.post(f"{self.base_url}/api/login", json=data)

    #     self.assertEqual(response.status_code, 200)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_03_questions(self):
        # TODO: 질문 생성 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
        data = {
            "user_id": self.test_user_id,
            "questions": ["Question 1", "Question 2", "Question 3"],
        }
        response = self.session.post(f"{self.base_url}/api/questions", json=data)

        TestTeamGAPI.test_poll_id = response.json()["poll_id"]

        self.assertEqual(response.status_code, 201)

    def test_04_questions_list(self):
        # TODO: 질문 리스트 엔드포인트에 GET 요청을 보내고, 응답을 확인합니다.
        params = {
            "poll_id": self.test_poll_id,
        }
        response = self.session.get(f"{self.base_url}/api/questions", params=params)
        self.assertEqual(response.status_code, 200)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_05_characters(self):
        # TODO: 캐릭터 생성 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
        data = {
            "poll_id": self.test_poll_id,
            "creatorName": self.test_nick_name,
            "answers": ["Answer 1", "Answer 2"],
        }
        response = self.session.post(f"{self.base_url}/api/characters", json=data)

        TestTeamGAPI.test_task_id = response.json()["task_id"]

        self.assertEqual(response.status_code, 201)

    def test_06_characters_urls_read(self):
        # TODO: 캐릭터 URL 읽기 엔드포인트에 GET 요청을 보내고, 응답을 확인합니다.
        while True:
            response = self.session.get(
                f"{self.base_url}/api/characters/urls/{self.test_task_id}"
            )

            if response.status_code == 200:
                TestTeamGAPI.results["urls"] = response.json()["result_url"]
                break
            elif response.status_code != 202:
                self.assertEqual(response.status_code, 200)

            time.sleep(1)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_07_characters_choice(self):
        # TODO: 캐릭터 선택 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
        data = {"task_id": self.test_task_id, "index": 3}
        response = self.session.post(
            f"{self.base_url}/api/characters/choice", json=data
        )

        self.assertEqual(response.status_code, 201)

    def test_08_characters_list(self):
        # TODO: 캐릭터 리스트 엔드포인트에 GET 요청을 보내고, 응답을 확인합니다.
        params = {
            "user_id": self.test_user_id,
        }
        response = self.session.get(f"{self.base_url}/api/characters", params=params)

        TestTeamGAPI.test_character_id = response.json()["characters"][0]["id"]

        self.assertEqual(response.status_code, 200)

    def test_09_characters_read(self):
        # TODO: 캐릭터 정보 확인 엔드포인트에 GET 요청을 보내고, 응답을 확인합니다.
        response = self.session.get(
            f"{self.base_url}/api/characters/{self.test_character_id}"
        )
        self.assertEqual(response.status_code, 200)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_10_characters_chart_list(self):
        # TODO: 캐릭터 차트 엔드포인트에 GET 요청을 보내고, 응답을 확인합니다.
        params = {
            "user_id": self.test_user_id,
        }
        response = self.session.get(
            f"{self.base_url}/api/characters/chart", params=params
        )

        self.assertEqual(response.status_code, 200, response.text)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_11_characters_duplicate(self):
        # TODO: 캐릭터 복제 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
        data = {
            "user_id": self.test_user_id,
        }

        data["session_id"] = "session_id_for_test"

        response = self.session.post(
            f"{self.base_url}/api/characters/duplicate", json=data
        )

        self.assertEqual(response.status_code, 201, response.text)

    # @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    # def test_12_extract_phrases(self):
    #     # TODO: 구문 추출 생성 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
    #     data = {"text": "This is a sample sentence for test."}  # 분석할 텍스트
    #     response = self.session.post(f"{self.base_url}/api/extract-phrases", json=data)

    #     TestTeamGAPI.results["extract_phrases_post"] = response.json()
    #     self.assertEqual(response.status_code, 200)

    # def test_13_extract_phrases_list(self):
    #     # TODO: 구문 추출 리스트 엔드포인트에 GET 요청을 보내고, 응답을 확인합니다.
    #     response = self.session.get(f"{self.base_url}/api/extract-phrases")
    #     TestTeamGAPI.results["extract_phrases_get"] = response.json()
    #     self.assertEqual(response.status_code, 200)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_14_logout(self):
        # TODO: 로그아웃 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
        response = self.session.post(f"{self.base_url}/api/logout")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main(verbosity=2, failfast=False, exit=False)

    # unittest.TextTestRunner().run(
    #     unittest.FunctionTestCase(TestTeamGAPI("test_00_test"))
    # )

    print(
        "\n",
        "\n".join([f"{key}: {value}\n" for key, value in TestTeamGAPI.results.items()]),
        "\n",
    )
