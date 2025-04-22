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
        if not request.user.has_perm('apps.investment.can_update_transaction_status'):
            return Response({
                'success': False,
                'error': 'You do not have permission to update transaction status'
            }, status=status.HTTP_403_FORBIDDEN)

        saving_id = request.data.get('id')
        new_status = request.data.get('status')
        remarks = request.data.get('remarks', '')  # Get remarks if provided

        try:
            saving = DailySaving.objects.get(id=saving_id)
            # Get existing history or initialize new
            history = saving.history or []
            if isinstance(history, str):
                history = json.loads(history)

            # Build history entry
            history_entry = {
                'old_status': saving.status,
                'new_status': new_status,
                'changed_at': timezone.now().isoformat(),
                'changed_by': request.user.username if request.user.is_authenticated else 'system'
            }

            # Add remarks to history if present
            if new_status == 'rejected' and remarks:
                history_entry['remarks'] = remarks
                # Save remarks to the model if it has a remarks field
                if hasattr(saving, 'remarks'):
                    saving.remarks = remarks

            # Add new history entry
            history.append(history_entry)

            # Update status and history
            saving.status = new_status
            saving.history = history
            saving.save()

            response_data = {
                'success': True,
                'new_status': new_status,
                'history': history
            }

            # Include remarks in response if present
            if new_status == 'rejected' and remarks:
                response_data['remarks'] = remarks

            return Response(response_data, status=status.HTTP_200_OK)

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

    def delete(self, request):
        if not request.user.has_perm('apps.investment.delete_dailysaving'):
            return Response({
                'success': False,
                'error': 'You do not have permission to update transaction status'
            }, status=status.HTTP_403_FORBIDDEN)

        transaction_id = request.data.get('id')

        try:
            transaction = DailySaving.objects.get(id=transaction_id)

            # Only allow deletion if status is pending
            if transaction.status != DailySaving.StatusChoices.PENDING:
                return Response({
                    'success': False,
                    'error': 'Only pending transactions can be deleted'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Delete the transaction
            transaction.delete()

            return Response({
                'success': True,
                'message': 'Transaction deleted successfully'
            }, status=status.HTTP_200_OK)

        except DailySaving.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Transaction record not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
