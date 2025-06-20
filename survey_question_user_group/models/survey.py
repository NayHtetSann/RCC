from odoo import api, models


class Survey(models.Model):
    _inherit = "survey.survey"

    # ------------------------------------------------------------
    # QUESTIONS MANAGEMENT
    # ------------------------------------------------------------

    @api.model
    def _get_pages_or_questions(self, user_input):
        """Returns the pages or questions (depending on the layout) that will be shown
        to the user taking the survey.
        In 'page_per_question' layout, we also want to show pages
        that have a description."""

        result = super()._get_pages_or_questions(user_input)
        if not result:
            return result

        # Filter the result (survey.question) by groups
        return self._filter_pages_or_questions(result, self.env.user)

    @api.model
    def _filter_pages_or_questions(self, result, respondent, reverse=False):
        """
        Filter the results before showing on the survey
        :param recordset result: pages or questions
        :param recordset respondent: the respondent
        :param boolean reverse: flag to return the reversed ones
        :return recordset new_result: pages or questions
        """
        new_result = result.filtered(
            lambda rec, resp=respondent: rec._shown_by_user(resp)
        )
        if reverse:
            return result - new_result
        return new_result

    def _prepare_user_input_predefined_questions(self):
        """
        Override to filter the results when predefined questions
        :param recordset result: pages or questions
        :param recordset respondent: the respondent
        :param boolean reverse: flag to return the reversed ones
        :return recordset new_result: pages or questions
        """
        questions = super()._prepare_user_input_predefined_questions()
        return self._filter_pages_or_questions(questions, self.env.user)
