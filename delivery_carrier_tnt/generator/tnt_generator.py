# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 FactorLibre (http://www.factorlibre.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import unicodedata
from datetime import datetime
from openerp.addons.base_delivery_carrier_files.generator import \
    CarrierFileGenerator
import logging
_logger = logging.getLogger(__name__)


class TNTFileGenerator(CarrierFileGenerator):

    @classmethod
    def carrier_for(cls, carrier_name):
        return carrier_name == 'tnt'

    def _get_rows(self, picking, configuration):
        result = [[]]
        if (not picking.notified2carrier) and \
                picking.lines_manifest and picking.datetime_label:
            result = [[picking.lines_manifest]]
            if not picking.carrier_id.tnt_config_id.is_test:
                picking.notified2carrier = True
        return result

    def _write_rows(self, file_handle, rows, configuration):
        """
        Write the rows in the file (file_handle)

        :param StringIO file_handle: file to write in
        :param rows: rows to write in the file
        :param browse_record configuration: configuration of the file to
               generate
        :return: the file_handle as StringIO with the rows written in it
        """
        row_text = ""
        for row in rows:
            if row:
                row_text += u"{}\n".format("".join(row))
        row_text = unicodedata.normalize('NFKD', row_text).encode(
            'ascii', 'ignore')
        file_handle.write(row_text)
        return file_handle

    def _tnt_filename(self, configuration):
        date_now = datetime.now()
        formatted_date = date_now.strftime('%Y%m%d%H%M%S')
        company_name = configuration.tnt_company_name
        ir_sequence_env = configuration.env['ir.sequence']
        file_sufix_number = ir_sequence_env.next_by_id(
            configuration.tnt_filename_sequence.id)
        contador = file_sufix_number.zfill(4)
        return "FD6CNFF_{}_{}.{}".format(
            company_name, formatted_date, contador)

    def _get_filename_grouped(self, configuration, extension='csv'):
        return self._tnt_filename(configuration)

    def _get_filename_single(self, picking, configuration, extension='csv'):
        return self._tnt_filename(configuration)

    def generate_files(self, pickings, configuration):
        res = super(TNTFileGenerator, self).generate_files(
            pickings, configuration)
        return res
