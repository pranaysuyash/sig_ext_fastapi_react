/**
 * Format error messages from various error types
 */
export const formatErrorMessage = (error) => {
    if (!error) {
        return 'An unknown error occurred';
    }

    // Handle axios error responses
    if (error.response?.data) {
        const { data } = error.response;

        // Handle structured error responses
        if (data.detail) {
            return typeof data.detail === 'string'
                ? data.detail
                : JSON.stringify(data.detail);
        }

        // Handle validation errors
        if (typeof data === 'object') {
            const messages = Object.entries(data)
                .map(([key, value]) => {
                    if (Array.isArray(value)) {
                        return `${key}: ${value.join(', ')}`;
                    }
                    return `${key}: ${value}`;
                });

            if (messages.length > 0) {
                return messages.join('\n');
            }
        }

        return JSON.stringify(data);
    }

    // Handle network errors
    if (error.request) {
        return 'Unable to connect to the server. Please check your internet connection.';
    }

    // Handle standard error objects
    return error.message || 'An unexpected error occurred';
};

/**
 * Log errors consistently
 */
export const logError = (error, context = '') => {
    const errorInfo = {
        timestamp: new Date().toISOString(),
        context,
        message: error.message,
        stack: error.stack,
    };

    if (error.response) {
        errorInfo.response = {
            status: error.response.status,
            statusText: error.response.statusText,
            data: error.response.data,
        };
    }

    if (error.config) {
        errorInfo.request = {
            url: error.config.url,
            method: error.config.method,
        };
    }

    console.error('Error:', errorInfo);

    // You could also send this to an error tracking service
    // if (process.env.NODE_ENV === 'production') {
    //     sendToErrorTrackingService(errorInfo);
    // }
};

/**
 * Check if error is an authentication error
 */
export const isAuthError = (error) => {
    return error.response?.status === 401;
};

/**
 * Check if error is a permission error
 */
export const isPermissionError = (error) => {
    return error.response?.status === 403;
};

/**
 * Get appropriate error message based on error type
 */
export const getErrorMessage = (error) => {
    if (isAuthError(error)) {
        return 'Please log in to continue';
    }

    if (isPermissionError(error)) {
        return 'You do not have permission to perform this action';
    }

    return formatErrorMessage(error);
};

/**
 * Handle file upload errors specifically
 */
export const handleUploadError = (error) => {
    if (error.response?.status === 413) {
        return 'File is too large. Please try a smaller file.';
    }

    if (error.response?.status === 415) {
        return 'File type not supported. Please use JPG or PNG files.';
    }

    return getErrorMessage(error);
};