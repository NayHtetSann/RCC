from odoo import fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    group_ids = fields.Many2many(
        "res.groups",
    )

    def _shown_by_user(self, respondent):
        """
        Check if a question should be shown to the respondent.
        If yes, check its page next.
        :param recordset respondent: the user to check
        :return boolean
        """
        self.ensure_one()
        if not respondent:
            return False
        if not self.group_ids:
            if self.page_id:
                return self.page_id._shown_by_user(respondent)
            return True
        self._cr.execute(
            """SELECT 1 FROM res_groups_users_rel WHERE uid=%s AND gid IN %s""",
            (respondent.id, tuple(self.group_ids.ids)),
        )
        if bool(self._cr.fetchone()):
            # Check its page
            if self.page_id:
                return self.page_id._shown_by_user(respondent)
            return True
        return False
