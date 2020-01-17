import os
import sys

from locust import HttpLocust, TaskSet, seq_task

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.database import DatabaseConnection

del sys.path[0]


class UserBehavior(TaskSet):

    dev = DatabaseConnection(section="api_token")
    token = dev.get_access_key()
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + token[0],
    }

    def _iterate_student(self, response):
        for student in response.json()["data"]:
            self.client.get(
                "/students/" + student["student_uuid"] + "/photos/",
                headers=self.headers,
                name="Get Student Photo",
            )
            self.client.get(
                "/students/" + student["student_uuid"] + "/assessment/early_years/",
                headers=self.headers,
                name="Get Student assessment early years",
            )
            self.client.get(
                "/students/" + student["student_uuid"] + "/assessment/statutory/",
                headers=self.headers,
                name="Get Student assessment statutory",
            )
            self.client.get(
                "/students/" + student["student_uuid"] + "/assessment/steps/",
                headers=self.headers,
                name="Get Student assessment steps",
            )
            self.client.get(
                "/students/" + student["student_uuid"] + "/contacts/",
                headers=self.headers,
                name="Get Student contacts",
            )
            self.client.get(
                "/students/" + student["student_uuid"] + "/exclusions/",
                headers=self.headers,
                name="Get Student exclusions",
            )
            self.client.get(
                "/students/" + student["student_uuid"] + "/meals/",
                headers=self.headers,
                name="Get Student meals",
            )
            self.client.get(
                "/students/" + student["student_uuid"] + "/register/",
                headers=self.headers,
                name="Get Student register",
            )
            self.client.get(
                "/students/" + student["student_uuid"] + "/register/historic/",
                headers=self.headers,
                name="Get Student register historic",
            )
            self.client.get(
                "/students/sen/" + student["student_uuid"],
                headers=self.headers,
                name="Get Student sen records",
            )
            self.client.get(
                "/students/lac/" + student["student_uuid"],
                headers=self.headers,
                name="Get Student lac records",
            )

    def _iterate_staff(self, response):
        for staff in response.json()["data"]:
            self.client.get(
                "/staff/" + staff["staff_uuid"] + "/contracts/",
                headers=self.headers,
                name="Get Staff contracts",
            )
            self.client.get(
                "/staff/" + staff["staff_uuid"] + "/register/",
                headers=self.headers,
                name="Get Staff register",
            )

    @seq_task(4)
    def apapi_student(self):
        response = self.client.get(
            "/students/", headers=self.headers, name="Get Student List"
        )
        next = response.json()["next_uri"]
        while next:
            self._iterate_student(response)
            response = self.client.get(
                next, headers=self.headers, name="Get next Student List"
            )
            next = response.json()["next_uri"]

    @seq_task(2)
    def apapi_staff(self):
        response = self.client.get(
            "/staff/", headers=self.headers, name="Get Staff List"
        )
        next = response.json()["next_uri"]
        if next:
            while next:
                self._iterate_staff(response)
                response = self.client.get(
                    next, headers=self.headers, name="Get next Staff List"
                )
                next = response.json()["next_uri"]
        else:
            self._iterate_staff(response)

    @seq_task(3)
    def apapi_class(self):
        self.client.get("/classes/", headers=self.headers, name="Get Class")

    @seq_task(1)
    def apapi_school(self):
        self.client.get("/school/", headers=self.headers, name="Get School")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
