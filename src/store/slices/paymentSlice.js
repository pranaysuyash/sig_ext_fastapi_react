// src/store/slices/paymentSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Async thunk to process payment
export const processPayment = createAsyncThunk(
    'payment/processPayment',
    async (paymentData, { rejectWithValue, getState }) => {
        try {
            const { auth } = getState();
            const response = await axios.post('http://localhost:8000/payments/process', paymentData, {
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${auth.token}`,
                },
            });
            return response.data;
        } catch (error) {
            return rejectWithValue(error.response.data);
        }
    }
);

const paymentSlice = createSlice({
    name: 'payment',
    initialState: {
        status: null,
        loading: false,
        error: null,
    },
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(processPayment.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(processPayment.fulfilled, (state, action) => {
                state.loading = false;
                state.status = action.payload.status;
            })
            .addCase(processPayment.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload.message || 'Payment processing failed';
            });
    },
});

export default paymentSlice.reducer;
