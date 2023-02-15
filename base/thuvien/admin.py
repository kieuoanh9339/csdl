from django.contrib import admin
from thuvien.models import Sach, NguoiMuon, TheMuon, TheMuon_Sach

class SachAdmin(admin.ModelAdmin):
    list_display = ['maSach', 'tenSach', 'tacGia', 'theLoai', 'ngonNgu', 'soLuong']
    list_display_links = ['tenSach']
    search_fields = ['maSach', 'tenSach', 'tacGia', 'theLoai', 'ngonNgu']

class NguoiMuonAdmin(admin.ModelAdmin):
    list_display = ['masv', 'ten', 'namSinh', 'email', 'sach_da_muon']
    list_display_links = ['masv', 'ten']
    search_fields = ['masv', 'ten', 'namSinh', 'email']

class TheMuonAdmin(admin.ModelAdmin):
    def ngayMuonFormat(self, obj):
        return obj.ngayMuon.strftime('%d-%m-%Y')
    ngayMuonFormat.short_description = 'Ngay Muon'
    def ngayTraFormat(self, obj):
        return obj.ngayTra.strftime('%d-%m-%Y')
    ngayTraFormat.short_description = 'Ngay Tra'
    list_display = ['maThe', 'nguoiMuon', 'ngayMuonFormat', 'ngayTraFormat', 'so_dau_sach']
    list_display_links = ['maThe']
    search_fields = ['maThe', 'nguoiMuon__masv', 'nguoiMuon__ten', 'nguoiMuon__namSinh', 'nguoiMuon__email']

class TheMuon_SachAdmin(admin.ModelAdmin):
    list_display = ['themuon', 'sach', 'soLuong']
    list_display_links = ['themuon', 'sach']
    list_filter = ['themuon', 'sach']
    

# Register your models here.
admin.site.register(Sach, SachAdmin)
admin.site.register(NguoiMuon, NguoiMuonAdmin)
admin.site.register(TheMuon, TheMuonAdmin)
admin.site.register(TheMuon_Sach, TheMuon_SachAdmin)