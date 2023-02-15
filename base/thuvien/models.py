from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Sach(models.Model):
    def __str__(self) -> str:
        return self.tenSach
    
    maSach = models.IntegerField(primary_key=True)
    tenSach = models.CharField(max_length=200)
    tacGia = models.CharField(max_length=200)
    theLoai = models.CharField(max_length=100)
    ngonNgu = models.CharField(max_length=100)
    soLuong = models.IntegerField(default=0)


class NguoiMuon(models.Model):
    def __str__(self) -> str:
        return self.ten
    def sach_da_muon(self):
        themuons = TheMuon.objects.filter(nguoiMuon=self)
        tm_s = TheMuon_Sach.objects.filter(themuon__in=themuons)
        return len(Sach.objects.filter(maSach__in=tm_s.values('sach')))

    ten = models.CharField(max_length=200)
    masv = models.CharField(max_length=50, primary_key=True)
    matkhau = models.CharField(max_length=100, default=None) 
    namSinh = models.IntegerField()
    email = models.CharField(max_length=200)
    token = models.CharField(max_length=1000, default=None, null=True)


class TheMuon(models.Model):
    def __str__(self) -> str:
        return str(self.maThe)
    def so_dau_sach(self):
        return len(TheMuon_Sach.objects.filter(themuon=self))

    maThe = models.BigAutoField(primary_key=True)
    nguoiMuon = ForeignKey(NguoiMuon, on_delete=models.CASCADE)
    ngayMuon = models.DateField(auto_now_add=True)
    ngayTra = models.DateField()
    

class TheMuon_Sach(models.Model):
    def __str__(self) -> str:
        return self.themuon.nguoiMuon.ten + " - " + self.sach.tenSach

    themuon = ForeignKey(TheMuon, on_delete=models.CASCADE)
    sach = ForeignKey(Sach, on_delete=models.CASCADE)
    soLuong = models.IntegerField(default=0)