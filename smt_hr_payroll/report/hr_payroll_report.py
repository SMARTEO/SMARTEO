# -*- coding: utf-8 -*-


from psycopg2 import sql

from odoo import tools
from odoo import fields, models


class HrPayrollReport(models.Model):
    _inherit = "hr.payroll.report"

    idemnlog_wage = fields.Float('Indemnités transport', readonly=True)
    idemnrepas_wage = fields.Float('Indemnités repas', readonly=True)
    out_wage = fields.Float('Retenues pour absence', readonly=True)
    absmal2_wage = fields.Float('Congés maternité', readonly=True)
    primqu01_wage = fields.Float('Prime conditionnelle', readonly=True)
    primeass01_wage = fields.Float('Prime trimestrielle', readonly=True)
    primeperf01_wage = fields.Float('Prime exceptionnelle', readonly=True)
    preav01_wage = fields.Float('Préavis', readonly=True)
    idemn01_wage = fields.Float('Licenciement', readonly=True)
    indemn02_wage = fields.Float('Indemnité compensatrice de congé non prise', readonly=True)

    compcong01_wage = fields.Float('Compensatrice de Congés payés', readonly=True)
    cnaps_ps_wage = fields.Float('CNAPS (part salariale)', readonly=True)
    cnaps_pp_wage = fields.Float('CNaPS (part patronale)', readonly=True)
    ostie_ps_wage = fields.Float('OSTIE (part salariale)', readonly=True)
    ostie_pp_wage = fields.Float('OSTIE (part patronale)', readonly=True)
    fmfp_wage = fields.Float('FMFP', readonly=True)
    simpo_wage = fields.Float('SALAIRE IMPOSABLE', readonly=True)
    childnum_wage = fields.Float('Nombre enfant', readonly=True)
    irsa01_wage = fields.Float('IRSA', readonly=True)
    irsa03_wage = fields.Float('IRSA intermediaire', readonly=True)

    irsa02_wage = fields.Float('IRSA à payer', readonly=True)
    fraisbanc_wage = fields.Float('Frais bancaire', readonly=True)
    alloc_wage = fields.Float('Allocation familiale', readonly=True)
    ava15_wage = fields.Float('Avance sur salaire du 15', readonly=True)
    avansp_wage = fields.Float('Avance spéciale', readonly=True)
    rbstcnaps_wage = fields.Float('Remboursement CNAPS', readonly=True)
    totpopcom_wage = fields.Float('Total opérations complémentaires', readonly=True)
    ajustnet_wage = fields.Float('Ajustement de salaire net', readonly=True)
    gross_gross_wage = fields.Float('Salaire brut réel', invisible=True, readonly=True)


    def _select(self):
        return super()._select() + """,
                CASE WHEN wd.id = min_id.min_line THEN idemnlog.total ELSE 0 END as idemnlog_wage,
                CASE WHEN wd.id = min_id.min_line THEN idemnrepas.total ELSE 0 END as idemnrepas_wage,
                CASE WHEN wd.id = min_id.min_line THEN out.total ELSE 0 END as out_wage,
                CASE WHEN wd.id = min_id.min_line THEN absmal2.total ELSE 0 END as absmal2_wage,
                CASE WHEN wd.id = min_id.min_line THEN primqu01.total ELSE 0 END as primqu01_wage,
                CASE WHEN wd.id = min_id.min_line THEN primeass01.total ELSE 0 END as primeass01_wage,
                CASE WHEN wd.id = min_id.min_line THEN primeperf01.total ELSE 0 END as primeperf01_wage,
                CASE WHEN wd.id = min_id.min_line THEN preav01.total ELSE 0 END as preav01_wage,
                CASE WHEN wd.id = min_id.min_line THEN idemn01.total ELSE 0 END as idemn01_wage,
                CASE WHEN wd.id = min_id.min_line THEN indemn02.total ELSE 0 END as indemn02_wage,
                CASE WHEN wd.id = min_id.min_line THEN compcong01.total ELSE 0 END as compcong01_wage,
                CASE WHEN wd.id = min_id.min_line THEN cnaps_ps.total ELSE 0 END as cnaps_ps_wage,
                CASE WHEN wd.id = min_id.min_line THEN cnaps_pp.total ELSE 0 END as cnaps_pp_wage,
                CASE WHEN wd.id = min_id.min_line THEN ostie_ps.total ELSE 0 END as ostie_ps_wage,
                CASE WHEN wd.id = min_id.min_line THEN ostie_pp.total ELSE 0 END as ostie_pp_wage,
                CASE WHEN wd.id = min_id.min_line THEN fmfp.total ELSE 0 END as fmfp_wage,
                CASE WHEN wd.id = min_id.min_line THEN simpo.total ELSE 0 END as simpo_wage,
                CASE WHEN wd.id = min_id.min_line THEN childnum.total ELSE 0 END as childnum_wage,
                CASE WHEN wd.id = min_id.min_line THEN irsa01.total ELSE 0 END as irsa01_wage,
                CASE WHEN wd.id = min_id.min_line THEN irsa03.total ELSE 0 END as irsa03_wage,
                CASE WHEN wd.id = min_id.min_line THEN irsa02.total ELSE 0 END as irsa02_wage,
                CASE WHEN wd.id = min_id.min_line THEN fraisbanc.total ELSE 0 END as fraisbanc_wage,
                CASE WHEN wd.id = min_id.min_line THEN alloc.total ELSE 0 END as alloc_wage,
                CASE WHEN wd.id = min_id.min_line THEN ava15.total ELSE 0 END as ava15_wage,
                CASE WHEN wd.id = min_id.min_line THEN avansp.total ELSE 0 END as avansp_wage,
                CASE WHEN wd.id = min_id.min_line THEN rbstcnaps.total ELSE 0 END as rbstcnaps_wage,
                CASE WHEN wd.id = min_id.min_line THEN totpopcom.total ELSE 0 END as totpopcom_wage,
                CASE WHEN wd.id = min_id.min_line THEN ajustnet.total ELSE 0 END as ajustnet_wage,
                CASE WHEN wd.id = min_id.min_line THEN gross.total ELSE 0 END as gross_gross_wage
                """

    def _from(self):
        return super()._from() + """
                left join hr_payslip_line idemnlog on (idemnlog.slip_id = p.id and idemnlog.code = 'INDEMNLOG')
                left join hr_payslip_line idemnrepas on (idemnrepas.slip_id = p.id and idemnrepas.code = 'INDEMNREPAS')
                left join hr_payslip_line out on (out.slip_id = p.id and out.code = 'OUT')
                left join hr_payslip_line absmal2 on (absmal2.slip_id = p.id and absmal2.code = 'ABSMAL2')
                left join hr_payslip_line primqu01 on (primqu01.slip_id = p.id and primqu01.code = 'PRIMQU01')
                left join hr_payslip_line primeass01 on (primeass01.slip_id = p.id and primeass01.code = 'PRIMEASS01')
                left join hr_payslip_line primeperf01 on (primeperf01.slip_id = p.id and primeperf01.code = 'PRIMEPERF01')
                left join hr_payslip_line preav01 on (preav01.slip_id = p.id and preav01.code = 'PREAV01')
                left join hr_payslip_line idemn01 on (idemn01.slip_id = p.id and idemn01.code = 'INDEMN01')
                left join hr_payslip_line indemn02 on (indemn02.slip_id = p.id and indemn02.code = 'INDEMN02')
                left join hr_payslip_line compcong01 on (compcong01.slip_id = p.id and compcong01.code = 'COMPCONG01')
                left join hr_payslip_line cnaps_ps on (cnaps_ps.slip_id = p.id and cnaps_ps.code = 'CNaPS - PS')
                left join hr_payslip_line cnaps_pp on (cnaps_pp.slip_id = p.id and cnaps_pp.code = 'CNaPS - PP')
                left join hr_payslip_line ostie_ps on (ostie_ps.slip_id = p.id and ostie_ps.code = 'OSTIE - PS')
                left join hr_payslip_line ostie_pp on (ostie_pp.slip_id = p.id and ostie_pp.code = 'OSTIE - PP')
                left join hr_payslip_line fmfp on (fmfp.slip_id = p.id and fmfp.code = 'FMFP')
                left join hr_payslip_line simpo on (simpo.slip_id = p.id and simpo.code = 'SIMPO')
                left join hr_payslip_line childnum on (childnum.slip_id = p.id and childnum.code = 'CHILDNUM')
                left join hr_payslip_line irsa01 on (irsa01.slip_id = p.id and irsa01.code = 'IRSA01')
                left join hr_payslip_line irsa03 on (irsa03.slip_id = p.id and irsa03.code = 'IRSA03')
                left join hr_payslip_line irsa02 on (irsa02.slip_id = p.id and irsa02.code = 'IRSA02')
                left join hr_payslip_line fraisbanc on (fraisbanc.slip_id = p.id and fraisbanc.code = 'FRAISBANC')
                left join hr_payslip_line alloc on (alloc.slip_id = p.id and alloc.code = 'ALLOC')
                left join hr_payslip_line ava15 on (ava15.slip_id = p.id and ava15.code = 'ava15')
                left join hr_payslip_line avansp on (avansp.slip_id = p.id and avansp.code = 'AVANSP')
                left join hr_payslip_line rbstcnaps on (rbstcnaps.slip_id = p.id and rbstcnaps.code = 'RBSTCNAPS')
                left join hr_payslip_line totpopcom on (totpopcom.slip_id = p.id and totpopcom.code = 'TOTPOPCOM')
                left join hr_payslip_line ajustnet on (ajustnet.slip_id = p.id and ajustnet.code = 'AJUSTNET')
                left join hr_payslip_line gross on (gross.slip_id = p.id and gross.code = 'SBRUT')
                """

    def _group_by(self):
        return super()._group_by() + """,
                idemnlog.total,
                idemnrepas.total,
                out.total,
                absmal2.total,
                primqu01.total,
                primeass01.total,
                primeperf01.total,
                preav01.total,
                idemn01.total,
                indemn02.total,
                compcong01.total,
                cnaps_ps.total,
                cnaps_pp.total,
                ostie_ps.total,
                ostie_pp.total,
                fmfp.total,
                simpo.total,
                childnum.total,
                irsa01.total,
                irsa03.total,
                irsa02.total,
                fraisbanc.total,
                alloc.total,
                ava15.total,
                avansp.total,
                rbstcnaps.total,
                totpopcom.total,
                ajustnet.total,
                gross.total
                """
