from odoo.http import request

from odoo.addons.survey.controllers.main import Survey


class SurveyCtrol(Survey):
    def _check_validity(
        self, survey_token, answer_token, ensure_token=True, check_partner=True
    ):
        """
        * survey_void: survey is void and should not be taken;
        """
        resp = super()._check_validity(
            survey_token, answer_token, ensure_token, check_partner
        )
        if resp is not True:
            return resp
        survey_sudo = self._fetch_from_access_token(survey_token, answer_token)[0]
        respondent = request.env.user
        if survey_sudo.questions_layout == "page_per_section":
            valid_pages = survey_sudo._filter_pages_or_questions(
                survey_sudo.page_ids, respondent
            )
            if not valid_pages:
                return "survey_void"
        valid_questions = survey_sudo._filter_pages_or_questions(
            survey_sudo.question_ids, respondent
        )
        if not valid_questions:
            return "survey_void"
        return resp
