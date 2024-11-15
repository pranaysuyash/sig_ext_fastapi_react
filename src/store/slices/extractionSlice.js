// // // // // // // // import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// // // // // // // // import axios from 'axios';

// // // // // // // // // const uploadImage = createAsyncThunk(
// // // // // // // // //     'extraction/uploadImage',
// // // // // // // // //     async (formData, { rejectWithValue, getState }) => {
// // // // // // // // //         try {
// // // // // // // // //             const { auth } = getState();
// // // // // // // // //             const token = auth.token;

// // // // // // // // //             if (!token) {
// // // // // // // // //                 throw new Error("Missing authentication token");
// // // // // // // // //             }

// // // // // // // // //             // Create axios instance with custom config
// // // // // // // // //             const axiosInstance = axios.create({
// // // // // // // // //                 baseURL: 'http://localhost:8000',
// // // // // // // // //                 timeout: 60000, // Increase timeout to 60 seconds for large files
// // // // // // // // //                 maxContentLength: Infinity,
// // // // // // // // //                 maxBodyLength: Infinity,
// // // // // // // // //             });

// // // // // // // // //             // Log the request details
// // // // // // // // //             const fileInfo = formData.get('file');
// // // // // // // // //             console.log('Preparing upload:', {
// // // // // // // // //                 fileSize: fileInfo ? `${(fileInfo.size / (1024 * 1024)).toFixed(2)} MB` : 'No file',
// // // // // // // // //                 fileType: fileInfo?.type,
// // // // // // // // //                 fileName: fileInfo?.name,
// // // // // // // // //             });

// // // // // // // // //             // Send the upload request
// // // // // // // // //             const response = await axiosInstance.post('/extraction/upload', formData, {
// // // // // // // // //                 headers: {
// // // // // // // // //                     'Content-Type': 'multipart/form-data',
// // // // // // // // //                     Authorization: `Bearer ${token}`,
// // // // // // // // //                 },
// // // // // // // // //                 onUploadProgress: (progressEvent) => {
// // // // // // // // //                     const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
// // // // // // // // //                     console.log(`Upload progress: ${percentCompleted}%`);
// // // // // // // // //                 },
// // // // // // // // //             });

// // // // // // // // //             // Log successful response
// // // // // // // // //             console.log('Upload successful:', {
// // // // // // // // //                 status: response.status,
// // // // // // // // //                 data: response.data,
// // // // // // // // //             });

// // // // // // // // //             return response.data;
// // // // // // // // //         } catch (error) {
// // // // // // // // //             // Log detailed error information
// // // // // // // // //             console.error('Upload error:', {
// // // // // // // // //                 message: error.message,
// // // // // // // // //                 response: {
// // // // // // // // //                     status: error.response?.status,
// // // // // // // // //                     statusText: error.response?.statusText,
// // // // // // // // //                     data: error.response?.data,
// // // // // // // // //                 },
// // // // // // // // //                 request: error.request ? 'Request was made but no response received' : 'Request setup failed',
// // // // // // // // //                 config: {
// // // // // // // // //                     url: error.config?.url,
// // // // // // // // //                     method: error.config?.method,
// // // // // // // // //                     headers: error.config?.headers,
// // // // // // // // //                     timeout: error.config?.timeout,
// // // // // // // // //                 },
// // // // // // // // //             });

// // // // // // // // //             // Determine appropriate error message
// // // // // // // // //             let errorMessage = 'Failed to upload image.';

// // // // // // // // //             if (error.response) {
// // // // // // // // //                 // Server responded with error
// // // // // // // // //                 switch (error.response.status) {
// // // // // // // // //                     case 400:
// // // // // // // // //                         errorMessage = 'Invalid file format or request.';
// // // // // // // // //                         break;
// // // // // // // // //                     case 401:
// // // // // // // // //                         errorMessage = 'Please log in again to upload files.';
// // // // // // // // //                         break;
// // // // // // // // //                     case 413:
// // // // // // // // //                         errorMessage = 'File is too large for the server to process.';
// // // // // // // // //                         break;
// // // // // // // // //                     case 500:
// // // // // // // // //                         errorMessage = 'Server encountered an error while processing the file.';
// // // // // // // // //                         break;
// // // // // // // // //                     default:
// // // // // // // // //                         errorMessage = error.response.data?.message ||
// // // // // // // // //                             `Server error (${error.response.status})`;
// // // // // // // // //                 }
// // // // // // // // //             } else if (error.request) {
// // // // // // // // //                 // Request made but no response
// // // // // // // // //                 errorMessage = 'No response from server. Please check your connection.';
// // // // // // // // //             } else {
// // // // // // // // //                 // Request setup failed
// // // // // // // // //                 errorMessage = 'Failed to send request. Please try again.';
// // // // // // // // //             }

// // // // // // // // //             return rejectWithValue({
// // // // // // // // //                 message: errorMessage,
// // // // // // // // //                 technicalDetails: error.response?.data?.message || error.message,
// // // // // // // // //                 status: error.response?.status,
// // // // // // // // //                 details: error.response?.data
// // // // // // // // //             });
// // // // // // // // //         }
// // // // // // // // //     }
// // // // // // // // // );

// // // // // // // // // Update the error handling in the uploadImage thunk
// // // // // // // // const uploadImage = createAsyncThunk(
// // // // // // // //     'extraction/uploadImage',
// // // // // // // //     async (formData, { rejectWithValue, getState }) => {
// // // // // // // //         try {
// // // // // // // //             const { auth } = getState();
// // // // // // // //             const token = auth.token;

// // // // // // // //             if (!token) {
// // // // // // // //                 throw new Error("Missing authentication token");
// // // // // // // //             }

// // // // // // // //             // Create axios instance with custom config
// // // // // // // //             const axiosInstance = axios.create({
// // // // // // // //                 baseURL: 'http://localhost:8000',
// // // // // // // //                 timeout: 60000,
// // // // // // // //                 maxContentLength: Infinity,
// // // // // // // //                 maxBodyLength: Infinity,
// // // // // // // //             });

// // // // // // // //             // Log the request details
// // // // // // // //             const fileInfo = formData.get('file');
// // // // // // // //             console.log('Preparing upload:', {
// // // // // // // //                 fileSize: fileInfo ? `${(fileInfo.size / (1024 * 1024)).toFixed(2)} MB` : 'No file',
// // // // // // // //                 fileType: fileInfo?.type,
// // // // // // // //                 fileName: fileInfo?.name,
// // // // // // // //             });

// // // // // // // //             // Send the upload request
// // // // // // // //             const response = await axiosInstance.post('/extraction/upload', formData, {
// // // // // // // //                 headers: {
// // // // // // // //                     'Content-Type': 'multipart/form-data',
// // // // // // // //                     Authorization: `Bearer ${token}`,
// // // // // // // //                 },
// // // // // // // //                 onUploadProgress: (progressEvent) => {
// // // // // // // //                     const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
// // // // // // // //                     console.log(`Upload progress: ${percentCompleted}%`);
// // // // // // // //                 },
// // // // // // // //             });

// // // // // // // //             // Log successful response
// // // // // // // //             console.log('Upload successful:', {
// // // // // // // //                 status: response.status,
// // // // // // // //                 data: response.data,
// // // // // // // //             });

// // // // // // // //             return response.data;
// // // // // // // //         } catch (error) {
// // // // // // // //             // Log detailed error information
// // // // // // // //             console.error('Upload error:', {
// // // // // // // //                 message: error.message,
// // // // // // // //                 response: {
// // // // // // // //                     status: error.response?.status,
// // // // // // // //                     statusText: error.response?.statusText,
// // // // // // // //                     data: error.response?.data,
// // // // // // // //                 },
// // // // // // // //                 request: error.request ? 'Request was made but no response received' : 'Request setup failed',
// // // // // // // //                 config: {
// // // // // // // //                     url: error.config?.url,
// // // // // // // //                     method: error.config?.method,
// // // // // // // //                     headers: error.config?.headers,
// // // // // // // //                     timeout: error.config?.timeout,
// // // // // // // //                 },
// // // // // // // //             });

// // // // // // // //             // Extract error details from response
// // // // // // // //             const errorDetails = error.response?.data?.detail || error.response?.data;
// // // // // // // //             const errorMessage = typeof errorDetails === 'string' ? errorDetails :
// // // // // // // //                 errorDetails?.message || 'Failed to upload image.';

// // // // // // // //             // Determine appropriate error message based on status code
// // // // // // // //             let userMessage = '';
// // // // // // // //             if (error.response) {
// // // // // // // //                 switch (error.response.status) {
// // // // // // // //                     case 400:
// // // // // // // //                         userMessage = errorMessage || 'Invalid file format or request.';
// // // // // // // //                         break;
// // // // // // // //                     case 401:
// // // // // // // //                         userMessage = 'Please log in again to upload files.';
// // // // // // // //                         break;
// // // // // // // //                     case 413:
// // // // // // // //                         userMessage = 'File is too large for the server to process. Maximum size is 10MB.';
// // // // // // // //                         break;
// // // // // // // //                     case 415:
// // // // // // // //                         userMessage = errorMessage || 'Unsupported file type. Please use JPG, PNG, TIFF, or PDF.';
// // // // // // // //                         break;
// // // // // // // //                     case 500:
// // // // // // // //                         userMessage = 'Server encountered an error while processing the file. Please try again or contact support.';
// // // // // // // //                         break;
// // // // // // // //                     default:
// // // // // // // //                         userMessage = errorMessage || `Upload failed (${error.response.status})`;
// // // // // // // //                 }
// // // // // // // //             } else if (error.request) {
// // // // // // // //                 userMessage = 'No response from server. Please check your connection and try again.';
// // // // // // // //             } else {
// // // // // // // //                 userMessage = 'Failed to send request. Please try again.';
// // // // // // // //             }

// // // // // // // //             return rejectWithValue({
// // // // // // // //                 message: userMessage,
// // // // // // // //                 technicalDetails: errorMessage,
// // // // // // // //                 status: error.response?.status,
// // // // // // // //                 details: error.response?.data
// // // // // // // //             });
// // // // // // // //         }
// // // // // // // //     }
// // // // // // // // );

// // // // // // // // // Async thunk to extract signature
// // // // // // // // const extractSignature = createAsyncThunk(
// // // // // // // //     'extraction/extractSignature',
// // // // // // // //     async ({ imageId, cropData }, { rejectWithValue, getState }) => {
// // // // // // // //         try {
// // // // // // // //             const { auth } = getState();
// // // // // // // //             const token = auth.token;

// // // // // // // //             if (!token) {
// // // // // // // //                 throw new Error("Missing authentication token");
// // // // // // // //             }

// // // // // // // //             const headers = {
// // // // // // // //                 'Content-Type': 'application/json',
// // // // // // // //                 Authorization: `Bearer ${token}`,
// // // // // // // //             };

// // // // // // // //             const response = await axios.post(
// // // // // // // //                 `http://localhost:8000/extraction/${imageId}/extract`,
// // // // // // // //                 cropData,
// // // // // // // //                 { headers }
// // // // // // // //             );
// // // // // // // //             return { imageId, signature: response.data.signature };
// // // // // // // //         } catch (error) {
// // // // // // // //             return rejectWithValue(error.response?.data || { message: "Signature extraction failed" });
// // // // // // // //         }
// // // // // // // //     }
// // // // // // // // );

// // // // // // // // const extractionSlice = createSlice({
// // // // // // // //     name: 'extraction',
// // // // // // // //     initialState: {
// // // // // // // //         images: [],
// // // // // // // //         loading: false,
// // // // // // // //         error: null,
// // // // // // // //         extractedSignatures: {},
// // // // // // // //     },
// // // // // // // //     reducers: {},
// // // // // // // //     extraReducers: (builder) => {
// // // // // // // //         builder
// // // // // // // //             .addCase(uploadImage.pending, (state) => {
// // // // // // // //                 state.loading = true;
// // // // // // // //                 state.error = null;
// // // // // // // //             })
// // // // // // // //             .addCase(uploadImage.fulfilled, (state, action) => {
// // // // // // // //                 state.loading = false;
// // // // // // // //                 state.images.push(action.payload.image);
// // // // // // // //             })
// // // // // // // //             .addCase(uploadImage.rejected, (state, action) => {
// // // // // // // //                 state.loading = false;
// // // // // // // //                 state.error = action.payload.message || 'Image upload failed';
// // // // // // // //             })
// // // // // // // //             .addCase(extractSignature.pending, (state) => {
// // // // // // // //                 state.loading = true;
// // // // // // // //                 state.error = null;
// // // // // // // //             })
// // // // // // // //             .addCase(extractSignature.fulfilled, (state, action) => {
// // // // // // // //                 state.loading = false;
// // // // // // // //                 state.extractedSignatures[action.payload.imageId] = action.payload.signature;
// // // // // // // //             })
// // // // // // // //             .addCase(extractSignature.rejected, (state, action) => {
// // // // // // // //                 state.loading = false;
// // // // // // // //                 state.error = action.payload.message || 'Signature extraction failed';
// // // // // // // //             });
// // // // // // // //     },
// // // // // // // // });

// // // // // // // // export default extractionSlice.reducer;

// // // // // // // // // Export the async thunks and reducer
// // // // // // // // export { uploadImage, extractSignature };

// // // // // // // import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// // // // // // // import axios from 'axios';

// // // // // // // // Utility function to format error messages
// // // // // // // const formatErrorMessage = (error) => {
// // // // // // //     if (error.response?.data?.detail) {
// // // // // // //         return typeof error.response.data.detail === 'string'
// // // // // // //             ? error.response.data.detail
// // // // // // //             : JSON.stringify(error.response.data.detail);
// // // // // // //     }
// // // // // // //     return error.message || 'An unknown error occurred';
// // // // // // // };

// // // // // // // // Create axios instance with default config
// // // // // // // const api = axios.create({
// // // // // // //     baseURL: 'http://localhost:8000',
// // // // // // //     timeout: 30000,
// // // // // // //     headers: {
// // // // // // //         'Accept': 'application/json',
// // // // // // //     }
// // // // // // // });

// // // // // // // // Async thunk to upload image
// // // // // // // const uploadImage = createAsyncThunk(
// // // // // // //     'extraction/uploadImage',
// // // // // // //     async (formData, { rejectWithValue, getState }) => {
// // // // // // //         try {
// // // // // // //             const { auth } = getState();
// // // // // // //             const token = auth.token;

// // // // // // //             if (!token) {
// // // // // // //                 throw new Error("Missing authentication token");
// // // // // // //             }

// // // // // // //             // Log the request details
// // // // // // //             const fileInfo = formData.get('file');
// // // // // // //             console.log('Preparing upload:', {
// // // // // // //                 fileSize: fileInfo ? `${(fileInfo.size / (1024 * 1024)).toFixed(2)} MB` : 'No file',
// // // // // // //                 fileType: fileInfo?.type,
// // // // // // //                 fileName: fileInfo?.name,
// // // // // // //             });

// // // // // // //             // Send the upload request
// // // // // // //             const response = await api.post('/extraction/upload', formData, {
// // // // // // //                 headers: {
// // // // // // //                     'Content-Type': 'multipart/form-data',
// // // // // // //                     'Authorization': `Bearer ${token}`,
// // // // // // //                 },
// // // // // // //                 onUploadProgress: (progressEvent) => {
// // // // // // //                     const percentCompleted = Math.round(
// // // // // // //                         (progressEvent.loaded * 100) / progressEvent.total
// // // // // // //                     );
// // // // // // //                     console.log(`Upload progress: ${percentCompleted}%`);
// // // // // // //                 },
// // // // // // //             });

// // // // // // //             console.log('Upload successful:', response.data);
// // // // // // //             return response.data;

// // // // // // //         } catch (error) {
// // // // // // //             console.error('Upload error:', {
// // // // // // //                 message: error.message,
// // // // // // //                 response: {
// // // // // // //                     status: error.response?.status,
// // // // // // //                     statusText: error.response?.statusText,
// // // // // // //                     data: error.response?.data,
// // // // // // //                 },
// // // // // // //                 request: error.request ? 'Request was made but no response received' : 'Request setup failed',
// // // // // // //             });

// // // // // // //             return rejectWithValue({
// // // // // // //                 message: formatErrorMessage(error),
// // // // // // //                 status: error.response?.status,
// // // // // // //                 details: error.response?.data
// // // // // // //             });
// // // // // // //         }
// // // // // // //     }
// // // // // // // );

// // // // // // // // Async thunk to extract signature
// // // // // // // const extractSignature = createAsyncThunk(
// // // // // // //     'extraction/extractSignature',
// // // // // // //     async ({ imageId, cropData }, { rejectWithValue, getState }) => {
// // // // // // //         try {
// // // // // // //             const { auth } = getState();
// // // // // // //             const token = auth.token;

// // // // // // //             if (!token) {
// // // // // // //                 throw new Error("Missing authentication token");
// // // // // // //             }

// // // // // // //             const response = await api.post(
// // // // // // //                 `/extraction/${imageId}/extract`,
// // // // // // //                 cropData,
// // // // // // //                 {
// // // // // // //                     headers: {
// // // // // // //                         'Content-Type': 'application/json',
// // // // // // //                         'Authorization': `Bearer ${token}`,
// // // // // // //                     }
// // // // // // //                 }
// // // // // // //             );

// // // // // // //             return response.data;
// // // // // // //         } catch (error) {
// // // // // // //             return rejectWithValue({
// // // // // // //                 message: formatErrorMessage(error),
// // // // // // //                 status: error.response?.status,
// // // // // // //                 details: error.response?.data
// // // // // // //             });
// // // // // // //         }
// // // // // // //     }
// // // // // // // );

// // // // // // // const extractionSlice = createSlice({
// // // // // // //     name: 'extraction',
// // // // // // //     initialState: {
// // // // // // //         images: [],
// // // // // // //         loading: false,
// // // // // // //         error: null,
// // // // // // //         uploadProgress: 0,
// // // // // // //         extractedSignatures: {},
// // // // // // //     },
// // // // // // //     reducers: {
// // // // // // //         clearError: (state) => {
// // // // // // //             state.error = null;
// // // // // // //         },
// // // // // // //         setUploadProgress: (state, action) => {
// // // // // // //             state.uploadProgress = action.payload;
// // // // // // //         },
// // // // // // //     },
// // // // // // //     extraReducers: (builder) => {
// // // // // // //         builder
// // // // // // //             // Upload Image
// // // // // // //             .addCase(uploadImage.pending, (state) => {
// // // // // // //                 state.loading = true;
// // // // // // //                 state.error = null;
// // // // // // //                 state.uploadProgress = 0;
// // // // // // //             })
// // // // // // //             .addCase(uploadImage.fulfilled, (state, action) => {
// // // // // // //                 state.loading = false;
// // // // // // //                 state.uploadProgress = 100;
// // // // // // //                 if (action.payload.image) {
// // // // // // //                     state.images.push(action.payload.image);
// // // // // // //                 }
// // // // // // //             })
// // // // // // //             .addCase(uploadImage.rejected, (state, action) => {
// // // // // // //                 state.loading = false;
// // // // // // //                 state.uploadProgress = 0;
// // // // // // //                 state.error = action.payload?.message || 'Image upload failed';
// // // // // // //             })
// // // // // // //             // Extract Signature
// // // // // // //             .addCase(extractSignature.pending, (state) => {
// // // // // // //                 state.loading = true;
// // // // // // //                 state.error = null;
// // // // // // //             })
// // // // // // //             .addCase(extractSignature.fulfilled, (state, action) => {
// // // // // // //                 state.loading = false;
// // // // // // //                 if (action.payload.image) {
// // // // // // //                     const index = state.images.findIndex(img => img.id === action.payload.image.id);
// // // // // // //                     if (index !== -1) {
// // // // // // //                         state.images[index] = action.payload.image;
// // // // // // //                     }
// // // // // // //                     state.extractedSignatures[action.payload.image.id] = action.payload.image.extracted_signature_path;
// // // // // // //                 }
// // // // // // //             })
// // // // // // //             .addCase(extractSignature.rejected, (state, action) => {
// // // // // // //                 state.loading = false;
// // // // // // //                 state.error = action.payload?.message || 'Signature extraction failed';
// // // // // // //             });
// // // // // // //     },
// // // // // // // });

// // // // // // // export const { clearError, setUploadProgress } = extractionSlice.actions;
// // // // // // // export { uploadImage, extractSignature };
// // // // // // // export default extractionSlice.reducer;

// // // // // // import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// // // // // // import { api, handleApiError } from '../../utils/api';

// // // // // // // Async thunk to upload image
// // // // // // const uploadImage = createAsyncThunk(
// // // // // //     'extraction/uploadImage',
// // // // // //     async (formData, { rejectWithValue }) => {
// // // // // //         try {
// // // // // //             // Log the request details
// // // // // //             const fileInfo = formData.get('file');
// // // // // //             console.log('Preparing upload:', {
// // // // // //                 fileSize: fileInfo ? `${(fileInfo.size / (1024 * 1024)).toFixed(2)} MB` : 'No file',
// // // // // //                 fileType: fileInfo?.type,
// // // // // //                 fileName: fileInfo?.name,
// // // // // //             });

// // // // // //             // Send the upload request
// // // // // //             const response = await api.post('/extraction/upload', formData, {
// // // // // //                 headers: {
// // // // // //                     'Content-Type': 'multipart/form-data',
// // // // // //                 },
// // // // // //                 onUploadProgress: (progressEvent) => {
// // // // // //                     const percentCompleted = Math.round(
// // // // // //                         (progressEvent.loaded * 100) / progressEvent.total
// // // // // //                     );
// // // // // //                     console.log(`Upload progress: ${percentCompleted}%`);
// // // // // //                 },
// // // // // //             });

// // // // // //             console.log('Upload successful:', response.data);
// // // // // //             return response.data;

// // // // // //         } catch (error) {
// // // // // //             return rejectWithValue(handleApiError(error));
// // // // // //         }
// // // // // //     }
// // // // // // );

// // // // // // // Async thunk to extract signature
// // // // // // const extractSignature = createAsyncThunk(
// // // // // //     'extraction/extractSignature',
// // // // // //     async ({ imageId, cropData }, { rejectWithValue }) => {
// // // // // //         try {
// // // // // //             const response = await api.post(
// // // // // //                 `/extraction/${imageId}/extract`,
// // // // // //                 cropData,
// // // // // //                 {
// // // // // //                     headers: {
// // // // // //                         'Content-Type': 'application/json',
// // // // // //                     }
// // // // // //                 }
// // // // // //             );

// // // // // //             return response.data;
// // // // // //         } catch (error) {
// // // // // //             return rejectWithValue(handleApiError(error));
// // // // // //         }
// // // // // //     }
// // // // // // );

// // // // // // const extractionSlice = createSlice({
// // // // // //     name: 'extraction',
// // // // // //     initialState: {
// // // // // //         images: [],
// // // // // //         loading: false,
// // // // // //         error: null,
// // // // // //         uploadProgress: 0,
// // // // // //         extractedSignatures: {},
// // // // // //     },
// // // // // //     reducers: {
// // // // // //         clearError: (state) => {
// // // // // //             state.error = null;
// // // // // //         },
// // // // // //         setUploadProgress: (state, action) => {
// // // // // //             state.uploadProgress = action.payload;
// // // // // //         },
// // // // // //     },
// // // // // //     extraReducers: (builder) => {
// // // // // //         builder
// // // // // //             // Upload Image
// // // // // //             .addCase(uploadImage.pending, (state) => {
// // // // // //                 state.loading = true;
// // // // // //                 state.error = null;
// // // // // //                 state.uploadProgress = 0;
// // // // // //             })
// // // // // //             .addCase(uploadImage.fulfilled, (state, action) => {
// // // // // //                 state.loading = false;
// // // // // //                 state.uploadProgress = 100;
// // // // // //                 if (action.payload.image) {
// // // // // //                     state.images.push(action.payload.image);
// // // // // //                 }
// // // // // //             })
// // // // // //             .addCase(uploadImage.rejected, (state, action) => {
// // // // // //                 state.loading = false;
// // // // // //                 state.uploadProgress = 0;
// // // // // //                 state.error = action.payload?.message || 'Image upload failed';
// // // // // //             })
// // // // // //             // Extract Signature
// // // // // //             .addCase(extractSignature.pending, (state) => {
// // // // // //                 state.loading = true;
// // // // // //                 state.error = null;
// // // // // //             })
// // // // // //             .addCase(extractSignature.fulfilled, (state, action) => {
// // // // // //                 state.loading = false;
// // // // // //                 if (action.payload.image) {
// // // // // //                     const index = state.images.findIndex(img => img.id === action.payload.image.id);
// // // // // //                     if (index !== -1) {
// // // // // //                         state.images[index] = action.payload.image;
// // // // // //                     }
// // // // // //                     state.extractedSignatures[action.payload.image.id] = action.payload.image.extracted_signature_path;
// // // // // //                 }
// // // // // //             })
// // // // // //             .addCase(extractSignature.rejected, (state, action) => {
// // // // // //                 state.loading = false;
// // // // // //                 state.error = action.payload?.message || 'Signature extraction failed';
// // // // // //             });
// // // // // //     },
// // // // // // });

// // // // // // export const { clearError, setUploadProgress } = extractionSlice.actions;
// // // // // // export { uploadImage, extractSignature };
// // // // // // export default extractionSlice.reducer;

// // // // // import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// // // // // import axiosInstance from '../../utils/axiosInstance';

// // // // // export const uploadImage = createAsyncThunk(
// // // // //     'extraction/uploadImage',
// // // // //     async (formData) => {
// // // // //         const response = await axiosInstance.post('/extraction/upload/', formData, {
// // // // //             headers: {
// // // // //                 'Content-Type': 'multipart/form-data'
// // // // //             }
// // // // //         });
// // // // //         return response.data;
// // // // //     }
// // // // // );

// // // // // export const selectRegion = createAsyncThunk(
// // // // //     'extraction/selectRegion',
// // // // //     async ({ session_id, x1, y1, x2, y2 }) => {
// // // // //         const response = await axiosInstance.post('/extraction/select_region/', {
// // // // //             session_id,
// // // // //             x1,
// // // // //             y1,
// // // // //             x2,
// // // // //             y2
// // // // //         });
// // // // //         return response.data;
// // // // //     }
// // // // // );

// // // // // export const processImage = createAsyncThunk(
// // // // //     'extraction/processImage',
// // // // //     async ({ session_id, color, threshold }) => {
// // // // //         const response = await axiosInstance.post('/extraction/process_image/', {
// // // // //             session_id,
// // // // //             color,
// // // // //             threshold
// // // // //         }, {
// // // // //             responseType: 'blob'
// // // // //         });
// // // // //         return URL.createObjectURL(response.data);
// // // // //     }
// // // // // );

// // // // // export const resetSession = createAsyncThunk(
// // // // //     'extraction/resetSession',
// // // // //     async (session_id) => {
// // // // //         const response = await axiosInstance.post('/extraction/reset_session/', { session_id });
// // // // //         return response.data;
// // // // //     }
// // // // // );

// // // // // const extractionSlice = createSlice({
// // // // //     name: 'extraction',
// // // // //     initialState: {
// // // // //         loading: false,
// // // // //         error: null,
// // // // //         uploadProgress: 0,
// // // // //         finalImage: null
// // // // //     },
// // // // //     reducers: {
// // // // //         clearError(state) {
// // // // //             state.error = null;
// // // // //         }
// // // // //     },
// // // // //     extraReducers: (builder) => {
// // // // //         builder
// // // // //             .addCase(uploadImage.pending, (state) => {
// // // // //                 state.loading = true;
// // // // //                 state.error = null;
// // // // //             })
// // // // //             .addCase(uploadImage.fulfilled, (state) => {
// // // // //                 state.loading = false;
// // // // //             })
// // // // //             .addCase(uploadImage.rejected, (state, action) => {
// // // // //                 state.loading = false;
// // // // //                 state.error = action.error.message;
// // // // //             })
// // // // //             .addCase(selectRegion.pending, (state) => {
// // // // //                 state.loading = true;
// // // // //                 state.error = null;
// // // // //             })
// // // // //             .addCase(selectRegion.fulfilled, (state) => {
// // // // //                 state.loading = false;
// // // // //             })
// // // // //             .addCase(selectRegion.rejected, (state, action) => {
// // // // //                 state.loading = false;
// // // // //                 state.error = action.error.message;
// // // // //             })
// // // // //             .addCase(processImage.pending, (state) => {
// // // // //                 state.loading = true;
// // // // //                 state.error = null;
// // // // //             })
// // // // //             .addCase(processImage.fulfilled, (state, action) => {
// // // // //                 state.loading = false;
// // // // //                 state.finalImage = action.payload;
// // // // //             })
// // // // //             .addCase(processImage.rejected, (state, action) => {
// // // // //                 state.loading = false;
// // // // //                 state.error = action.error.message;
// // // // //             })
// // // // //             .addCase(resetSession.pending, (state) => {
// // // // //                 state.loading = true;
// // // // //                 state.error = null;
// // // // //             })
// // // // //             .addCase(resetSession.fulfilled, (state) => {
// // // // //                 state.loading = false;
// // // // //                 state.finalImage = null;
// // // // //             })
// // // // //             .addCase(resetSession.rejected, (state, action) => {
// // // // //                 state.loading = false;
// // // // //                 state.error = action.error.message;
// // // // //             });
// // // // //     }
// // // // // });

// // // // // export const { clearError } = extractionSlice.actions;

// // // // // export default extractionSlice.reducer;

// // // // import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// // // // import axiosInstance from '../../utils/axiosInstance';

// // // // export const uploadImage = createAsyncThunk(
// // // //     'extraction/uploadImage',
// // // //     async (formData) => {
// // // //         const response = await axiosInstance.post('/extraction/upload/', formData, {
// // // //             headers: {
// // // //                 'Content-Type': 'multipart/form-data'
// // // //             }
// // // //         });
// // // //         return response.data;
// // // //     }
// // // // );

// // // // export const selectRegion = createAsyncThunk(
// // // //     'extraction/selectRegion',
// // // //     async ({ session_id, x1, y1, x2, y2 }) => {
// // // //         const response = await axiosInstance.post('/extraction/select_region/', {
// // // //             session_id,
// // // //             x1,
// // // //             y1,
// // // //             x2,
// // // //             y2
// // // //         });
// // // //         return response.data;
// // // //     }
// // // // );

// // // // export const processImage = createAsyncThunk(
// // // //     'extraction/processImage',
// // // //     async ({ session_id, color, threshold }) => {
// // // //         const response = await axiosInstance.post('/extraction/process_image/', {
// // // //             session_id,
// // // //             color,
// // // //             threshold
// // // //         }, {
// // // //             responseType: 'blob'
// // // //         });
// // // //         return URL.createObjectURL(response.data);
// // // //     }
// // // // );

// // // // export const resetSession = createAsyncThunk(
// // // //     'extraction/resetSession',
// // // //     async (session_id) => {
// // // //         const response = await axiosInstance.post('/extraction/reset_session/', { session_id });
// // // //         return response.data;
// // // //     }
// // // // );

// // // // const extractionSlice = createSlice({
// // // //     name: 'extraction',
// // // //     initialState: {
// // // //         loading: false,
// // // //         error: null,
// // // //         uploadProgress: 0,
// // // //         finalImage: null
// // // //     },
// // // //     reducers: {
// // // //         clearError(state) {
// // // //             state.error = null;
// // // //         }
// // // //     },
// // // //     extraReducers: (builder) => {
// // // //         builder
// // // //             .addCase(uploadImage.pending, (state) => {
// // // //                 state.loading = true;
// // // //                 state.error = null;
// // // //             })
// // // //             .addCase(uploadImage.fulfilled, (state) => {
// // // //                 state.loading = false;
// // // //             })
// // // //             .addCase(uploadImage.rejected, (state, action) => {
// // // //                 state.loading = false;
// // // //                 state.error = action.error.message;
// // // //             })
// // // //             .addCase(selectRegion.pending, (state) => {
// // // //                 state.loading = true;
// // // //                 state.error = null;
// // // //             })
// // // //             .addCase(selectRegion.fulfilled, (state) => {
// // // //                 state.loading = false;
// // // //             })
// // // //             .addCase(selectRegion.rejected, (state, action) => {
// // // //                 state.loading = false;
// // // //                 state.error = action.error.message;
// // // //             })
// // // //             .addCase(processImage.pending, (state) => {
// // // //                 state.loading = true;
// // // //                 state.error = null;
// // // //             })
// // // //             .addCase(processImage.fulfilled, (state, action) => {
// // // //                 state.loading = false;
// // // //                 state.finalImage = action.payload;
// // // //             })
// // // //             .addCase(processImage.rejected, (state, action) => {
// // // //                 state.loading = false;
// // // //                 state.error = action.error.message;
// // // //             })
// // // //             .addCase(resetSession.pending, (state) => {
// // // //                 state.loading = true;
// // // //                 state.error = null;
// // // //             })
// // // //             .addCase(resetSession.fulfilled, (state) => {
// // // //                 state.loading = false;
// // // //                 state.finalImage = null;
// // // //             })
// // // //             .addCase(resetSession.rejected, (state, action) => {
// // // //                 state.loading = false;
// // // //                 state.error = action.error.message;
// // // //             });
// // // //     }
// // // // });

// // // // export const { clearError } = extractionSlice.actions;

// // // // export default extractionSlice.reducer;


// // // import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// // // import axiosInstance from '../../utils/axiosInstance';

// // // export const uploadImage = createAsyncThunk(
// // //     'extraction/uploadImage',
// // //     async (formData) => {
// // //         const response = await axiosInstance.post('/extraction/upload/', formData, {
// // //             headers: {
// // //                 'Content-Type': 'multipart/form-data'
// // //             }
// // //         });
// // //         return response.data;
// // //     }
// // // );

// // // export const selectRegion = createAsyncThunk(
// // //     'extraction/selectRegion',
// // //     async ({ session_id, x1, y1, x2, y2 }) => {
// // //         const response = await axiosInstance.post('/extraction/select_region/', {
// // //             session_id,
// // //             x1,
// // //             y1,
// // //             x2,
// // //             y2
// // //         });
// // //         return response.data;
// // //     }
// // // );

// // // export const processImage = createAsyncThunk(
// // //     'extraction/processImage',
// // //     async ({ session_id, region, color, threshold }) => {
// // //         const response = await axiosInstance.post('/extraction/process_image/', {
// // //             session_id,
// // //             x1: region.x1,
// // //             y1: region.y1,
// // //             x2: region.x2,
// // //             y2: region.y2,
// // //             color,
// // //             threshold
// // //         }, {
// // //             responseType: 'blob'
// // //         });
// // //         return URL.createObjectURL(response.data); // Returns processed image URL
// // //     }
// // // );

// // // export const resetSession = createAsyncThunk(
// // //     'extraction/resetSession',
// // //     async (session_id) => {
// // //         const response = await axiosInstance.post('/extraction/reset_session/', { session_id });
// // //         return response.data;
// // //     }
// // // );

// // // const extractionSlice = createSlice({
// // //     name: 'extraction',
// // //     initialState: {
// // //         loading: false,
// // //         error: null,
// // //         uploadProgress: 0,
// // //         finalImage: null
// // //     },
// // //     reducers: {
// // //         clearError(state) {
// // //             state.error = null;
// // //         }
// // //     },
// // //     extraReducers: (builder) => {
// // //         builder
// // //             .addCase(uploadImage.pending, (state) => {
// // //                 state.loading = true;
// // //                 state.error = null;
// // //             })
// // //             .addCase(uploadImage.fulfilled, (state) => {
// // //                 state.loading = false;
// // //             })
// // //             .addCase(uploadImage.rejected, (state, action) => {
// // //                 state.loading = false;
// // //                 state.error = action.error.message;
// // //             })
// // //             .addCase(selectRegion.pending, (state) => {
// // //                 state.loading = true;
// // //                 state.error = null;
// // //             })
// // //             .addCase(selectRegion.fulfilled, (state) => {
// // //                 state.loading = false;
// // //             })
// // //             .addCase(selectRegion.rejected, (state, action) => {
// // //                 state.loading = false;
// // //                 state.error = action.error.message;
// // //             })
// // //             .addCase(processImage.pending, (state) => {
// // //                 state.loading = true;
// // //                 state.error = null;
// // //             })
// // //             .addCase(processImage.fulfilled, (state, action) => {
// // //                 state.loading = false;
// // //                 state.finalImage = action.payload;
// // //             })
// // //             .addCase(processImage.rejected, (state, action) => {
// // //                 state.loading = false;
// // //                 state.error = action.error.message;
// // //             })
// // //             .addCase(resetSession.pending, (state) => {
// // //                 state.loading = true;
// // //                 state.error = null;
// // //             })
// // //             .addCase(resetSession.fulfilled, (state) => {
// // //                 state.loading = false;
// // //                 state.finalImage = null;
// // //             })
// // //             .addCase(resetSession.rejected, (state, action) => {
// // //                 state.loading = false;
// // //                 state.error = action.error.message;
// // //             });
// // //     }
// // // });

// // // export const { clearError } = extractionSlice.actions;

// // // export default extractionSlice.reducer;


// // import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// // import axiosInstance from '../../utils/axiosInstance';

// // // Async thunk for uploading an image
// // export const uploadImage = createAsyncThunk(
// //     'extraction/uploadImage',
// //     async (formData) => {
// //         const response = await axiosInstance.post('/extraction/upload', formData, {
// //             headers: { 'Content-Type': 'multipart/form-data' }
// //         });
// //         return response.data;
// //     }
// // );

// // // Async thunk for selecting a region
// // export const selectRegion = createAsyncThunk(
// //     'extraction/selectRegion',
// //     async ({ session_id, x1, y1, x2, y2 }) => {
// //         const response = await axiosInstance.post('/extraction/select_region', {
// //             session_id, x1, y1, x2, y2
// //         });
// //         return response.data;
// //     }
// // );

// // // Async thunk for processing the image
// // export const processImage = createAsyncThunk(
// //     'extraction/processImage',
// //     async ({ session_id, x1, y1, x2, y2, color, threshold }) => {
// //         const response = await axiosInstance.post('/extraction/process_image', {
// //             session_id, x1, y1, x2, y2, color, threshold
// //         }, { responseType: 'blob' });
// //         return URL.createObjectURL(response.data); // Returns processed image URL
// //     }
// // );

// // // Redux slice definition
// // const extractionSlice = createSlice({
// //     name: 'extraction',
// //     initialState: {
// //         loading: false,
// //         error: null,
// //         uploadProgress: 0,
// //         finalImage: null,
// //         sessionId: null,
// //     },
// //     reducers: {
// //         clearError(state) {
// //             state.error = null;
// //         }
// //     },
// //     extraReducers: (builder) => {
// //         builder
// //             .addCase(uploadImage.pending, (state) => { state.loading = true; })
// //             .addCase(uploadImage.fulfilled, (state, action) => {
// //                 state.loading = false;
// //                 state.sessionId = action.payload.id; // Store session ID from response
// //             })
// //             .addCase(uploadImage.rejected, (state, action) => { state.loading = false; state.error = action.error.message; })
// //             .addCase(processImage.pending, (state) => { state.loading = true; })
// //             .addCase(processImage.fulfilled, (state, action) => {
// //                 state.loading = false;
// //                 state.finalImage = action.payload;
// //             })
// //             .addCase(processImage.rejected, (state, action) => { state.loading = false; state.error = action.error.message; });
// //     }
// // });

// // export const { clearError } = extractionSlice.actions;
// // export default extractionSlice.reducer;


// // extractionSlice.js
// import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
// import axiosInstance from '../../utils/axiosInstance';

// export const uploadImage = createAsyncThunk(
//     'extraction/uploadImage',
//     async (formData) => {
//         const response = await axiosInstance.post('/extraction/upload/', formData, {
//             headers: { 'Content-Type': 'multipart/form-data' },
//         });
//         return response.data;
//     }
// );

// export const selectRegion = createAsyncThunk(
//     'extraction/selectRegion',
//     async ({ session_id, x1, y1, x2, y2 }) => {
//         const response = await axiosInstance.post('/extraction/select_region/', {
//             session_id,
//             x1,
//             y1,
//             x2,
//             y2,
//         });
//         return response.data;
//     }
// );

// export const processImage = createAsyncThunk(
//     'extraction/processImage',
//     async ({ session_id, x1, y1, x2, y2, color, threshold }) => {
//         const response = await axiosInstance.post(
//             '/extraction/process_image/',
//             {
//                 session_id,
//                 x1,
//                 y1,
//                 x2,
//                 y2,
//                 color,
//                 threshold,
//             },
//             { responseType: 'blob' }
//         );
//         const blob = new Blob([response.data], { type: 'image/png' });
//         return URL.createObjectURL(blob);
//     }
// );

// const extractionSlice = createSlice({
//     name: 'extraction',
//     initialState: {
//         loading: false,
//         error: null,
//         uploadProgress: 0,
//         finalImage: null,
//         sessionId: null,
//     },
//     reducers: {
//         clearError(state) {
//             state.error = null;
//         },
//     },
//     extraReducers: (builder) => {
//         builder
//             .addCase(uploadImage.pending, (state) => {
//                 state.loading = true;
//             })
//             .addCase(uploadImage.fulfilled, (state, action) => {
//                 state.loading = false;
//                 state.sessionId = action.payload.id;
//             })
//             .addCase(uploadImage.rejected, (state, action) => {
//                 state.loading = false;
//                 state.error = action.error.message;
//             })
//             .addCase(processImage.pending, (state) => {
//                 state.loading = true;
//             })
//             .addCase(processImage.fulfilled, (state, action) => {
//                 state.loading = false;
//                 state.finalImage = action.payload;
//             })
//             .addCase(processImage.rejected, (state, action) => {
//                 state.loading = false;
//                 state.error = action.error.message;
//             });
//     },
// });

// export const { clearError } = extractionSlice.actions;
// export default extractionSlice.reducer;

// extractionSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../utils/axiosInstance';

// Helper to construct complete image URL
const getFullImageUrl = (path) => {
    const baseUrl = 'http://127.0.0.1:8000';
    const cleanPath = path.startsWith('/') ? path : `/${path}`;
    return `${baseUrl}${cleanPath}`;
};

// Upload image thunk
export const uploadImage = createAsyncThunk(
    'extraction/uploadImage',
    async (formData, { dispatch, rejectWithValue }) => {
        try {
            const response = await axiosInstance.post('/extraction/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round(
                        (progressEvent.loaded * 100) / progressEvent.total
                    );
                    dispatch(setUploadProgress(percentCompleted));
                },
            });

            console.log('Upload response:', response.data);

            if (!response.data.id || !response.data.file_path) {
                throw new Error('Incomplete response from server.');
            }

            return {
                id: response.data.id,
                file_path: response.data.file_path,
                imageUrl: getFullImageUrl(response.data.file_path),
            };
        } catch (error) {
            console.error('Upload error:', error);
            const message = error.response?.data?.message || error.message || 'Upload failed';
            return rejectWithValue(message);
        }
    }
);

// Select region thunk
export const selectRegion = createAsyncThunk(
    'extraction/selectRegion',
    async ({ sessionId, x1, y1, x2, y2 }, { rejectWithValue }) => {
        try {
            const response = await axiosInstance.post('/extraction/select_region/', {
                session_id: sessionId,
                x1,
                y1,
                x2,
                y2,
            });
            return response.data;
        } catch (error) {
            console.error('Region selection error:', error);
            const message = error.response?.data?.message || error.message || 'Region selection failed';
            return rejectWithValue(message);
        }
    }
);

// Process image thunk
export const processImage = createAsyncThunk(
    'extraction/processImage',
    async ({ sessionId, x1, y1, x2, y2, color, threshold }, { rejectWithValue }) => {
        try {
            const response = await axiosInstance.post(
                '/extraction/process_image/',
                {
                    session_id: sessionId,
                    x1,
                    y1,
                    x2,
                    y2,
                    color: color.replace('#', ''),
                    threshold,
                },
                { responseType: 'blob' }
            );

            const blob = new Blob([response.data], { type: 'image/png' });
            const objectUrl = URL.createObjectURL(blob);
            return objectUrl;
        } catch (error) {
            console.error('Image processing error:', error);
            const message = error.response?.data?.message || error.message || 'Processing failed';
            return rejectWithValue(message);
        }
    }
);

// Reset session thunk
export const resetSession = createAsyncThunk(
    'extraction/resetSession',
    async (sessionId, { rejectWithValue }) => {
        try {
            const response = await axiosInstance.post('/extraction/reset_session/', { session_id: sessionId });
            return response.data;
        } catch (error) {
            console.error('Reset session error:', error);
            const message = error.response?.data?.message || error.message || 'Reset failed';
            return rejectWithValue(message);
        }
    }
);

const extractionSlice = createSlice({
    name: 'extraction',
    initialState: {
        loading: false,
        error: null,
        uploadProgress: 0,
        finalImage: null,
        sessionId: null,
        uploadedImageUrl: null,
        selectedRegion: null,
    },
    reducers: {
        clearError: (state) => {
            state.error = null;
        },
        setUploadProgress: (state, action) => {
            state.uploadProgress = action.payload;
        },
        setSelectedRegion: (state, action) => {
            state.selectedRegion = action.payload;
        },
        reset: (state) => {
            state.loading = false;
            state.error = null;
            state.uploadProgress = 0;
            state.finalImage = null;
            state.sessionId = null;
            state.uploadedImageUrl = null;
            state.selectedRegion = null;
        },
    },
    extraReducers: (builder) => {
        builder
            // Upload Image
            .addCase(uploadImage.pending, (state) => {
                state.loading = true;
                state.error = null;
                state.uploadProgress = 0;
            })
            .addCase(uploadImage.fulfilled, (state, action) => {
                state.loading = false;
                state.sessionId = action.payload.id;
                state.uploadedImageUrl = action.payload.imageUrl;
                state.error = null;
                state.uploadProgress = 100;
            })
            .addCase(uploadImage.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || 'Upload failed';
                state.uploadProgress = 0;
            })

            // Select Region
            .addCase(selectRegion.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(selectRegion.fulfilled, (state, action) => {
                state.loading = false;
                state.selectedRegion = action.payload.region; // Adjust based on actual response
                state.error = null;
            })
            .addCase(selectRegion.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || 'Region selection failed';
            })

            // Process Image
            .addCase(processImage.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(processImage.fulfilled, (state, action) => {
                state.loading = false;
                state.finalImage = action.payload;
                state.error = null;
            })
            .addCase(processImage.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || 'Processing failed';
            })

            // Reset Session
            .addCase(resetSession.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(resetSession.fulfilled, (state) => {
                state.loading = false;
                state.finalImage = null;
                state.sessionId = null;
                state.uploadedImageUrl = null;
                state.selectedRegion = null;
                state.error = null;
            })
            .addCase(resetSession.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || 'Reset failed';
            });
    },
});

export const { clearError, setUploadProgress, setSelectedRegion, reset } = extractionSlice.actions;
export default extractionSlice.reducer;