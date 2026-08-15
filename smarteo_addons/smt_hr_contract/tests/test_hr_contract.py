from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrVersionWageAndHours(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.classification = cls.env["hr.classification"].create({"name": "Senior Technician"})
        # hr.version.wage is a required, non-precomputed stored compute field
        # (see smt_hr_contract._compute_wage): it must be supplied explicitly
        # at creation time, otherwise the initial INSERT violates the NOT
        # NULL constraint before the compute ever runs.
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Contract Test Employee",
                "classification_id": cls.classification.id,
                "wage": 0,
            }
        )

    def test_wage_mirrors_base_salary(self):
        self.employee.base_salary = 1733.33

        self.assertEqual(self.employee.wage, 1733.33)

    def test_wage_updates_when_base_salary_changes_again(self):
        self.employee.base_salary = 1000.0
        self.assertEqual(self.employee.wage, 1000.0)

        self.employee.base_salary = 2500.0

        self.assertEqual(self.employee.wage, 2500.0)

    def test_classification_id_follows_employee(self):
        self.assertEqual(self.employee.version_id.classification_id, self.classification)

        other_classification = self.env["hr.classification"].create({"name": "Junior Technician"})
        self.employee.classification_id = other_classification.id

        self.assertEqual(self.employee.version_id.classification_id, other_classification)

    def test_hourly_salary_default_full_time_calendar(self):
        self.employee.base_salary = 1733.33
        self.assertEqual(self.employee.hour_per_week, 40.0)

        self.assertAlmostEqual(self.employee.hourly_salary, 10.0, places=2)

    def test_hourly_salary_zero_when_no_weekly_hours(self):
        part_time_calendar = self.env["resource.calendar"].create(
            {
                "name": "Zero Hours Calendar",
                "full_time_required_hours": 0,
                "hours_per_day": 0,
            }
        )
        self.employee.resource_calendar_id = part_time_calendar.id
        self.employee.base_salary = 1733.33

        self.assertEqual(self.employee.hour_per_week, 0.0)
        self.assertEqual(self.employee.hourly_salary, 0.0)
