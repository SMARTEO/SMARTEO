# -*- coding: utf-8 -*-
from datetime import date

from dateutil.relativedelta import relativedelta
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrChildAge(TransactionCase):
    def test_no_birthday_gives_zero_age(self):
        child = self.env["hr.child"].create({"name": "No Birthday Child"})

        self.assertEqual(child.child_age, 0)

    def test_child_of_21_is_still_dependent(self):
        birthday = date.today() - relativedelta(years=21)
        child = self.env["hr.child"].create({"name": "Boundary Child", "birthday": birthday})

        self.assertEqual(child.child_age, 21)
        self.assertEqual(child.state, "dependent")

    def test_child_of_22_is_not_dependent(self):
        birthday = date.today() - relativedelta(years=22)
        child = self.env["hr.child"].create({"name": "Adult Child", "birthday": birthday})

        self.assertEqual(child.child_age, 22)
        self.assertEqual(child.state, "not_dependent")

    def test_age_recomputes_when_birthday_changes(self):
        child = self.env["hr.child"].create(
            {
                "name": "Growing Child",
                "birthday": date.today() - relativedelta(years=5),
            }
        )
        # Reading child_age first forces _compute_age() to run; it is the only
        # field formally wired as this method's compute target (see state's
        # caveat below).
        self.assertEqual(child.child_age, 5)
        self.assertEqual(child.state, "dependent")

        child.birthday = date.today() - relativedelta(years=25)

        self.assertEqual(child.child_age, 25)
        self.assertEqual(child.state, "not_dependent")

    def test_state_is_only_refreshed_when_child_age_is_accessed_first(self):
        # `state` is set as a side effect inside _compute_age(), but only
        # `child_age` is declared with compute='_compute_age' on the field
        # itself. Odoo only reruns a compute method when one of its declared
        # target fields is accessed/flushed, so reading `state` before ever
        # touching `child_age` can surface a stale value. This test documents
        # that current, easy-to-miss behavior rather than the intended one.
        child = self.env["hr.child"].create(
            {
                "name": "Order Sensitive Child",
                "birthday": date.today() - relativedelta(years=5),
            }
        )

        self.assertFalse(child.state)

        self.assertEqual(child.child_age, 5)
        self.assertEqual(child.state, "dependent")
