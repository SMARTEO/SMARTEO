# -*- coding: utf-8 -*-
import odoo
import odoo.modules.registry

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo.tools.translate import _

# The Home controller and ensure_db() moved in v17+.
try:
    from odoo.addons.web.controllers.home import Home as HomeBase
    from odoo.addons.web.controllers.utils import ensure_db
except ImportError:
    from odoo.addons.web.controllers.main import Home as HomeBase
    from odoo.addons.web.controllers.main import ensure_db


class Home(HomeBase):

    @http.route('/web/login', type='http', auth="public")
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            ip_address = request.httprequest.environ.get('REMOTE_ADDR', '')
            login = request.params.get('login')
            if login:
                user_rec = request.env['res.users'].sudo().search([('login', '=', login)])
                if user_rec.allowed_ips:
                    allowed = [rec.ip_address for rec in user_rec.allowed_ips]
                    if ip_address in allowed:
                        try:
                            uid = request.session.authenticate(
                                request.session.db,
                                request.params['login'],
                                request.params['password'],
                            )
                            request.params['login_success'] = True
                            return request.redirect(self._login_redirect(uid, redirect=redirect))
                        except odoo.exceptions.AccessDenied as e:
                            request.uid = old_uid
                            if e.args == odoo.exceptions.AccessDenied().args:
                                values['error'] = _("Wrong login/password")
                    else:
                        request.uid = old_uid
                        values['error'] = _("Not allowed to login from this IP address")
                else:
                    try:
                        uid = request.session.authenticate(
                            request.session.db,
                            request.params['login'],
                            request.params['password'],
                        )
                        request.params['login_success'] = True
                        return request.redirect(self._login_redirect(uid, redirect=redirect))
                    except odoo.exceptions.AccessDenied as e:
                        request.uid = old_uid
                        if e.args == odoo.exceptions.AccessDenied().args:
                            values['error'] = _("Wrong login/password")

        return request.render('web.login', values)
