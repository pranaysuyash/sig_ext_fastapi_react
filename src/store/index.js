// // src/store/index.js
// import { configureStore } from '@reduxjs/toolkit';
// import authReducer from './slices/authSlice';
// import extractionReducer from './slices/extractionSlice';
// import paymentReducer from './slices/paymentSlice';

// const store = configureStore({
//     reducer: {
//         auth: authReducer,
//         extraction: extractionReducer,
//         payment: paymentReducer,
//     },
// });

// export default store;

import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import extractionReducer from './slices/extractionSlice';
import paymentReducer from './slices/paymentSlice';

export const store = configureStore({
    reducer: {
        auth: authReducer,
        extraction: extractionReducer,
        payment: paymentReducer,
    },
});