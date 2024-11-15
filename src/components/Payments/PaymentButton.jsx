// src/components/Payments/PaymentButton.jsx
import React from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';

const PaymentButton = () => {
  const token = useSelector((state) => state.auth.token);

  const loadRazorpayScript = (src) => {
    return new Promise((resolve) => {
      const script = document.createElement('script');
      script.src = src;
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.body.appendChild(script);
    });
  };

  const handlePayment = async () => {
    const res = await loadRazorpayScript(
      'https://checkout.razorpay.com/v1/checkout.js'
    );

    if (!res) {
      alert('Razorpay SDK failed to load. Are you online?');
      return;
    }

    // Create order on the backend
    const order = await axios.post(
      'http://localhost:8000/payments/create-order',
      {
        amount: 500, // Amount in INR (e.g., 500 INR)
        currency: 'INR',
        receipt: 'receipt#1',
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const options = {
      key: 'YOUR_RAZORPAY_KEY_ID', // Replace with your Razorpay Key ID
      amount: order.data.amount.toString(),
      currency: order.data.currency,
      name: 'Signature Extractor App',
      description: 'Subscription Payment',
      order_id: order.data.id,
      handler: async (response) => {
        // Verify payment on the backend
        try {
          const verification = await axios.post(
            'http://localhost:8000/payments/verify-payment',
            {
              payment_id: response.razorpay_payment_id,
              order_id: response.razorpay_order_id,
              signature: response.razorpay_signature,
            },
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          if (verification.data.status === 'captured') {
            alert('Payment Successful!');
            // Optionally, update user subscription status in the frontend
          } else {
            alert('Payment Verification Failed!');
          }
        } catch (error) {
          alert('Payment Verification Failed!');
        }
      },
      prefill: {
        name: 'User Name', // Replace with actual user name
        email: 'user@example.com', // Replace with actual user email
        contact: '9999999999', // Replace with actual user contact
      },
      notes: {
        address: 'Signature Extractor App Office',
      },
      theme: {
        color: '#1E3A8A',
      },
    };

    const paymentObject = new window.Razorpay(options);
    paymentObject.open();
  };

  return (
    <button
      onClick={handlePayment}
      className="bg-secondary text-white px-4 py-2 rounded hover:bg-primary"
    >
      Subscribe Now
    </button>
  );
};

export default PaymentButton;
