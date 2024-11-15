// // // // // // // src/store/slices/authSlice.js
// // // // // // import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// // // // // // import axios from 'axios';

// // // // // // // Async thunk for user login
// // // // // // export const loginUser = createAsyncThunk(
// // // // // //     'auth/loginUser',
// // // // // //     async (credentials, { rejectWithValue }) => {
// // // // // //         try {
// // // // // //             const response = await axios.post('http://localhost:8000/auth/login', credentials);
// // // // // //             return response.data;
// // // // // //         } catch (error) {
// // // // // //             return rejectWithValue(error.response.data);
// // // // // //         }
// // // // // //     }
// // // // // // );

// // // // // // // Async thunk for user registration
// // // // // // export const registerUser = createAsyncThunk(
// // // // // //     'auth/registerUser',
// // // // // //     async (userData, { rejectWithValue }) => {
// // // // // //         try {
// // // // // //             const response = await axios.post('http://localhost:8000/auth/register', userData);
// // // // // //             return response.data;
// // // // // //         } catch (error) {
// // // // // //             return rejectWithValue(error.response.data);
// // // // // //         }
// // // // // //     }
// // // // // // );

// // // // // // const authSlice = createSlice({
// // // // // //     name: 'auth',
// // // // // //     initialState: {
// // // // // //         user: null,
// // // // // //         token: localStorage.getItem('token') || null,
// // // // // //         loading: false,
// // // // // //         error: null,
// // // // // //         isAuthenticated: !!localStorage.getItem('token'),
// // // // // //     },
// // // // // //     reducers: {
// // // // // //         logout: (state) => {
// // // // // //             state.user = null;
// // // // // //             state.token = null;
// // // // // //             state.isAuthenticated = false;
// // // // // //             localStorage.removeItem('token');
// // // // // //         },
// // // // // //     },
// // // // // //     extraReducers: (builder) => {
// // // // // //         builder
// // // // // //             // Login
// // // // // //             .addCase(loginUser.pending, (state) => {
// // // // // //                 state.loading = true;
// // // // // //                 state.error = null;
// // // // // //             })
// // // // // //             .addCase(loginUser.fulfilled, (state, action) => {
// // // // // //                 state.loading = false;
// // // // // //                 state.token = action.payload.token;
// // // // // //                 state.isAuthenticated = true;
// // // // // //                 localStorage.setItem('token', action.payload.token);
// // // // // //             })
// // // // // //             .addCase(loginUser.rejected, (state, action) => {
// // // // // //                 state.loading = false;
// // // // // //                 state.error = action.payload.message || 'Login failed';
// // // // // //             })
// // // // // //             // Register
// // // // // //             .addCase(registerUser.pending, (state) => {
// // // // // //                 state.loading = true;
// // // // // //                 state.error = null;
// // // // // //             })
// // // // // //             .addCase(registerUser.fulfilled, (state, action) => {
// // // // // //                 state.loading = false;
// // // // // //                 state.token = action.payload.token;
// // // // // //                 state.isAuthenticated = true;
// // // // // //                 localStorage.setItem('token', action.payload.token);
// // // // // //             })
// // // // // //             .addCase(registerUser.rejected, (state, action) => {
// // // // // //                 state.loading = false;
// // // // // //                 state.error = action.payload.message || 'Registration failed';
// // // // // //             });
// // // // // //     },
// // // // // // });

// // // // // // export const { logout } = authSlice.actions;
// // // // // // export default authSlice.reducer;


// // // // // // import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// // // // // // import axiosInstance from '../../utils/axiosInstance';

// // // // // // // Define and export async thunks only once
// // // // // // export const registerUser = createAsyncThunk(
// // // // // //     'auth/registerUser',
// // // // // //     async (userData, { rejectWithValue }) => {
// // // // // //         try {
// // // // // //             const response = await axiosInstance.post('/auth/register', userData);
// // // // // //             return response.data;
// // // // // //         } catch (error) {
// // // // // //             return rejectWithValue(error.response?.data || { message: "Registration failed" });
// // // // // //         }
// // // // // //     }
// // // // // // );

// // // // // // export const loginUser = createAsyncThunk(
// // // // // //     'auth/loginUser',
// // // // // //     async (credentials, { rejectWithValue }) => {
// // // // // //         try {
// // // // // //             const response = await axiosInstance.post('/auth/login', credentials);
// // // // // //             return response.data;
// // // // // //         } catch (error) {
// // // // // //             return rejectWithValue(error.response?.data || { message: "Login failed" });
// // // // // //         }
// // // // // //     }
// // // // // // );

// // // // // // const authSlice = createSlice({
// // // // // //     name: 'auth',
// // // // // //     initialState: {
// // // // // //         token: localStorage.getItem('token') || null,
// // // // // //         isAuthenticated: !!localStorage.getItem('token'),
// // // // // //         loading: false,
// // // // // //         error: null,
// // // // // //     },
// // // // // //     reducers: {
// // // // // //         logout: (state) => {
// // // // // //             state.token = null;
// // // // // //             state.isAuthenticated = false;
// // // // // //             localStorage.removeItem('token');
// // // // // //         },
// // // // // //         clearError: (state) => {
// // // // // //             state.error = null;
// // // // // //         },
// // // // // //     },
// // // // // //     extraReducers: (builder) => {
// // // // // //         builder
// // // // // //             .addCase(registerUser.pending, (state) => {
// // // // // //                 state.loading = true;
// // // // // //                 state.error = null;
// // // // // //             })
// // // // // //             .addCase(registerUser.fulfilled, (state, action) => {
// // // // // //                 state.loading = false;
// // // // // //                 state.token = action.payload.access_token;
// // // // // //                 state.isAuthenticated = true;
// // // // // //                 localStorage.setItem('token', action.payload.access_token);
// // // // // //             })
// // // // // //             .addCase(registerUser.rejected, (state, action) => {
// // // // // //                 state.loading = false;
// // // // // //                 state.error = action.payload.message || 'Registration failed';
// // // // // //             })
// // // // // //             .addCase(loginUser.pending, (state) => {
// // // // // //                 state.loading = true;
// // // // // //                 state.error = null;
// // // // // //             })
// // // // // //             .addCase(loginUser.fulfilled, (state, action) => {
// // // // // //                 state.loading = false;
// // // // // //                 state.token = action.payload.access_token;
// // // // // //                 state.isAuthenticated = true;
// // // // // //                 localStorage.setItem('token', action.payload.access_token);
// // // // // //             })
// // // // // //             .addCase(loginUser.rejected, (state, action) => {
// // // // // //                 state.loading = false;
// // // // // //                 state.error = action.payload.message || 'Login failed';
// // // // // //             });
// // // // // //     },
// // // // // // });

// // // // // // // Export the slice's actions and reducer correctly
// // // // // // export const { logout, clearError } = authSlice.actions;
// // // // // // export default authSlice.reducer;

// // // // // import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// // // // // import axiosInstance from '../../utils/axiosInstance';

// // // // // export const registerUser = createAsyncThunk(
// // // // //     'auth/registerUser',
// // // // //     async (userData, { rejectWithValue }) => {
// // // // //         try {
// // // // //             const response = await axiosInstance.post('/auth/register', userData);
// // // // //             return response.data;
// // // // //         } catch (error) {
// // // // //             if (!error.response) {
// // // // //                 return rejectWithValue({
// // // // //                     message: 'Network error - please check your connection'
// // // // //                 });
// // // // //             }
// // // // //             return rejectWithValue(
// // // // //                 error.response?.data || { message: "Registration failed" }
// // // // //             );
// // // // //         }
// // // // //     }
// // // // // );

// // // // // export const loginUser = createAsyncThunk(
// // // // //     'auth/loginUser',
// // // // //     async (credentials, { rejectWithValue }) => {
// // // // //         try {
// // // // //             const response = await axiosInstance.post('/auth/login', credentials);
// // // // //             return response.data;
// // // // //         } catch (error) {
// // // // //             if (!error.response) {
// // // // //                 return rejectWithValue({
// // // // //                     message: 'Network error - please check your connection'
// // // // //                 });
// // // // //             }
// // // // //             return rejectWithValue(
// // // // //                 error.response?.data || { message: "Login failed" }
// // // // //             );
// // // // //         }
// // // // //     }
// // // // // );

// // // // // const authSlice = createSlice({
// // // // //     name: 'auth',
// // // // //     initialState: {
// // // // //         user: null,
// // // // //         token: localStorage.getItem('token') || null,
// // // // //         isAuthenticated: !!localStorage.getItem('token'),
// // // // //         loading: false,
// // // // //         error: null,
// // // // //     },
// // // // //     reducers: {
// // // // //         logout: (state) => {
// // // // //             state.user = null;
// // // // //             state.token = null;
// // // // //             state.isAuthenticated = false;
// // // // //             localStorage.removeItem('token');
// // // // //         },
// // // // //         clearError: (state) => {
// // // // //             state.error = null;
// // // // //         },
// // // // //     },
// // // // //     extraReducers: (builder) => {
// // // // //         builder
// // // // //             // Register cases
// // // // //             .addCase(registerUser.pending, (state) => {
// // // // //                 state.loading = true;
// // // // //                 state.error = null;
// // // // //             })
// // // // //             .addCase(registerUser.fulfilled, (state, action) => {
// // // // //                 state.loading = false;
// // // // //                 state.user = action.payload;
// // // // //                 // Don't set token on register - user should login
// // // // //             })
// // // // //             .addCase(registerUser.rejected, (state, action) => {
// // // // //                 state.loading = false;
// // // // //                 state.error = action.payload?.detail || action.payload?.message || 'Registration failed';
// // // // //             })
// // // // //             // Login cases
// // // // //             .addCase(loginUser.pending, (state) => {
// // // // //                 state.loading = true;
// // // // //                 state.error = null;
// // // // //             })
// // // // //             .addCase(loginUser.fulfilled, (state, action) => {
// // // // //                 state.loading = false;
// // // // //                 state.token = action.payload.access_token;
// // // // //                 state.isAuthenticated = true;
// // // // //                 localStorage.setItem('token', action.payload.access_token);
// // // // //             })
// // // // //             .addCase(loginUser.rejected, (state, action) => {
// // // // //                 state.loading = false;
// // // // //                 state.error = action.payload?.detail || action.payload?.message || 'Login failed';
// // // // //             });
// // // // //     },
// // // // // });

// // // // // export const { logout, clearError } = authSlice.actions;
// // // // // export default authSlice.reducer;

// // // // import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// // // // import axiosInstance from '../../utils/axiosInstance';

// // // // export const registerUser = createAsyncThunk(
// // // //     'auth/registerUser',
// // // //     async (userData, { rejectWithValue }) => {
// // // //         try {
// // // //             const response = await axiosInstance.post('/auth/register', userData);
// // // //             return response.data;
// // // //         } catch (error) {
// // // //             if (!error.response) {
// // // //                 return rejectWithValue({
// // // //                     message: 'Network error - please check your connection'
// // // //                 });
// // // //             }
// // // //             return rejectWithValue(
// // // //                 error.response?.data || { message: "Registration failed" }
// // // //             );
// // // //         }
// // // //     }
// // // // );

// // // // export const loginUser = createAsyncThunk(
// // // //     'auth/loginUser',
// // // //     async (credentials, { rejectWithValue }) => {
// // // //         try {
// // // //             const response = await axiosInstance.post('/auth/login', credentials);
// // // //             return response.data;
// // // //         } catch (error) {
// // // //             if (!error.response) {
// // // //                 return rejectWithValue({
// // // //                     message: 'Network error - please check your connection'
// // // //                 });
// // // //             }
// // // //             return rejectWithValue(
// // // //                 error.response?.data || { message: "Login failed" }
// // // //             );
// // // //         }
// // // //     }
// // // // );

// // // // const authSlice = createSlice({
// // // //     name: 'auth',
// // // //     initialState: {
// // // //         user: null,
// // // //         token: localStorage.getItem('token') || null,
// // // //         isAuthenticated: !!localStorage.getItem('token'),
// // // //         loading: false,
// // // //         error: null,
// // // //     },
// // // //     reducers: {
// // // //         logout: (state) => {
// // // //             state.user = null;
// // // //             state.token = null;
// // // //             state.isAuthenticated = false;
// // // //             localStorage.removeItem('token');
// // // //         },
// // // //         clearError: (state) => {
// // // //             state.error = null;
// // // //         },
// // // //     },
// // // //     extraReducers: (builder) => {
// // // //         builder
// // // //             // Register cases
// // // //             .addCase(registerUser.pending, (state) => {
// // // //                 state.loading = true;
// // // //                 state.error = null;
// // // //             })
// // // //             .addCase(registerUser.fulfilled, (state, action) => {
// // // //                 state.loading = false;
// // // //                 state.user = action.payload;
// // // //                 // Don't set token on register - user should login
// // // //             })
// // // //             .addCase(registerUser.rejected, (state, action) => {
// // // //                 state.loading = false;
// // // //                 state.error = action.payload?.detail || action.payload?.message || 'Registration failed';
// // // //             })
// // // //             // Login cases
// // // //             .addCase(loginUser.pending, (state) => {
// // // //                 state.loading = true;
// // // //                 state.error = null;
// // // //             })
// // // //             .addCase(loginUser.fulfilled, (state, action) => {
// // // //                 state.loading = false;
// // // //                 state.token = action.payload.access_token;
// // // //                 state.isAuthenticated = true;
// // // //                 localStorage.setItem('token', action.payload.access_token);
// // // //             })
// // // //             .addCase(loginUser.rejected, (state, action) => {
// // // //                 state.loading = false;
// // // //                 state.error = action.payload?.detail || action.payload?.message || 'Login failed';
// // // //             });
// // // //     },
// // // // });

// // // // export const { logout, clearError } = authSlice.actions;
// // // // export default authSlice.reducer;

// // // import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// // // import axiosInstance from '../../utils/axiosInstance';

// // // export const loginUser = createAsyncThunk(
// // //     'auth/loginUser',
// // //     async (formData, { rejectWithValue }) => {
// // //         try {
// // //             // Set the correct content type for form data
// // //             const config = {
// // //                 headers: {
// // //                     'Content-Type': 'application/x-www-form-urlencoded'
// // //                 }
// // //             };

// // //             // Convert FormData to URLSearchParams
// // //             const params = new URLSearchParams();
// // //             if (formData instanceof FormData) {
// // //                 for (let [key, value] of formData.entries()) {
// // //                     params.append(key, value);
// // //                 }
// // //             } else {
// // //                 // If it's already URLSearchParams, use it directly
// // //                 for (let [key, value] of Object.entries(formData)) {
// // //                     params.append(key, value);
// // //                 }
// // //             }

// // //             const response = await axiosInstance.post('/auth/login', params, config);
// // //             return response.data;
// // //         } catch (error) {
// // //             console.error('Login error details:', error.response?.data);

// // //             if (error.response?.data?.detail) {
// // //                 return rejectWithValue(error.response.data);
// // //             }

// // //             return rejectWithValue({
// // //                 detail: error.message || 'Login failed'
// // //             });
// // //         }
// // //     }
// // // );

// // // const authSlice = createSlice({
// // //     name: 'auth',
// // //     initialState: {
// // //         token: localStorage.getItem('token') || null,
// // //         isAuthenticated: !!localStorage.getItem('token'),
// // //         loading: false,
// // //         error: null,
// // //     },
// // //     reducers: {
// // //         logout: (state) => {
// // //             state.token = null;
// // //             state.isAuthenticated = false;
// // //             localStorage.removeItem('token');
// // //         },
// // //         clearError: (state) => {
// // //             state.error = null;
// // //         },
// // //     },
// // //     extraReducers: (builder) => {
// // //         builder
// // //             .addCase(loginUser.pending, (state) => {
// // //                 state.loading = true;
// // //                 state.error = null;
// // //             })
// // //             .addCase(loginUser.fulfilled, (state, action) => {
// // //                 state.loading = false;
// // //                 state.token = action.payload.access_token;
// // //                 state.isAuthenticated = true;
// // //                 localStorage.setItem('token', action.payload.access_token);
// // //             })
// // //             .addCase(loginUser.rejected, (state, action) => {
// // //                 state.loading = false;
// // //                 state.error = action.payload || { detail: 'Login failed' };
// // //             });
// // //     },
// // // });

// // // export const { logout, clearError } = authSlice.actions;
// // // export default authSlice.reducer;

// // import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// // import axiosInstance from '../../utils/axiosInstance';

// // // Register thunk
// // export const registerUser = createAsyncThunk(
// //     'auth/registerUser',
// //     async (userData, { rejectWithValue }) => {
// //         try {
// //             const response = await axiosInstance.post('/auth/register', userData);
// //             return response.data;
// //         } catch (error) {
// //             console.error('Registration error details:', error.response?.data);

// //             if (error.response?.data?.detail) {
// //                 return rejectWithValue(error.response.data);
// //             }

// //             return rejectWithValue({
// //                 detail: error.message || 'Registration failed'
// //             });
// //         }
// //     }
// // );

// // // Login thunk
// // export const loginUser = createAsyncThunk(
// //     'auth/loginUser',
// //     async (formData, { rejectWithValue }) => {
// //         try {
// //             const config = {
// //                 headers: {
// //                     'Content-Type': 'application/x-www-form-urlencoded'
// //                 }
// //             };

// //             const params = new URLSearchParams();
// //             if (formData instanceof FormData) {
// //                 for (let [key, value] of formData.entries()) {
// //                     params.append(key, value);
// //                 }
// //             } else {
// //                 for (let [key, value] of Object.entries(formData)) {
// //                     params.append(key, value);
// //                 }
// //             }

// //             const response = await axiosInstance.post('/auth/login', params, config);
// //             return response.data;
// //         } catch (error) {
// //             console.error('Login error details:', error.response?.data);

// //             if (error.response?.data?.detail) {
// //                 return rejectWithValue(error.response.data);
// //             }

// //             return rejectWithValue({
// //                 detail: error.message || 'Login failed'
// //             });
// //         }
// //     }
// // );

// // const authSlice = createSlice({
// //     name: 'auth',
// //     initialState: {
// //         user: null,
// //         token: localStorage.getItem('token') || null,
// //         isAuthenticated: !!localStorage.getItem('token'),
// //         loading: false,
// //         error: null,
// //     },
// //     reducers: {
// //         logout: (state) => {
// //             state.user = null;
// //             state.token = null;
// //             state.isAuthenticated = false;
// //             localStorage.removeItem('token');
// //         },
// //         clearError: (state) => {
// //             state.error = null;
// //         },
// //     },
// //     extraReducers: (builder) => {
// //         builder
// //             // Register cases
// //             .addCase(registerUser.pending, (state) => {
// //                 state.loading = true;
// //                 state.error = null;
// //             })
// //             .addCase(registerUser.fulfilled, (state, action) => {
// //                 state.loading = false;
// //                 state.user = action.payload;
// //             })
// //             .addCase(registerUser.rejected, (state, action) => {
// //                 state.loading = false;
// //                 state.error = action.payload?.detail || 'Registration failed';
// //             })
// //             // Login cases
// //             .addCase(loginUser.pending, (state) => {
// //                 state.loading = true;
// //                 state.error = null;
// //             })
// //             .addCase(loginUser.fulfilled, (state, action) => {
// //                 state.loading = false;
// //                 state.token = action.payload.access_token;
// //                 state.isAuthenticated = true;
// //                 localStorage.setItem('token', action.payload.access_token);
// //             })
// //             .addCase(loginUser.rejected, (state, action) => {
// //                 state.loading = false;
// //                 state.error = action.payload?.detail || 'Login failed';
// //             });
// //     },
// // });

// // export const { logout, clearError } = authSlice.actions;
// // export default authSlice.reducer;

// import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// import axiosInstance from '../../utils/axiosInstance';

// export const loginUser = createAsyncThunk(
//     'auth/loginUser',
//     async ({ email, password }, { rejectWithValue }) => {
//         try {
//             // Create form data in the exact format FastAPI expects
//             const formData = new URLSearchParams();
//             formData.append('username', email);  // FastAPI OAuth2 expects 'username'
//             formData.append('password', password);

//             const response = await axiosInstance.post('/auth/login', formData, {
//                 headers: {
//                     'Content-Type': 'application/x-www-form-urlencoded',
//                 }
//             });
//             return response.data;
//         } catch (error) {
//             console.error('Login error details:', error.response?.data);
//             return rejectWithValue(error.response?.data || { detail: 'Login failed' });
//         }
//     }
// );

// export const registerUser = createAsyncThunk(
//     'auth/registerUser',
//     async ({ email, password }, { rejectWithValue }) => {
//         try {
//             const response = await axiosInstance.post('/auth/register', {
//                 email,
//                 password
//             });
//             return response.data;
//         } catch (error) {
//             console.error('Registration error details:', error.response?.data);
//             return rejectWithValue(error.response?.data || { detail: 'Registration failed' });
//         }
//     }
// );

// const authSlice = createSlice({
//     name: 'auth',
//     initialState: {
//         user: null,
//         token: localStorage.getItem('token') || null,
//         isAuthenticated: !!localStorage.getItem('token'),
//         loading: false,
//         error: null,
//     },
//     reducers: {
//         logout: (state) => {
//             state.user = null;
//             state.token = null;
//             state.isAuthenticated = false;
//             localStorage.removeItem('token');
//         },
//         clearError: (state) => {
//             state.error = null;
//         },
//     },
//     extraReducers: (builder) => {
//         builder
//             .addCase(loginUser.pending, (state) => {
//                 state.loading = true;
//                 state.error = null;
//             })
//             .addCase(loginUser.fulfilled, (state, action) => {
//                 state.loading = false;
//                 state.token = action.payload.access_token;
//                 state.isAuthenticated = true;
//                 localStorage.setItem('token', action.payload.access_token);
//             })
//             .addCase(loginUser.rejected, (state, action) => {
//                 state.loading = false;
//                 if (Array.isArray(action.payload?.detail)) {
//                     state.error = action.payload.detail.map(err => err.msg).join(', ');
//                 } else {
//                     state.error = action.payload?.detail || 'Login failed';
//                 }
//             })
//             .addCase(registerUser.pending, (state) => {
//                 state.loading = true;
//                 state.error = null;
//             })
//             .addCase(registerUser.fulfilled, (state, action) => {
//                 state.loading = false;
//                 state.user = action.payload;
//             })
//             .addCase(registerUser.rejected, (state, action) => {
//                 state.loading = false;
//                 if (Array.isArray(action.payload?.detail)) {
//                     state.error = action.payload.detail.map(err => err.msg).join(', ');
//                 } else {
//                     state.error = action.payload?.detail || 'Registration failed';
//                 }
//             });
//     },
// });

// export const { logout, clearError } = authSlice.actions;
// export default authSlice.reducer;


import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../utils/axiosInstance';

export const loginUser = createAsyncThunk(
    'auth/loginUser',
    async ({ email, password }, { rejectWithValue }) => {
        try {
            const data = new URLSearchParams();
            data.append('username', email);
            data.append('password', password);

            const response = await axiosInstance.post('/auth/login', data, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });
            return response.data;
        } catch (error) {
            console.error('Login error details:', error.response?.data);
            if (error.response?.data?.detail) {
                return rejectWithValue(error.response.data);
            }
            return rejectWithValue({ detail: 'Login failed' });
        }
    }
);

export const registerUser = createAsyncThunk(
    'auth/registerUser',
    async ({ email, password }, { rejectWithValue }) => {
        try {
            const response = await axiosInstance.post('/auth/register', {
                email,
                password
            });
            return response.data;
        } catch (error) {
            console.error('Registration error details:', error.response?.data);
            if (error.response?.data?.detail) {
                return rejectWithValue(error.response.data);
            }
            return rejectWithValue({ detail: 'Registration failed' });
        }
    }
);

const authSlice = createSlice({
    name: 'auth',
    initialState: {
        user: null,
        token: localStorage.getItem('token') || null,
        isAuthenticated: !!localStorage.getItem('token'),
        loading: false,
        error: null,
    },
    reducers: {
        logout: (state) => {
            state.user = null;
            state.token = null;
            state.isAuthenticated = false;
            localStorage.removeItem('token');
        },
        clearError: (state) => {
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(loginUser.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(loginUser.fulfilled, (state, action) => {
                state.loading = false;
                state.token = action.payload.access_token;
                state.isAuthenticated = true;
                localStorage.setItem('token', action.payload.access_token);
            })
            .addCase(loginUser.rejected, (state, action) => {
                state.loading = false;
                if (Array.isArray(action.payload?.detail)) {
                    state.error = action.payload.detail.map(err => err.msg).join(', ');
                } else {
                    state.error = action.payload?.detail || 'Login failed';
                }
            })
            .addCase(registerUser.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(registerUser.fulfilled, (state, action) => {
                state.loading = false;
                state.user = action.payload;
            })
            .addCase(registerUser.rejected, (state, action) => {
                state.loading = false;
                if (Array.isArray(action.payload?.detail)) {
                    state.error = action.payload.detail.map(err => err.msg).join(', ');
                } else {
                    state.error = action.payload?.detail || 'Registration failed';
                }
            });
    },
});

export const { logout, clearError } = authSlice.actions;
export default authSlice.reducer;