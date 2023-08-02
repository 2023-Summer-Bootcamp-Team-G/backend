import time
import uuid
import unittest
import requests

RUN_POST_TESTS = True
RUN_EXTRACT_TESTS = False


class TestTeamGAPI(unittest.TestCase):
    base_url = "http://localhost:8000"
    base_url = "http://3.35.88.150:8000"
    # base_url = "https://1tsme.site"

    main_user_id = "test-unittest"
    main_password = "test"
    main_nick_name = "nickname-unittest"

    main_session = requests.session()

    results = dict()

    def setUp(self):
        pass

    def create_logged_in_session(self, return_data=False):
        session = requests.session()
        data = {
            "user_id": "unittest-" + str(uuid.uuid4()),
            "password": self.main_password,
            "nick_name": self.main_nick_name,
        }
        response = session.post(f"{self.base_url}/api/register", json=data)
        self.assertEqual(response.status_code, 201)
        if return_data:
            return session, data
        else:
            return session

    def test_00_test(self):
        # TODO: 테스트
        # session, data = self.create_logged_in_session(True)

        # del data["nick_name"]

        # response = self.main_session.post(f"{self.base_url}/api/login", json=data)

        # print(response.content)

        # self.assertTrue(False)
        pass

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_01_register(self):
        # TODO: 회원가입 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
        self.create_logged_in_session()

    def test_02_login(self):
        # TODO: 로그인 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
        data = {
            "user_id": self.main_user_id,
            "password": self.main_password,
        }
        response = self.main_session.post(f"{self.base_url}/api/login", json=data)

        # print(response.json())

        self.assertEqual(response.status_code, 200)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_03_questions(self):
        # TODO: 질문 생성 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
        questions = [
            "나를 동물로 표현한다 하면 어떤 동물이야?",
            "나를 색으로 표현한다면 무슨 색이야?",
            "나는 어떤 그림체가 어울려?",
            "내가 자주 들고다니는 물건은 뭐야?",
            "내가 자주 나타나는 장소는 어디야?",
            "내가 자주 하고다니는 악세사리는?",
        ]

        questions += [
            "내가 자주 입는 옷은 뭐야?",
        ]

        data = {
            "user_id": self.main_user_id,
            "questions": questions,
        }

        response = self.main_session.post(f"{self.base_url}/api/questions", json=data)
        print("response", response.text.replace("\n", "")[:128], end=" ")
        TestTeamGAPI.test_poll_id = response.json()["poll_id"]
        self.assertEqual(response.status_code, 201)

    def test_04_questions_list(self):
        # TODO: 질문 리스트 엔드포인트에 GET 요청을 보내고, 응답을 확인합니다.
        params = {
            "poll_id": self.test_poll_id,
        }
        response = self.main_session.get(
            f"{self.base_url}/api/questions", params=params
        )
        data = response.json()
        TestTeamGAPI.main_user_id = data["user_id"]
        TestTeamGAPI.questions = data["questions"]

        print(data["nick_name"])

        self.assertEqual(response.status_code, 200)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_05_characters(self):
        # TODO: 캐릭터 생성 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
        sessions = {
            "creator": self.main_session,
            "anonymous": requests.session(),
            "answerer": self.create_logged_in_session(),
        }

        data = {
            "poll_id": self.test_poll_id,
            "creatorName": self.main_nick_name,
            "answers": [],
        }

        test_task_ids = list()

        for key, session in sessions.items():
            print("test with:", key, end=" ")

            data["answers"] = [key + ", " + question for question in self.questions]
            response = session.post(f"{self.base_url}/api/characters", json=data)
            print("response", response.text.replace("\n", "")[:128], end="\n")
            test_task_ids.append(response.json()["task_id"])
            TestTeamGAPI.test_task_ids = test_task_ids
            self.assertEqual(response.status_code, 201)

    def test_06_characters_urls_read(self):
        # TODO: 캐릭터 URL 읽기 엔드포인트에 GET 요청을 보내고, 응답을 확인합니다.
        completed_test = 0

        responses = [requests.Response() for _ in self.test_task_ids]

        while completed_test < len(self.test_task_ids):
            for i, task_id in enumerate(self.test_task_ids):
                if responses[i] is None:
                    continue
                else:
                    responses[i] = self.main_session.get(
                        f"{self.base_url}/api/characters/urls/{task_id}"
                    )

                if responses[i].status_code == 200:
                    data = responses[i].json()

                    TestTeamGAPI.results["urls"] = TestTeamGAPI.results.get(
                        "urls", list()
                    )
                    TestTeamGAPI.results["urls"].append(data["result_url"])

                    responses[i] = None
                    completed_test += 1

                    self.assertTrue(
                        all(key in data for key in ["result_url", "keyword"])
                    )
                elif responses[i].status_code != 202:
                    self.assertEqual(responses[i].status_code, 200)

            time.sleep(1)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_07_characters_choice(self):
        # TODO: 캐릭터 선택 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
        data = {
            "task_id": self.test_task_ids[0],
            "index": len(TestTeamGAPI.results["urls"]) - 1,
        }
        response = self.main_session.post(
            f"{self.base_url}/api/characters/choice", json=data
        )
        self.assertEqual(response.status_code, 201)

    def test_08_characters_list(self):
        # TODO: 캐릭터 리스트 엔드포인트에 GET 요청을 보내고, 응답을 확인합니다.
        params = {
            "user_id": self.main_user_id,
        }

        # # for test
        # params = {}
        # TestTeamGAPI.main_session = requests.session()

        response = self.main_session.get(
            f"{self.base_url}/api/characters", params=params
        )
        TestTeamGAPI.test_character_id = response.json()["characters"][0]["id"]
        self.assertEqual(response.status_code, 200)

    def test_09_characters_read(self):
        # TODO: 캐릭터 정보 확인 엔드포인트에 GET 요청을 보내고, 응답을 확인합니다.
        response = self.main_session.get(
            f"{self.base_url}/api/characters/{self.test_character_id}"
        )
        self.assertEqual(response.status_code, 200)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_10_characters_chart_list(self):
        # TODO: 캐릭터 차트 엔드포인트에 GET 요청을 보내고, 응답을 확인합니다.
        params = {
            "user_id": self.main_user_id,
        }
        response = self.main_session.get(
            f"{self.base_url}/api/characters/chart", params=params
        )
        self.assertEqual(response.status_code, 200, response.text)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_11_characters_duplicate(self):
        # TODO: 캐릭터 복제 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
        session, data = self.create_logged_in_session(True)

        users = {
            "creator": {
                "session": self.main_session,
                "data": {"user_id": self.main_user_id},
            },
            # "new_creator": {
            #     "session": session,
            #     "data": {"user_id": data["user_id"]},
            # },
        }

        # new_creator
        TestTeamGAPI.main_session = session
        print("setup start")
        self.test_03_questions()
        self.test_05_characters()
        print("setup end\n")

        test_task_ids = list()

        for key, user in users.items():
            print("test with:", key, end=" ")

            data["answers"] = [key + ", " + question for question in self.questions]
            response = user["session"].post(
                f"{self.base_url}/api/characters/duplicate", json=user["data"]
            )
            print("response", response.text.replace("\n", "")[:128], end="\n")
            test_task_ids.append(response.json()["task_id"])
            TestTeamGAPI.test_task_ids = test_task_ids
            self.assertEqual(
                response.status_code, 201, response.text.replace("\n", "")[:128]
            )

    def test_12_characters_urls_read(self):
        # TODO: 캐릭터 URL 읽기 엔드포인트에 GET 요청을 보내고, 응답을 확인합니다.
        self.test_06_characters_urls_read()

    @unittest.skipUnless(RUN_EXTRACT_TESTS, "Skipping extract_phrases tests")
    def test_13_extract_phrases(self):
        # TODO: 구문 추출 생성 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
        data = {"text": "This is a sample sentence for test."}  # 분석할 텍스트
        response = self.main_session.post(
            f"{self.base_url}/api/extract-phrases", json=data
        )

        TestTeamGAPI.results["extract_phrases_post"] = response.json()
        self.assertEqual(response.status_code, 200)

    @unittest.skipUnless(RUN_EXTRACT_TESTS, "Skipping extract_phrases tests")
    def test_14_extract_phrases_list(self):
        # TODO: 구문 추출 리스트 엔드포인트에 GET 요청을 보내고, 응답을 확인합니다.
        response = self.main_session.get(f"{self.base_url}/api/extract-phrases")
        TestTeamGAPI.results["extract_phrases_get"] = response.json()
        self.assertEqual(response.status_code, 200)

    @unittest.skipUnless(RUN_POST_TESTS, "Skipping POST tests")
    def test_15_logout(self):
        # TODO: 로그아웃 엔드포인트에 POST 요청을 보내고, 응답을 확인합니다.
        response = self.main_session.post(f"{self.base_url}/api/logout")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main(verbosity=2, failfast=True, exit=False)

    # unittest.TextTestRunner().run(
    #     unittest.FunctionTestCase(TestTeamGAPI("test_00_test"))
    # )

    print(
        "\n",
        "\n".join(
            [
                f"{key}: " + "\n".join(str(item) + "\n" for item in value)
                for key, value in TestTeamGAPI.results.items()
            ]
        ),
        "\n",
    )
