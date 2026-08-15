from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrClassification(TransactionCase):
    def test_create_classification(self):
        classification = self.env["hr.classification"].create({"name": "Manager"})

        self.assertEqual(classification.name, "Manager")


@tagged("post_install", "-at_install")
class TestHrEmployeeIdentity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.classification = cls.env["hr.classification"].create({"name": "Technician"})
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Jean Rakoto",
                "cnaps": "CNAPS-001",
                "ostie": "OSTIE-001",
                "matricule": "MAT-001",
                "classification_id": cls.classification.id,
                # smt_hr_contract makes hr.version.wage required without
                # precompute=True; every employee/version creation across the
                # whole database must set it explicitly or it fails with a
                # NOT NULL violation (see summary note in the PR/report).
                "wage": 1000,
            }
        )

    def test_employee_identity_fields(self):
        self.assertEqual(self.employee.cnaps, "CNAPS-001")
        self.assertEqual(self.employee.ostie, "OSTIE-001")
        self.assertEqual(self.employee.matricule, "MAT-001")
        self.assertEqual(self.employee.classification_id, self.classification)

    def test_children_ids_reverse_relation(self):
        child = self.env["hr.child"].create(
            {
                "name": "Employee Child",
                "employe_id": self.employee.id,
            }
        )

        self.assertIn(child, self.employee.children_ids)

    def test_public_employee_mirrors_identity_fields(self):
        public_employee = self.env["hr.employee.public"].browse(self.employee.id)

        self.assertEqual(public_employee.cnaps, "CNAPS-001")
        self.assertEqual(public_employee.ostie, "OSTIE-001")
        self.assertEqual(public_employee.matricule, "MAT-001")
        self.assertEqual(public_employee.classification_id, self.classification)

    def test_public_employee_children_ids_reverse_relation(self):
        child = self.env["hr.child"].create(
            {
                "name": "Public Employee Child",
                "employe_public_id": self.employee.id,
            }
        )
        public_employee = self.env["hr.employee.public"].browse(self.employee.id)

        self.assertIn(child, public_employee.children_ids)
