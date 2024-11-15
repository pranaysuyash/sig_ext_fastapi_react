// // import axios from 'axios';

// // const API_BASE_URL = 'http://localhost:8000';

// // // Create axios instance with defaults
// // export const api = axios.create({
// //     baseURL: API_BASE_URL,
// //     timeout: 30000,
// //     headers: {
// //         'Accept': 'application/json'
// //     }
// // });

// // // Add request interceptor for auth token
// // api.interceptors.request.use(
// //     (config) => {
// //         const token = localStorage.getItem('token');
// //         if (token) {
// //             config.headers['Authorization'] = `Bearer ${token}`;
// //         }
// //         return config;
// //     },
// //     (error) => {
// //         return Promise.reject(error);
// //     }
// // );

// // // Add response interceptor for error handling
// // api.interceptors.response.use(
// //     (response) => response,
// //     (error) => {
// //         if (error.response?.status === 401) {
// //             // Handle unauthorized access
// //             localStorage.removeItem('token');
// //             window.location.href = '/login';
// //         }
// //         return Promise.reject(error);
// //     }
// // );

// // export const formatErrorMessage = (error) => {
// //     if (error.response?.data?.detail) {
// //         return typeof error.response.data.detail === 'string'
// //             ? error.response.data.detail
// //             : JSON.stringify(error.response.data.detail);
// //     }
// //     return error.message || 'An unknown error occurred';
// // };

// // export const handleApiError = (error) => {
// //     console.error('API Error:', {
// //         message: error.message,
// //         response: {
// //             status: error.response?.status,
// //             statusText: error.response?.statusText,
// //             data: error.response?.data,
// //         },
// //         request: error.request ? 'Request was made but no response received' : 'Request setup failed',
// //     });

// //     return {
// //         message: formatErrorMessage(error),
// //         status: error.response?.status,
// //         details: error.response?.data
// //     };
// // };

// import axiosInstance from './axiosInstance';

// const uploadImage = async (formData) => {
//     try {
//         const response = await axiosInstance.post('/extraction/upload/', formData, {
//             headers: {
//                 'Content-Type': 'multipart/form-data'
//             }
//         });
//         return response.data;
//     } catch (error) {
//         throw error.response ? error.response.data : error.message;
//     }
// };

// const selectRegion = async ({ session_id, x1, y1, x2, y2 }) => {
//     try {
//         const response = await axiosInstance.post('/extraction/select_region/', {
//             session_id,
//             x1,
//             y1,
//             x2,
//             y2
//         });
//         return response.data;
//     } catch (error) {
//         throw error.response ? error.response.data : error.message;
//     }
// };

// const processImage = async ({ session_id, color, threshold }) => {
//     try {
//         const response = await axiosInstance.post('/extraction/process_image/', {
//             session_id,
//             color,
//             threshold
//         }, {
//             responseType: 'blob'
//         });
//         return URL.createObjectURL(response.data);
//     } catch (error) {
//         throw error.response ? error.response.data : error.message;
//     }
// };

// const resetSession = async (session_id) => {
//     try {
//         const response = await axiosInstance.post('/extraction/reset_session/', { session_id });
//         return response.data;
//     } catch (error) {
//         throw error.response ? error.response.data : error.message;
//     }
// };

// export default {
//     uploadImage,
//     selectRegion,
//     processImage,
//     resetSession
// };

import axiosInstance from './axiosInstance';

const uploadImage = async (formData) => {
    try {
        const response = await axiosInstance.post('/extraction/upload/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error.message;
    }
};

const selectRegion = async ({ session_id, x1, y1, x2, y2 }) => {
    try {
        const response = await axiosInstance.post('/extraction/select_region/', {
            session_id,
            x1,
            y1,
            x2,
            y2
        });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error.message;
    }
};

const processImage = async ({ session_id, color, threshold }) => {
    try {
        const response = await axiosInstance.post('/extraction/process_image/', {
            session_id,
            color,
            threshold
        }, {
            responseType: 'blob'
        });
        return URL.createObjectURL(response.data);
    } catch (error) {
        throw error.response ? error.response.data : error.message;
    }
};

const resetSession = async (session_id) => {
    try {
        const response = await axiosInstance.post('/extraction/reset_session/', { session_id });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error.message;
    }
};

export default {
    uploadImage,
    selectRegion,
    processImage,
    resetSession
};
