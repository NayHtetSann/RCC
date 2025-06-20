from odoo.tests.common import HttpCase

from odoo.addons.survey.tests import common


class TestSurveyController(common.TestSurveyCommon, HttpCase):
    def setUp(cls):
        super().setUp()
        cls.group_survey_manager = cls.env.ref("survey.group_survey_manager", False)
        cls.survey.users_login_required = False
        cls.survey.questions_layout = "page_per_section"

    def test_normal(self):
        survey = self.survey
        r = self._access_start(survey)
        self.assertResponse(r, 200, [survey.title])

        answers = self.env["survey.user_input"].search([("survey_id", "=", survey.id)])
        self.assertEqual(len(answers), 1)
        answer_token = answers.access_token
        self.assertTrue(answer_token)
        self.assertAnswer(answers, "new", self.env["survey.question"])

    def test_page_with_group(self):
        survey = self.survey
        self.page_0.group_ids |= self.group_survey_manager
        r = self._access_start(survey)
        self.assertResponse(r, 200, ["No question yet, come back later."])

        answers = self.env["survey.user_input"].search([("survey_id", "=", survey.id)])
        self.assertEqual(len(answers), 0)
        answer_token = answers.access_token
        self.assertFalse(answer_token)

    def test_page_with_group_2(self):
        survey = self.survey
        self.page_0.group_ids |= self.group_survey_manager
        page_1 = self.env["survey.question"].create(
            {
                "is_page": True,
                "question_type": False,
                "sequence": 4,
                "title": "Page2: Page without group",
                "survey_id": survey.id,
            }
        )
        self._add_question(
            page_1,
            "What do you like most",
            "multiple_choice",
            labels=[
                {"value": "The 1"},
                {"value": "The 2"},
                {"value": "The 3"},
                {"value": "The 4"},
            ],
            survey_id=survey.id,
        )

        r = self._access_start(survey)
        self.assertResponse(r, 200, [survey.title])

        answers = self.env["survey.user_input"].search([("survey_id", "=", survey.id)])
        self.assertEqual(len(answers), 1)
        answer_token = answers.access_token
        self.assertTrue(answer_token)
        self.assertAnswer(answers, "new", self.env["survey.question"])

    def test_question(self):
        survey = self.survey
        survey.questions_layout = "page_per_question"
        self._access_start(survey)

        answers = self.env["survey.user_input"].search([("survey_id", "=", survey.id)])
        self.assertEqual(len(answers), 1)
        answer_token = answers.access_token
        self.assertTrue(answer_token)
        self.assertEqual(len(answers.predefined_question_ids), 2)

    def test_question_with_group(self):
        survey = self.survey
        survey.questions_layout = "page_per_question"
        survey.question_ids.group_ids |= self.group_survey_manager
        r = self._access_start(survey)
        self.assertResponse(r, 200, ["No question yet, come back later."])

        answers = self.env["survey.user_input"].search([("survey_id", "=", survey.id)])
        self.assertEqual(len(answers), 0)
        answer_token = answers.access_token
        self.assertFalse(answer_token)
        self.assertEqual(len(answers.predefined_question_ids), 0)

    def test_question_with_group_2(self):
        survey = self.survey
        survey.questions_layout = "page_per_question"
        survey.question_ids[0].group_ids |= self.group_survey_manager
        self._access_start(survey)

        answers = self.env["survey.user_input"].search([("survey_id", "=", survey.id)])
        self.assertEqual(len(answers), 1)
        answer_token = answers.access_token
        self.assertTrue(answer_token)
        self.assertAnswer(answers, "new", self.env["survey.question"])
        self.assertEqual(len(answers.predefined_question_ids), 1)

    def test_question_one_page(self):
        survey = self.survey
        survey.questions_layout = "one_page"
        self._access_start(survey)

        answers = self.env["survey.user_input"].search([("survey_id", "=", survey.id)])
        self.assertEqual(len(answers), 1)
        answer_token = answers.access_token
        self.assertTrue(answer_token)
        self.assertEqual(len(answers.predefined_question_ids), 2)

    def test_question_one_page_group(self):
        survey = self.survey
        survey.questions_layout = "one_page"

        survey.question_ids.group_ids |= self.group_survey_manager
        r = self._access_start(survey)
        self.assertResponse(r, 200, ["No question yet, come back later."])

        answers = self.env["survey.user_input"].search([("survey_id", "=", survey.id)])
        self.assertEqual(len(answers), 0)
        answer_token = answers.access_token
        self.assertFalse(answer_token)
        self.assertEqual(len(answers.predefined_question_ids), 0)

    def test_question_one_page_group_2(self):
        survey = self.survey
        survey.questions_layout = "one_page"
        self.page_0.group_ids |= self.group_survey_manager
        survey.question_ids.page_id = self.page_0

        r = self._access_start(survey)
        self.assertResponse(r, 200, ["No question yet, come back later."])

        answers = self.env["survey.user_input"].search([("survey_id", "=", survey.id)])
        self.assertEqual(len(answers), 0)
        answer_token = answers.access_token
        self.assertFalse(answer_token)
        self.assertEqual(len(answers.predefined_question_ids), 0)
