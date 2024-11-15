export const ACCEPTED_IMAGE_TYPES = {
    'image/jpeg': ['.jpg', '.jpeg'],
    'image/png': ['.png']
};

export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

export const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export const validateImageFile = (file) => {
    if (!file) {
        return 'No file selected';
    }

    if (file.size > MAX_FILE_SIZE) {
        return `File size (${formatFileSize(file.size)}) exceeds the limit of ${formatFileSize(MAX_FILE_SIZE)}.`;
    }

    if (!Object.keys(ACCEPTED_IMAGE_TYPES).includes(file.type)) {
        return `File type "${file.type}" is not supported. Accepted types are: JPG, PNG`;
    }

    return null;
};

export const createFilePreview = (file) => {
    return URL.createObjectURL(file);
};

export const revokeFilePreview = (previewUrl) => {
    if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
    }
};

export const getFileExtension = (filename) => {
    return filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 2).toLowerCase();
};

export const isImageFile = (file) => {
    return Object.keys(ACCEPTED_IMAGE_TYPES).includes(file.type);
};