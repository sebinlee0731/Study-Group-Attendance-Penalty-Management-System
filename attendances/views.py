from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Attendance
from .serializers import AttendanceSerializer
from .services.attendance_facade import AttendanceFacade


class AttendanceCreateView(generics.CreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = AttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        facade = AttendanceFacade()
        attendance = facade.record(
            validated_data=serializer.validated_data,
            request_user=request.user
        )

        response_serializer = AttendanceSerializer(attendance)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class AttendanceListView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        schedule_id = self.kwargs['schedule_id']

        return Attendance.objects.filter(
            schedule_id=schedule_id
        )