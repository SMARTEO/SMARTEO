def migrate(cr, version):
    cr.execute("""
        UPDATE hr_employee
        SET smt_phone = phone
        WHERE phone IS NOT NULL
          AND phone != ''
    """)
