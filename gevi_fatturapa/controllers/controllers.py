# -*- coding: utf-8 -*-

from openerp import http


class FatturaElettronicaController(http.Controller):

    @http.route([
        '/fatturaelettronica/preview/<attachment_id>',
    ], type='http', auth='user', website=True)
    def pdf_preview(self, attachment_id, **data):
        attach = http.request.env['ir.attachment'].browse(int(attachment_id))
        xml = attach.get_xml_string()
        xmlhttpheaders = [
            ('Content-Type', 'application/xml'), ('Content-Length', len(xml))
        ]
        downloadhttpheaders=[
            ('Content-Type', 'text/xml'),
            ('Content-Disposition', 'attachment; filename=' + attachment_id),
            ('Content-Length', len(xml))
        ]
        return http.request.make_response(xml, headers=xmlhttpheaders)
