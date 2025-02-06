from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Payment, Transaction
import razorpay
import logging
from django.db import transaction as db_transaction

# Set up logger for debugging
logger = logging.getLogger(__name__)

@csrf_exempt
def confirm_payment(request):
    if request.method != "POST":
        logger.warning("Invalid request method for confirm_payment view.")
        return redirect('/')

    try:
        # Initialize Razorpay client with keys
        RAZORPAY_KEY_ID = getattr(settings, "RAZORPAY_KEY_ID", None)
        RAZORPAY_KEY_SECRET = getattr(settings, "RAZORPAY_KEY_SECRET", None)

        if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
            logger.error("Razorpay keys are missing in settings.")
            return redirect('payment_failed')  # Redirect to failure page if keys are not set

        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

        # Extract Razorpay payment details from the POST request
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        if not razorpay_order_id or not razorpay_payment_id or not razorpay_signature:
            logger.error("Missing Razorpay payment details in POST data.")
            return redirect('payment_failed')  # Redirect to failure page if details are missing

        # Verify payment signature using Razorpay utility
        verification_data = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        # Log the verification data for debugging
        logger.info(f"Verification Data: {verification_data}")

        client.utility.verify_payment_signature(verification_data)

        # Begin database transaction to ensure atomicity
        with db_transaction.atomic():
            # Get the payment object using the Razorpay order ID
            payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)

            # Update the payment details with Razorpay response data
            payment.razorpay_payment_id = razorpay_payment_id
            payment.payment_signature = razorpay_signature
            payment.status = "COMPLETED"  # Change status to completed
            payment.save()

            # Get the related transaction object
            transaction = get_object_or_404(Transaction, id=payment.transaction.id)

            # Update transaction status
            transaction.status = "COMPLETED"  # Update transaction status (adjust as needed)
            transaction.save()

        # Redirect to the transaction list page after successful payment
        logger.info(f"Payment {payment.id} completed successfully.")
        return redirect('transaction_list')

    except razorpay.errors.SignatureVerificationError as e:
        # Log signature verification error for debugging
        logger.error(f"Razorpay Signature Verification Failed: {e}")
        return redirect('payment_failed')  # Redirect to a failure page

    except Exception as e:
        # Log any other errors for debugging
        logger.error(f"Error in confirm_payment view: {e}")
        return redirect('payment_failed')  # Redirect to a failure page
