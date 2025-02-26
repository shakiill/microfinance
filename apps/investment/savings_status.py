# views.py
import json

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.loan.views import IsStaffAndAuthenticated
from apps.helpers.utils import CsrfExemptSessionAuthentication
from apps.investment.models import DailySaving


class ChangeSavingStatus(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]  # Disable CSRF check
    permission_classes = [IsStaffAndAuthenticated]  # Ensure user is authenticated

    def post(self, request):
        saving_id = request.data.get('id')
        new_status = request.data.get('status')

        try:
            saving = DailySaving.objects.get(id=saving_id)
            # Get existing history or initialize new
            history = saving.history or []
            if isinstance(history, str):
                history = json.loads(history)

            # Add new history entry
            history.append({
                'old_status': saving.status,
                'new_status': new_status,
                'changed_at': timezone.now().isoformat(),
                'changed_by': request.user.username if request.user.is_authenticated else 'system'
            })

            # Update status and history
            saving.status = new_status
            saving.history = history
            saving.save()

            return Response({
                'success': True,
                'new_status': new_status,
                'history': history
            }, status=status.HTTP_200_OK)

        except DailySaving.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Saving record not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

#
