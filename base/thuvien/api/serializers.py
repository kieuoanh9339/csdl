from django.db.models import fields
from rest_framework import serializers
from thuvien.models import Sach, NguoiMuon, TheMuon, TheMuon_Sach

class SachSerializer(serializers.ModelSerializer):
    maSach = serializers.IntegerField()
    tenSach = serializers.CharField(max_length=200)
    tacGia = serializers.CharField(max_length=200)
    theLoai = serializers.CharField(max_length=100)
    ngonNgu = serializers.CharField(max_length=100)
    soLuong = serializers.IntegerField(default=0)

    class Meta:
        model = Sach
        fields = ['maSach', 'tenSach', 'tacGia', 'theLoai', 'ngonNgu', 'soLuong']

class NguoiMuonSerializer(serializers.ModelSerializer):
    ten = serializers.CharField(max_length=200)
    masv = serializers.CharField(max_length=50)
    matkhau = serializers.CharField(max_length=100)
    token = serializers.CharField(max_length=1000, read_only=True)
    namSinh = serializers.IntegerField()
    email = serializers.EmailField()

    class Meta:
        model = NguoiMuon
        fields = ['ten', 'masv', 'matkhau', 'namSinh', 'email', 'token']

class TheMuonSerializer(serializers.ModelSerializer):
    nguoiMuon = serializers.PrimaryKeyRelatedField(queryset=NguoiMuon.objects.all())
    ngayMuon = serializers.DateField()
    ngayTra = serializers.DateField()

    class Meta:
        model = TheMuon
        fields = ['maThe', 'nguoiMuon', 'ngayMuon', 'ngayTra']

class TheMuonSachSerializer(serializers.ModelSerializer):
    themuon = serializers.PrimaryKeyRelatedField(queryset=TheMuon.objects.all())
    sach = serializers.PrimaryKeyRelatedField(queryset=Sach.objects.all())

    class Meta:
        model = TheMuon_Sach
        fields = ['themuon', 'sach']