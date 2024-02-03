from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FormulirCuti(models.Model):
	_name = 'formulir.cuti'
	_description = 'formulir cuti'

	line_ids = fields.One2many(comodel_name='formulir.cuti.line', inverse_name='cuti_id', string='Cuti_ids')
	

	name = fields.Char(string='Nama', compute='_compute_name')
	wilayah = fields.Char(string='Wilayah', required=True)
	nik = fields.Char(string='NIK', required=True)
	jabatan = fields.Char(string='Jabatan')
	jml_hari = fields.Char(string='Jumlah Hari')
	alamat_cuti = fields.Char(string='Alamat Selama Cuti')
	ttd_pemohon = fields.Binary(string='Tanda Tangan Pemohon')
	no_tlp = fields.Char(string='No Telp Selama Cuti')
	jml_cuti = fields.Char(string='Jumlah Cuti disetujui')
	alasan = fields.Char(string='Alasan')
	ttd_manager = fields.Binary(string='Tanda Tangan')
	jatah_cuti = fields.Char(string='Jatah Cuti tahun berjalan')
	jml_cuti2 = fields.Char(string='Jumlah Cuti terpakai')
	cd_cuti = fields.Char(string='Cadangan Cuti bersama')
	sisa_cuti = fields.Char(string='Sisa Cuti Tersedia')
	ttd_hrd = fields.Binary(string='Tanda Tangan HRD/GA')
	jenis_cuti = fields.Selection(string='Jenis Cuti', selection=[
		('a','Cuti tahunan / biasa'),
		('b','Pernikahan karyawan/ti'),
		('c','Pernikahan anak kandung'),
		('d','Isteri melahirkan'),
		('e','Khitanan anak kandung'),
		('f','Pembaptisan anak kandung'),
		('g','Kematian keluarga tanggungan'),
		('h','Kematian orang tua / mertua'),
		('i','Cuti haid (khusus wanita)'),
		('j','Cuti melahirkan (khusus wanita)'),
		('k','Cuti pengganti hari libur')
		])
	state = fields.Selection(string='Status', selection=[
		('draft', 'Draft'),
		('confirm', 'Konfrimasi'),
		('review', 'review'),
		('approve', 'Setuju'),
		('done', 'Selesai'),
		],default='draft', tracking=True)

	@api.depends('create_uid')
	def _compute_name(self):
			for record in self:
				record.name = record.create_uid.name
			
	def action_confirm(self):
		self.state='confirm'
				
	def action_done(self):
		self.state='done'

	def action_draft(self):
		self.state='draft'	

	def action_review(self):
		self.state='review'	
	
	def action_approve(self):
		self.state='approve'

	def action_Reject(self):
		self.state='Reject'	



class FormulirCutiLIne(models.Model):
	_name = 'formulir.cuti.line'
	_description = 'Formulir Cuti LIne'

	cuti_id = fields.Many2one(comodel_name='formulir.cuti', string='cuti_id', ondelete='cascade', index=True)
	jenis_cuti = fields.Selection(string='Jenis Cuti', selection=[
		('a','Cuti tahunan / biasa'),
		('b','Pernikahan karyawan/ti'),
		('c','Pernikahan anak kandung'),
		('d','Isteri melahirkan'),
		('e','Khitanan anak kandung'),
		('f','Pembaptisan anak kandung'),
		('g','Kematian keluarga tanggungan'),
		('h','Kematian orang tua / mertua'),
		('i','Cuti haid (khusus wanita)'),
		('j','Cuti melahirkan (khusus wanita)'),
		('k','Cuti pengganti hari libur'),
		('l','Lainya'),
		],default="a", required=True)
	cuti_lainya = fields.Char(string='Cuti Lainya')
	tanggal_cuti = fields.Date(string='Tanggal Cuti')
	approval = fields.Selection(string='Approval', selection=[
		('draft', 'Draft'),
		('rejected', 'Rejected'),
		('approved', 'Approved'),
		], default='draft')
	
	def action_approve(self):
		self.approval='approved'

	def action_Reject(self):
		self.approval='rejected'

	approval_state_check = fields.Boolean(string="Approval State Check", compute="_compute_approval_state_check")

	@api.onchange('cuti_id.state')
	def _compute_approval_state_check(self):
		for record in self:
			record.approval_state_check = record.cuti_id.state != 'review'

	@api.constrains('tanggal_cuti','cuti_id.create_uid')
	def _check_duplicate_cuti_date(self):
		for rec in self:
			duplikate_cuti = self.env['formulir.cuti.line'].search([
				('tanggal_cuti', '=', rec.tanggal_cuti),
				('cuti_id.create_uid', '=', rec.cuti_id.create_uid.id),
				('id', '!=', rec.id)
		])
		if duplikate_cuti:
			raise ValidationError('Hayoooo gak boleh pakai tanggal yang sama !!!!.')
		
	