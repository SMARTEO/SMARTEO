# -*- coding: utf-8 -*-
import openai

from odoo import models, _
from odoo.exceptions import UserError


class DiscussChannel(models.Model):
    _inherit = 'discuss.channel'

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        rdata = super()._notify_thread(message, msg_vals=msg_vals, **kwargs)
        chatgpt_channel_id = self.env.ref('is_chatgpt_integration.channel_chatgpt')
        user_chatgpt = self.env.ref("is_chatgpt_integration.user_chatgpt")
        partner_chatgpt = self.env.ref("is_chatgpt_integration.partner_chatgpt")
        author_id = msg_vals.get('author_id')
        chatgpt_name = str(partner_chatgpt.name or '') + ', '
        prompt = msg_vals.get('body')
        if not prompt:
            return rdata

        api_key = self.env['ir.config_parameter'].sudo().get_param(
            'is_chatgpt_integration.openapi_api_key'
        )
        client = openai.OpenAI(api_key=api_key)

        partner_name = ''
        if author_id:
            partner = self.env['res.partner'].browse(author_id)
            if partner:
                partner_name = partner.name

        is_dm_with_chatgpt = (
            author_id != partner_chatgpt.id
            and (
                chatgpt_name in msg_vals.get('record_name', '')
                or 'ChatGPT,' in msg_vals.get('record_name', '')
            )
            and self.channel_type == 'chat'
        )
        is_chatgpt_channel = (
            author_id != partner_chatgpt.id
            and msg_vals.get('model', '') == 'discuss.channel'
            and msg_vals.get('res_id', 0) == chatgpt_channel_id.id
        )

        if is_dm_with_chatgpt or is_chatgpt_channel:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6,
                    max_tokens=3000,
                    user=partner_name or "user",
                )
                res = response.choices[0].message.content
                target = chatgpt_channel_id if is_chatgpt_channel else self
                target.with_user(user_chatgpt).message_post(
                    body=res,
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment',
                )
            except Exception as e:
                raise UserError(_(str(e)))

        return rdata
