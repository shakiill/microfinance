import json

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.loan.views import IsStaffAndAuthenticated
from apps.helpers.utils import CsrfExemptSessionAuthentication
from .models import Transaction  # Import the Transaction model


class ChangeTransactionStatus(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]  # Disable CSRF check
    permission_classes = [IsStaffAndAuthenticated]  # Ensure user is authenticated

    def post(self, request):
        transaction_id = request.data.get('id')
        new_status = request.data.get('status')
        remarks = request.data.get('remarks', '')  # Get remarks if provided

        try:
            transaction = Transaction.objects.get(id=transaction_id)
            # Get existing history or initialize new
            history = transaction.history or []
            if isinstance(history, str):
                history = json.loads(history)

            # Build history entry
            history_entry = {
                'old_status': transaction.status,
                'new_status': new_status,
                'changed_at': timezone.now().isoformat(),
                'changed_by': request.user.username if request.user.is_authenticated else 'system'
            }

            # Add remarks to history if present
            if new_status == 'rejected' and remarks:
                history_entry['remarks'] = remarks
                # Save remarks to the model
                transaction.remarks = remarks

            # Handle verification if status is changing to verified
            if new_status == Transaction.StatusChoices.VERIFIED:
                transaction.verified_by = request.user
                transaction.verified_at = timezone.now()

            # Add new history entry
            history.append(history_entry)

            # Update status and history
            transaction.status = new_status
            transaction.history = history
            transaction.save()

            response_data = {
                'success': True,
                'new_status': new_status,
                'history': history
            }

            # Include remarks in response if present
            if remarks:
                response_data['remarks'] = remarks

            return Response(response_data, status=status.HTTP_200_OK)

        except Transaction.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Transaction record not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        transaction_id = request.data.get('id')

        try:
            transaction = Transaction.objects.get(id=transaction_id)

            # Only allow deletion if status is pending
            if transaction.status != Transaction.StatusChoices.PENDING:
                return Response({
                    'success': False,
                    'error': 'Only pending transactions can be deleted'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Store the installment before deleting the transaction
            installment = transaction.installment
            transaction_amount = transaction.amount

            # Delete the transaction
            transaction.delete()

            # Update the installment's paid amount
            installment.paid_amount -= transaction_amount
            installment.save()

            return Response({
                'success': True,
                'message': 'Transaction deleted successfully'
            }, status=status.HTTP_200_OK)

        except Transaction.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Transaction record not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
