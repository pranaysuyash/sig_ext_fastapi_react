// // // // // // // // src/utils/axiosInstance.js
// // // // // // // import axios from 'axios';

// // // // // // // const axiosInstance = axios.create({
// // // // // // //     baseURL: 'http://localhost:8000', // Update with your backend URL
// // // // // // // });

// // // // // // // // Add a request interceptor to include the token
// // // // // // // axiosInstance.interceptors.request.use(
// // // // // // //     (config) => {
// // // // // // //         const token = localStorage.getItem('token');
// // // // // // //         if (token) {
// // // // // // //             config.headers.Authorization = `Bearer ${token}`;
// // // // // // //         }
// // // // // // //         return config;
// // // // // // //     },
// // // // // // //     (error) => Promise.reject(error)
// // // // // // // );

// // // // // // // export default axiosInstance;

// // // // // // import axios from 'axios';

// // // // // // const axiosInstance = axios.create({
// // // // // //     baseURL: 'http://localhost:8000', // Update with your backend URL
// // // // // //     timeout: 10000,
// // // // // //     headers: {
// // // // // //         'Content-Type': 'application/json'
// // // // // //     }
// // // // // // });

// // // // // // // Add a request interceptor
// // // // // // axiosInstance.interceptors.request.use(
// // // // // //     (config) => {
// // // // // //         const token = localStorage.getItem('token');
// // // // // //         if (token) {
// // // // // //             config.headers.Authorization = `Bearer ${token}`;
// // // // // //         }
// // // // // //         return config;
// // // // // //     },
// // // // // //     (error) => {
// // // // // //         return Promise.reject(error);
// // // // // //     }
// // // // // // );

// // // // // // // Add a response interceptor
// // // // // // axiosInstance.interceptors.response.use(
// // // // // //     (response) => {
// // // // // //         return response;
// // // // // //     },
// // // // // //     (error) => {
// // // // // //         if (error.response && error.response.status === 401) {
// // // // // //             // Handle unauthorized access
// // // // // //             localStorage.removeItem('token');
// // // // // //             window.location.href = '/login';
// // // // // //         }
// // // // // //         return Promise.reject(error);
// // // // // //     }
// // // // // // );

// // // // // // export default axiosInstance;

// // // // // import axios from 'axios';

// // // // // const axiosInstance = axios.create({
// // // // //     baseURL: 'http://localhost:8000', // Update with your backend URL
// // // // //     timeout: 10000,
// // // // //     headers: {
// // // // //         'Content-Type': 'application/json'
// // // // //     }
// // // // // });

// // // // // // Add a request interceptor
// // // // // axiosInstance.interceptors.request.use(
// // // // //     (config) => {
// // // // //         const token = localStorage.getItem('token');
// // // // //         if (token) {
// // // // //             config.headers.Authorization = `Bearer ${token}`;
// // // // //         }
// // // // //         return config;
// // // // //     },
// // // // //     (error) => {
// // // // //         return Promise.reject(error);
// // // // //     }
// // // // // );

// // // // // // Add a response interceptor
// // // // // axiosInstance.interceptors.response.use(
// // // // //     (response) => {
// // // // //         return response;
// // // // //     },
// // // // //     (error) => {
// // // // //         if (error.response && error.response.status === 401) {
// // // // //             // Handle unauthorized access
// // // // //             localStorage.removeItem('token');
// // // // //             window.location.href = '/login';
// // // // //         }
// // // // //         return Promise.reject(error);
// // // // //     }
// // // // // );

// // // // // export default axiosInstance;


// // // // // import axios from 'axios';

// // // // // const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

// // // // // const axiosInstance = axios.create({
// // // // //     baseURL: API_URL,
// // // // //     timeout: 10000,
// // // // //     headers: {
// // // // //         'Content-Type': 'application/json'
// // // // //     },
// // // // //     // Enable sending cookies if your API requires it
// // // // //     withCredentials: true
// // // // // });

// // // // // // Add a request interceptor
// // // // // axiosInstance.interceptors.request.use(
// // // // //     (config) => {
// // // // //         // Log the request URL for debugging
// // // // //         console.debug('Making request to:', config.url);

// // // // //         const token = localStorage.getItem('token');
// // // // //         if (token) {
// // // // //             config.headers.Authorization = `Bearer ${token}`;
// // // // //         }
// // // // //         return config;
// // // // //     },
// // // // //     (error) => {
// // // // //         console.error('Request error:', error);
// // // // //         return Promise.reject(error);
// // // // //     }
// // // // // );

// // // // // // Add a response interceptor
// // // // // axiosInstance.interceptors.response.use(
// // // // //     (response) => {
// // // // //         return response;
// // // // //     },
// // // // //     (error) => {
// // // // //         if (error.response) {
// // // // //             // The request was made and the server responded with a status code
// // // // //             // that falls out of the range of 2xx
// // // // //             console.error('Response error:', {
// // // // //                 status: error.response.status,
// // // // //                 data: error.response.data,
// // // // //                 headers: error.response.headers,
// // // // //             });

// // // // //             switch (error.response.status) {
// // // // //                 case 401:
// // // // //                     // Handle unauthorized access
// // // // //                     localStorage.removeItem('token');
// // // // //                     window.location.href = '/login';
// // // // //                     break;
// // // // //                 case 404:
// // // // //                     console.error('API endpoint not found:', error.config.url);
// // // // //                     break;
// // // // //                 case 500:
// // // // //                     console.error('Internal server error');
// // // // //                     break;
// // // // //             }
// // // // //         } else if (error.request) {
// // // // //             // The request was made but no response was received
// // // // //             console.error('No response received:', error.request);
// // // // //         } else {
// // // // //             // Something happened in setting up the request that triggered an Error
// // // // //             console.error('Error setting up request:', error.message);
// // // // //         }

// // // // //         return Promise.reject(error);
// // // // //     }
// // // // // );

// // // // // // Add a method to check API health
// // // // // axiosInstance.checkHealth = async () => {
// // // // //     try {
// // // // //         const response = await axiosInstance.get('/health');
// // // // //         return response.data;
// // // // //     } catch (error) {
// // // // //         console.error('Health check failed:', error);
// // // // //         throw error;
// // // // //     }
// // // // // };

// // // // // export default axiosInstance;

// // // // import axios from 'axios';

// // // // const axiosInstance = axios.create({
// // // //     baseURL: 'http://127.0.0.1:8000',  // Changed from localhost to 127.0.0.1
// // // //     timeout: 10000,
// // // //     headers: {
// // // //         'Content-Type': 'application/json'
// // // //     },
// // // //     withCredentials: true
// // // // });

// // // // // Add a request interceptor
// // // // axiosInstance.interceptors.request.use(
// // // //     (config) => {
// // // //         // Log request for debugging
// // // //         console.debug('Making request:', {
// // // //             url: config.url,
// // // //             method: config.method,
// // // //             data: config.data
// // // //         });

// // // //         const token = localStorage.getItem('token');
// // // //         if (token) {
// // // //             config.headers.Authorization = `Bearer ${token}`;
// // // //         }
// // // //         return config;
// // // //     },
// // // //     (error) => {
// // // //         console.error('Request error:', error);
// // // //         return Promise.reject(error);
// // // //     }
// // // // );

// // // // // Add a response interceptor
// // // // axiosInstance.interceptors.response.use(
// // // //     (response) => {
// // // //         console.debug('Response received:', {
// // // //             url: response.config.url,
// // // //             status: response.status,
// // // //             data: response.data
// // // //         });
// // // //         return response;
// // // //     },
// // // //     (error) => {
// // // //         if (error.response) {
// // // //             console.error('Response error:', {
// // // //                 url: error.config?.url,
// // // //                 status: error.response.status,
// // // //                 data: error.response.data
// // // //             });

// // // //             // Handle specific error cases
// // // //             switch (error.response.status) {
// // // //                 case 401:
// // // //                     localStorage.removeItem('token');
// // // //                     window.location.href = '/login';
// // // //                     break;
// // // //                 case 404:
// // // //                     console.error('Endpoint not found:', error.config.url);
// // // //                     break;
// // // //                 case 500:
// // // //                     console.error('Server error:', error.response.data);
// // // //                     break;
// // // //             }
// // // //         } else if (error.request) {
// // // //             console.error('No response received:', error.request);
// // // //         } else {
// // // //             console.error('Error setting up request:', error.message);
// // // //         }

// // // //         return Promise.reject(error);
// // // //     }
// // // // );

// // // // export default axiosInstance;

// // // import axios from 'axios';

// // // const axiosInstance = axios.create({
// // //     baseURL: 'http://127.0.0.1:8000',  // Changed from localhost to 127.0.0.1
// // //     timeout: 10000,
// // //     headers: {
// // //         'Content-Type': 'application/json'
// // //     },
// // //     withCredentials: true
// // // });

// // // // Add a request interceptor
// // // axiosInstance.interceptors.request.use(
// // //     (config) => {
// // //         // Log request for debugging
// // //         console.debug('Making request:', {
// // //             url: config.url,
// // //             method: config.method,
// // //             data: config.data
// // //         });

// // //         const token = localStorage.getItem('token');
// // //         if (token) {
// // //             config.headers.Authorization = `Bearer ${token}`;
// // //         }
// // //         return config;
// // //     },
// // //     (error) => {
// // //         console.error('Request error:', error);
// // //         return Promise.reject(error);
// // //     }
// // // );

// // // // Add a response interceptor
// // // axiosInstance.interceptors.response.use(
// // //     (response) => {
// // //         console.debug('Response received:', {
// // //             url: response.config.url,
// // //             status: response.status,
// // //             data: response.data
// // //         });
// // //         return response;
// // //     },
// // //     (error) => {
// // //         if (error.response) {
// // //             console.error('Response error:', {
// // //                 url: error.config?.url,
// // //                 status: error.response.status,
// // //                 data: error.response.data
// // //             });

// // //             // Handle specific error cases
// // //             switch (error.response.status) {
// // //                 case 401:
// // //                     localStorage.removeItem('token');
// // //                     window.location.href = '/login';
// // //                     break;
// // //                 case 404:
// // //                     console.error('Endpoint not found:', error.config.url);
// // //                     break;
// // //                 case 500:
// // //                     console.error('Server error:', error.response.data);
// // //                     break;
// // //             }
// // //         } else if (error.request) {
// // //             console.error('No response received:', error.request);
// // //         } else {
// // //             console.error('Error setting up request:', error.message);
// // //         }

// // //         return Promise.reject(error);
// // //     }
// // // );

// // // export default axiosInstance;

// // import axios from 'axios';

// // const axiosInstance = axios.create({
// //     baseURL: 'http://127.0.0.1:8000',
// //     timeout: 10000
// // });

// // // Add a request interceptor
// // axiosInstance.interceptors.request.use(
// //     (config) => {
// //         // Log request for debugging
// //         console.debug('Making request:', {
// //             url: config.url,
// //             method: config.method,
// //             data: config.data
// //         });

// //         const token = localStorage.getItem('token');
// //         if (token) {
// //             config.headers.Authorization = `Bearer ${token}`;
// //         }

// //         // Don't set Content-Type for FormData
// //         if (!(config.data instanceof FormData)) {
// //             config.headers['Content-Type'] = 'application/json';
// //         }

// //         return config;
// //     },
// //     (error) => {
// //         console.error('Request error:', error);
// //         return Promise.reject(error);
// //     }
// // );

// // // Add a response interceptor
// // axiosInstance.interceptors.response.use(
// //     (response) => {
// //         console.debug('Response received:', {
// //             url: response.config.url,
// //             status: response.status,
// //             data: response.data
// //         });
// //         return response;
// //     },
// //     (error) => {
// //         if (error.response) {
// //             console.error('Response error:', {
// //                 url: error.config?.url,
// //                 status: error.response.status,
// //                 data: error.response.data
// //             });

// //             // Handle specific error cases
// //             switch (error.response.status) {
// //                 case 401:
// //                     localStorage.removeItem('token');
// //                     window.location.href = '/login';
// //                     break;
// //                 case 422:
// //                     console.error('Validation error:', error.response.data);
// //                     break;
// //             }
// //         } else if (error.request) {
// //             console.error('No response received:', error.request);
// //         } else {
// //             console.error('Error setting up request:', error.message);
// //         }

// //         return Promise.reject(error);
// //     }
// // );

// // export default axiosInstance;

// import axios from 'axios';

// const axiosInstance = axios.create({
//     baseURL: 'http://127.0.0.1:8000',
//     timeout: 10000
// });

// // Add a request interceptor
// axiosInstance.interceptors.request.use(
//     (config) => {
//         // Log request for debugging
//         console.log('Making request:', {
//             url: config.url,
//             method: config.method,
//             data: config.data instanceof URLSearchParams
//                 ? Object.fromEntries(config.data)
//                 : config.data
//         });

//         const token = localStorage.getItem('token');
//         if (token) {
//             config.headers.Authorization = `Bearer ${token}`;
//         }

//         // Don't override Content-Type if it's already set
//         if (!config.headers['Content-Type']) {
//             config.headers['Content-Type'] = 'application/json';
//         }

//         return config;
//     },
//     (error) => {
//         console.error('Request error:', error);
//         return Promise.reject(error);
//     }
// );

// // Add a response interceptor
// axiosInstance.interceptors.response.use(
//     (response) => {
//         console.debug('Response received:', {
//             url: response.config.url,
//             status: response.status,
//             data: response.data
//         });
//         return response;
//     },
//     (error) => {
//         if (error.response) {
//             console.error('Response error:', {
//                 url: error.config?.url,
//                 status: error.response.status,
//                 data: error.response.data
//             });

//             switch (error.response.status) {
//                 case 401:
//                     localStorage.removeItem('token');
//                     window.location.href = '/login';
//                     break;
//                 case 422:
//                     console.error('Validation error:', error.response.data);
//                     break;
//             }
//         } else if (error.request) {
//             console.error('No response received:', error.request);
//         } else {
//             console.error('Error setting up request:', error.message);
//         }

//         return Promise.reject(error);
//     }
// );

// export default axiosInstance;


import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    timeout: 30000, // Increased timeout for file uploads
    maxContentLength: 50 * 1024 * 1024, // 50MB max content length
    maxBodyLength: 50 * 1024 * 1024, // 50MB max body length
});

// Add a request interceptor
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');

        // Log request details for debugging
        console.debug('Making request:', {
            url: config.url,
            method: config.method,
            headers: {
                ...config.headers,
                Authorization: token ? 'Bearer <token>' : undefined // Hide actual token in logs
            },
            contentType: config.headers['Content-Type']
        });

        // Add auth token if it exists
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        // Don't override Content-Type if it's already set (important for file uploads)
        if (!config.headers['Content-Type']) {
            config.headers['Content-Type'] = 'application/json';
        }

        return config;
    },
    (error) => {
        console.error('Request configuration error:', error);
        return Promise.reject(error);
    }
);

// Add a response interceptor
axiosInstance.interceptors.response.use(
    (response) => {
        // Log successful responses (without sensitive data)
        console.debug('Response received:', {
            url: response.config.url,
            status: response.status,
            statusText: response.statusText,
            data: response.data
        });
        return response;
    },
    (error) => {
        // Handle response errors
        if (error.response) {
            // Server responded with error status
            console.error('Response error:', {
                url: error.config?.url,
                status: error.response.status,
                statusText: error.response.statusText,
                data: error.response.data
            });

            // Handle specific status codes
            switch (error.response.status) {
                case 401:
                    // Unauthorized - clear token and redirect to login
                    localStorage.removeItem('token');
                    window.location.href = '/login';
                    break;

                case 403:
                    // Forbidden - user doesn't have necessary permissions
                    console.error('Permission denied:', error.response.data);
                    error.message = 'You do not have permission to perform this action';
                    break;

                case 413:
                    // Payload too large
                    error.message = 'File is too large. Please try a smaller file.';
                    break;

                case 415:
                    // Unsupported media type
                    error.message = 'File type not supported. Please use JPG or PNG files.';
                    break;

                case 422:
                    // Validation error
                    error.message = Object.values(error.response.data).join('. ');
                    break;

                case 500:
                    // Server error
                    error.message = error.response.data?.detail || 'An unexpected error occurred. Please try again.';
                    console.error('Server error details:', error.response.data);
                    break;

                default:
                    // Generic error message
                    error.message = error.response.data?.detail || 'Request failed. Please try again.';
            }
        } else if (error.request) {
            // Request made but no response received
            console.error('No response received:', {
                url: error.config?.url,
                method: error.config?.method,
                request: error.request
            });
            error.message = 'No response from server. Please check your connection.';
        } else {
            // Request setup error
            console.error('Request setup error:', error.message);
            error.message = 'Failed to send request. Please try again.';
        }

        // Add timestamp to errors for tracking
        error.timestamp = new Date().toISOString();

        return Promise.reject(error);
    }
);

// Add method to check auth status
axiosInstance.isAuthenticated = () => {
    return !!localStorage.getItem('token');
};

// Add method to clear auth token
axiosInstance.clearAuth = () => {
    localStorage.removeItem('token');
};

export default axiosInstance;
