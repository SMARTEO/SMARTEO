from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrLeaveType(TransactionCase):
    def test_is_of_the_paid_leave_type_round_trip(self):
        leave_type = self.env["hr.leave.type"].create(
            {
                "name": "Paid Test Leave",
                "requires_allocation": True,
                "is_of_the_paid_leave_type": True,
            }
        )

        self.assertTrue(leave_type.is_of_the_paid_leave_type)

    def test_is_of_the_paid_leave_type_defaults_to_false(self):
        leave_type = self.env["hr.leave.type"].create(
            {
                "name": "Unspecified Leave",
                "requires_allocation": True,
            }
        )

        self.assertFalse(leave_type.is_of_the_paid_leave_type)
