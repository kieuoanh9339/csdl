from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .auth import createToken, auth
from django.db import connection
from .serializers import NguoiMuonSerializer, SachSerializer, TheMuonSerializer

from thuvien.models import Sach, NguoiMuon, TheMuon, TheMuon_Sach



class SignUpRoute(APIView):
    def post(self, request):
        try:
            user = NguoiMuon.objects.raw("SELECT * FROM thuvien_nguoimuon WHERE masv=%s, [request.data['masv']]")[0]#ktra masv da ton tai chua
            return Response({'error': {}, 'message': 'Mã sinh viên đã tồn tại'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            request.data['token'] = createToken()
            serialier = NguoiMuonSerializer(data=request.data)
            if serialier.is_valid():
                serialier.save()
                return Response({'data': serialier.data, 'message': 'Tạo tài khoản thành công'}, status=status.HTTP_200_OK)
            return Response({'error': serialier.errors, 'message': 'Thông tin không đúng định dạng'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginRoute(APIView):
    def post(self, request):
        try:
            user = NguoiMuon.objects.raw("SELECT * FROM thuvien_nguoimuon WHERE masv=%s and matkhau= %s", [request.data['masv'],request.data['matkhau']])[0] #select * from nguoimuon where masv = request.data['masv'] and matkhau = request.data['matkhau']
            user.token = createToken()
            user.save()
            response = Response({"data": { 'token': user.token }, "message": "Đăng nhập thành công"}, status=status.HTTP_200_OK)
            response.set_cookie('token', user.token)
            return response
        except:
            return Response({"error": {}, "message": "Thông tin không chính xác"}, status=status.HTTP_401_UNAUTHORIZED)


class SachRoute(APIView):
    def get(self, request):
        sachs = Sach.objects.raw("SELECT * FROM thuvien_sach") 
        sachData = SachSerializer(sachs, many=True).data
        return Response(data=sachData, status=status.HTTP_200_OK)


class SachByIdRoute(APIView):
    def get(self, request, id):
        try:
            sach = Sach.objects.raw("SELECT * FROM thuvien_sach WHERE maSach = %s", [id])[0] 
            sachData = SachSerializer(sach).data
            return Response(data=sachData, status=status.HTTP_200_OK)
        except:
            return Response(data={'message': 'Sách không tồn tại'}, status=status.HTTP_404_NOT_FOUND)


class TheMuonRoute(APIView):
    def get(self, request):#lay tat ca the muon
        if auth(request.COOKIES.get('token')):
            ngMuon = NguoiMuon.objects.raw('SELECT * FROM thuvien_nguoimuon WHERE token = %s', [request.COOKIES['token']])
            themuons = TheMuon.objects.raw('SELECT * FROM thuvien_themuon WHERE nguoiMuon_id = %s', [ngMuon[0].masv])
            themuonData = TheMuonSerializer(themuons, many=True).data
            for t in themuonData:
                sachs = Sach.objects.raw(" SELECT * FROM thuvien_sach WHERE maSach IN (SELECT sach_id FROM thuvien_themuon_sach WHERE themuon_id =%s)",[t['maThe']])# lay cac cuon sach trong the muon
                print(len(sachs))
                SachData = SachSerializer(sachs, many=True).data
                t['sach'] = SachData
                for s in t['sach']:
                    s['soLuong'] = TheMuon_Sach.objects.raw("SELECT * FROM thuvien_themuon_sach WHERE sach_id = %s and themuon_id = %s", [s['maSach'], t['maThe']])[0].soLuong        
            return Response(data=themuonData, status=status.HTTP_200_OK)
        return Response(data={'message': 'Bạn phải đăng nhập trước khi xem thông tin mượn sách'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if auth(request.COOKIES.get('token')):
            request.data['nguoiMuon'] = NguoiMuon.objects.raw("SELECT * FROM thuvien_nguoimuon WHERE token = %s", [request.COOKIES['token']])[0].masv
            serializer = TheMuonSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(data=serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            serializer.save()
            if 'sach' not in request.data or len(request.data['sach']) == 0:
                return Response(data={'message': 'Bạn phải chọn ít nhất 1 sách', 'success': False}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            added_sachs = []
            for s in request.data['sach']:
                try:
                    sach = Sach.objects.raw("SELECT * FROM thuvien_sach WHERE maSach=%s",[s['maSach']])[0]
                    if sach.soLuong - int(s['soLuong']) < 0:
                        TheMuon.objects.raw("DELETE FROM thuvien_themuon WHERE maThe=%s", [serializer.data['maThe']])
                        for addedSach in added_sachs:
                            temp = Sach.objects.raw("SELECT * FROM thuvien_sach WHERE maSach=%s",[addedSach['maSach']])[0]
                            temp.soLuong += int(addedSach['soLuong'])
                            temp.save()
                        return Response(data={'message': 'Sách ' + sach.tenSach + ' không đủ số lượng. Chỉ còn ' + str(sach.soLuong) + ' cuốn', 'success': False}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                    connection.cursor().execute("INSERT INTO thuvien_themuon_sach (themuon_id, sach_id, soLuong) VALUES (%s, %s, %s)", [serializer.data['maThe'],s['maSach'], s['soLuong']])
                    sach.soLuong -= int(s['soLuong'])
                    sach.save()
                    added_sachs.append(s)
                    print(added_sachs)
                except:
                    TheMuon.objects.raw("DELETE FROM thuvien_themuon WHERE maThe=%s", [serializer.data['maThe']])
                    for addedSach in added_sachs:
                        temp = Sach.objects.raw("SELECT * FROM thuvien_sach WHERE maSach=%s",[addedSach['maSach']])[0]
                        temp.soLuong += addedSach['soLuong']
                        temp.save()
                    return Response(data={'message': 'Sách ' + s['maSach'] + ' không tồn tại', 'success': False}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            return Response(data={'message': 'Bạn đã mượn sách thành công', 'success': True}, status=status.HTTP_200_OK)
        return Response(data={'message': 'Bạn phải đăng nhập trước khi mượn sách', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)


class NguoiMuonRoute(APIView):
    def get(self, request):
        user = auth(request.COOKIES.get('token'))
        if user != None:
            nguoimuons = NguoiMuon.objects.raw("SELECT * FROM thuvien_nguoimuon WHERE token = %s", [request.COOKIES['token']])
            nguoimuonData = NguoiMuonSerializer(nguoimuons).data
            del nguoimuonData['token']
            del nguoimuonData['matkhau']
            return Response(data=nguoimuonData, status=status.HTTP_200_OK)
        return Response(data={'message': 'Bạn phải đăng nhập trước khi xem thông tin', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        user = auth(request.COOKIES.get('token'))
        if user != None:
            nguoimuons = NguoiMuon.objects.raw("SELECT * FROM thuvien_nguoimuon WHERE token = %s", [request.COOKIES['token']])[0]
            serializer = NguoiMuonSerializer(nguoimuons, data=request.data)
            if not serializer.is_valid():
                return Response(data={'errors': serializer.errors, 'message': 'Thông tin không đúng định dạng', 'success': False}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            serializer.save()
            return Response(data={'message': 'Cập nhật thông tin thành công', 'success': True}, status=status.HTTP_200_OK)
        return Response(data={'message': 'Bạn phải đăng nhập trước khi cập nhật thông tin', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

