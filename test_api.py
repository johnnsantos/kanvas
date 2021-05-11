from django.test import TestCase
from rest_framework.test import APIClient


class TestAccountView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.student1_data = {
            "username": "student1",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False,
        }

        self.student1_login_data = {
            "username": "student1",
            "password": "1234",
        }

        self.facilitator_data = {
            "username": "facilitator",
            "password": "1234",
            "is_superuser": False,
            "is_staff": True,
        }

        self.facilitator_login_data = {
            "username": "facilitator",
            "password": "1234",
        }

        self.instructor_data = {
            "username": "instructor",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True,
        }

        self.instructor_login_data = {
            "username": "instructor",
            "password": "1234",
        }

    def test_create_and_login_for_student_account(self):
        # create student user
        student_user = self.client.post(
            "/api/accounts/", self.student1_data, format="json"
        )

        # testa se o student user foi criado corretamente
        self.assertEqual(
            student_user.json(),
            {"id": 1, "username": "student1", "is_superuser": False, "is_staff": False},
        )
        self.assertEqual(student_user.status_code, 201)

        # testa se o login foi realizado corretamente e se o token é retornado
        response = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()

        self.assertIn("token", response.keys())

    def test_create_and_login_for_facilitator_account(self):
        # create facilitator user
        facilitator_user = self.client.post(
            "/api/accounts/", self.facilitator_data, format="json"
        )

        # testa se o facilitator user foi criado corretamente
        self.assertEqual(
            facilitator_user.json(),
            {
                "id": 1,
                "username": "facilitator",
                "is_superuser": False,
                "is_staff": True,
            },
        )
        self.assertEqual(facilitator_user.status_code, 201)

        # testa se o login foi realizado corretamente e se o token é retornado
        response = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()

        self.assertIn("token", response.keys())

    def test_create_and_login_for_instructor_account(self):
        # create instructor user
        instructor_user = self.client.post(
            "/api/accounts/", self.instructor_data, format="json"
        )

        # testa se o instructor user foi criado corretamente
        self.assertEqual(
            instructor_user.json(),
            {"id": 1, "username": "instructor", "is_superuser": True, "is_staff": True},
        )
        self.assertEqual(instructor_user.status_code, 201)

        # testa se o login foi realizado corretamente e se o token é retornado
        response = self.client.post(
            "/api/login/", self.instructor_login_data, format="json"
        ).json()

        self.assertIn("token", response.keys())

    def test_wrong_credentials_do_not_login(self):
        # create instructor user
        response = self.client.post(
            "/api/accounts/", self.instructor_data, format="json"
        )

        # faz o login com os dados do facilitador, sendo que esse não foi criado
        # testa se o sistema não faz o login e retorna 401
        response = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        )

        self.assertEqual(response.status_code, 401)

    def test_create_two_equals_users(self):
        response = self.client.post(
            "/api/accounts/", self.instructor_data, format="json"
        )
        response_2 = self.client.post(
            "/api/accounts/", self.instructor_data, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_2.status_code, 409)


class TestCourseView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.student1_data = {
            "username": "student1",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False,
        }

        self.student1_login_data = {
            "username": "student1",
            "password": "1234",
        }

        self.student2_data = {
            "username": "student2",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False,
        }

        self.facilitator_data = {
            "username": "facilitator",
            "password": "1234",
            "is_superuser": False,
            "is_staff": True,
        }

        self.facilitator_login_data = {
            "username": "facilitator",
            "password": "1234",
        }

        self.instructor1_data = {
            "username": "instructor",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True,
        }

        self.instructor1_login_data = {
            "username": "instructor",
            "password": "1234",
        }

        self.course_data = {"name": "course1"}

    def test_instructor_can_create_course(self):
        # create instructor user
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        # create course
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        ).json()

        self.assertDictEqual(course, {"id": 1, "name": "course1", "user_set": []})

    def test_facilitator_or_student_cannot_create_course(self):
        # create student user
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # student user cannot create course
        status_code = self.client.post(
            "/api/courses/", self.course_data, format="json"
        ).status_code
        self.assertEqual(status_code, 403)

        # create facilitator user
        self.client.post("/api/accounts/", self.facilitator_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # facilitator user cannot create course
        status_code = self.client.post(
            "/api/courses/", self.course_data, format="json"
        ).status_code
        self.assertEqual(status_code, 403)

    def test_anonymous_can_list_courses(self):
        # create instructor user
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create course
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        ).json()

        self.assertEqual(course, {"name": "course1", "user_set": [], "id": 1})

        # reset client -> no login
        client = APIClient()

        # list courses with anonymous user
        course_list = client.get("/api/courses/").json()

        self.assertEqual(len(course_list), 1)

    def test_instructor_can_register_students_on_course(self):
        # create student 1
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # create student 2
        self.client.post("/api/accounts/", self.student2_data, format="json")

        # create instructor
        self.client.post("/api/accounts/", self.instructor1_data, format="json")

        token = self.client.post(
            "/api/login/", self.instructor1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create course
        course = self.client.post(
            "/api/courses/", self.course_data, format="json"
        ).json()

        self.assertEqual(course, {"name": "course1", "user_set": [], "id": 1})

        # register students 1 and 2 in course
        response = self.client.put(
            "/api/courses/registrations/",
            {"course_id": 1, "user_ids": [1, 2]},
            format="json",
        )

        self.assertEqual(len(response.json()["user_set"]), 2)
        self.assertEqual(response.status_code, 200)

        # change students in course, now we have only student 1 in course
        response = self.client.put(
            "/api/courses/registrations/",
            {"course_id": 1, "user_ids": [1]},
            format="json",
        )
        self.assertEqual(len(response.json()["user_set"]), 1)
        self.assertEqual(response.json()["user_set"][0]["id"], 1)
        self.assertEqual(response.status_code, 200)

        # change students in course, now we have only student 2 in course
        response = self.client.put(
            "/api/courses/registrations/",
            {"course_id": 1, "user_ids": [2]},
            format="json",
        )
        self.assertEqual(len(response.json()["user_set"]), 1)
        self.assertEqual(response.json()["user_set"][0]["id"], 2)
        self.assertEqual(response.status_code, 200)

        # change students in course, now we don't have students in course
        response = self.client.put(
            "/api/courses/registrations/",
            {"course_id": 1, "user_ids": []},
            format="json",
        )
        self.assertEqual(len(response.json()["user_set"]), 0)
        self.assertEqual(response.status_code, 200)


class TestActivityView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.student1_data = {
            "username": "student1",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False,
        }

        self.student1_login_data = {
            "username": "student1",
            "password": "1234",
        }

        self.student2_data = {
            "username": "student2",
            "password": "1234",
            "is_superuser": False,
            "is_staff": False,
        }

        self.student2_login_data = {
            "username": "student2",
            "password": "1234",
        }

        self.facilitator_data = {
            "username": "facilitator",
            "password": "1234",
            "is_superuser": False,
            "is_staff": True,
        }

        self.facilitator_login_data = {
            "username": "facilitator",
            "password": "1234",
        }

        self.instructor_data = {
            "username": "instructor",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True,
        }

        self.instructor_login_data = {
            "username": "instructor",
            "password": "1234",
        }

        self.activity_data = {"repo": "test repo"}
        self.activity_data_1 = {"repo": "test repo"}
        self.activity_data_2 = {"repo": "test repo 2"}
        self.activity_data_3 = {"repo": "test repo"}
        self.activity_data_4 = {"repo": "test repo 2"}

    def test_create_activities_student(self):
        # test with no authentication
        response = self.client.post(
            "/api/activities/", self.activity_data, format="json"
        )
        self.assertEqual(response.status_code, 401)

        # create student user
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # login student user
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create activity
        response = self.client.post(
            "/api/activities/", self.activity_data, format="json"
        )
        activity = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            activity, {"id": 1, "user_id": 1, "repo": "test repo", "grade": None}
        )

    def test_facilitator_or_instructor_cannot_create_activity(self):
        # create facilitator user
        self.client.post("/api/accounts/", self.facilitator_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # try create activity
        response = self.client.post(
            "/api/activities/", self.activity_data, format="json"
        )
        self.assertEqual(response.status_code, 401)

        # create instructor user
        self.client.post("/api/accounts/", self.instructor_data, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # login
        token = self.client.post(
            "/api/login/", self.instructor_login_data, format="json"
        )

        # create activity
        response_2 = self.client.post(
            "/api/activities/", self.activity_data, format="json"
        )
        self.assertEqual(response_2.status_code, 401)

    def test_student_cannot_assign_grade(self):
        # student tries to assign grade, but it should not have
        # any effect
        activity_data = {"repo": "test repo", "grade": 10}
        # test with no authentication
        response = self.client.post("/api/activities/", activity_data, format="json")
        self.assertEqual(response.status_code, 401)

        # create student user
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create activity
        response = self.client.post("/api/activities/", activity_data, format="json")
        activity = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            activity, {"repo": "test repo", "user_id": 1, "id": 1, "grade": None}
        )

    def test_get_activities_student(self):
        # create student user
        self.client.post("/api/accounts/", self.student1_data, format="json")

        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # student user creates two activities
        activity_1 = self.client.post(
            "/api/activities/", self.activity_data_1, format="json"
        ).json()
        activity_2 = self.client.post(
            "/api/activities/", self.activity_data_2, format="json"
        ).json()

        self.assertEqual(
            activity_1, {"id": 1, "repo": "test repo", "user_id": 1, "grade": None}
        )

        self.assertEqual(
            activity_2, {"id": 2, "repo": "test repo 2", "user_id": 1, "grade": None}
        )

        activity_list = self.client.get("/api/activities/").json()

        self.assertEqual(
            activity_list,
            [
                {"id": 1, "repo": "test repo", "user_id": 1, "grade": None},
                {"id": 2, "repo": "test repo 2", "user_id": 1, "grade": None},
            ],
        )

    def test_student_can_only_see_own_activities(self):
        # create student 1
        self.client.post("/api/accounts/", self.student1_data, format="json")

        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create 2 activities for student 1
        self.client.post("/api/activities/", self.activity_data_1, format="json").json()
        self.client.post("/api/activities/", self.activity_data_2, format="json").json()

        # create student 2
        self.client.post("/api/accounts/", self.student2_data, format="json")

        token = self.client.post(
            "/api/login/", self.student2_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create 2 activities for student 2
        self.client.post("/api/activities/", self.activity_data_3, format="json").json()
        self.client.post("/api/activities/", self.activity_data_4, format="json").json()

        # student 2 only sees his own
        student_2_activities = self.client.get("/api/activities/")

        self.assertEqual(len(student_2_activities.json()), 2)
        self.assertEqual(student_2_activities.status_code, 200)

    def test_facilitator_gets_all_activities(self):
        # create a student user
        self.client.post("/api/accounts/", self.student1_data, format="json")

        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create 2 activities for student 1
        self.client.post("/api/activities/", self.activity_data_1, format="json").json()
        self.client.post("/api/activities/", self.activity_data_2, format="json").json()

        # create a student user 2
        self.client.post("/api/accounts/", self.student2_data, format="json")

        token = self.client.post(
            "/api/login/", self.student2_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create 2 activities for student 2
        self.client.post("/api/activities/", self.activity_data_3, format="json").json()
        self.client.post("/api/activities/", self.activity_data_4, format="json").json()

        # create facilitator user
        self.client.post("/api/accounts/", self.facilitator_data, format="json")

        token = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        all_activities = self.client.get("/api/activities/")

        self.assertEqual(len(all_activities.json()), 4)
        self.assertEqual(all_activities.status_code, 200)

    def test_facilitator_can_filter_activities(self):
        # create student user
        self.client.post("/api/accounts/", self.student1_data, format="json")

        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create 2 activities for student 1
        self.client.post("/api/activities/", self.activity_data_1, format="json").json()
        self.client.post("/api/activities/", self.activity_data_2, format="json").json()

        # create a student user 2
        self.client.post("/api/accounts/", self.student2_data, format="json")

        token = self.client.post(
            "/api/login/", self.student2_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create 2 activities for student 2
        self.client.post("/api/activities/", self.activity_data_3, format="json").json()
        self.client.post("/api/activities/", self.activity_data_4, format="json").json()

        # create facilitator user
        self.client.post("/api/accounts/", self.facilitator_data, format="json")

        token = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        filtered_activities_1 = self.client.get("/api/activities/1/")
        filtered_activities_2 = self.client.get("/api/activities/2/")
        self.assertEqual(len(filtered_activities_1.json()), 2)
        self.assertEqual(len(filtered_activities_1.json()), 2)
        self.assertEqual(filtered_activities_1.status_code, 200)
        self.assertEqual(filtered_activities_2.status_code, 200)

    def test_facilitator_can_grade_activities(self):
        # test with no authentication
        response = self.client.post(
            "/api/activities/", self.activity_data, format="json"
        )
        self.assertEqual(response.status_code, 401)

        # create student user
        self.client.post("/api/accounts/", self.student1_data, format="json")

        # login
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create activity
        response = self.client.post(
            "/api/activities/", self.activity_data, format="json"
        )
        activity = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            activity, {"repo": "test repo", "user_id": 1, "id": 1, "grade": None}
        )

        # create facilitator user
        self.client.post("/api/accounts/", self.facilitator_data, format="json")

        token = self.client.post(
            "/api/login/", self.facilitator_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # facilitator updates activity
        response = self.client.put(
            "/api/activities/",
            {"id": 1, "grade": 90},
            format="json",
        )

        # switch to student account
        token = self.client.post(
            "/api/login/", self.student1_login_data, format="json"
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        activity = self.client.get("/api/activities/").json()[0]

        self.assertEqual(activity["grade"], 90)
