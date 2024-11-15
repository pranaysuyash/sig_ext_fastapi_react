// src/components/Extraction/ImageUploader.jsx

import React, { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import axiosInstance from '../../utils/axiosInstance';

const ImageUploader = ({ onUpload }) => {
  const [uploading, setUploading] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [error, setError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const createPreview = (file) => {
    const preview = URL.createObjectURL(file);
    setPreviewUrl(preview);
  };

  const handleError = (error) => {
    console.error('ImageUploader Error:', error);
    setError('Failed to upload image. Please try again.');
    setUploadProgress(0);
  };

  const onDrop = useCallback(
    async (acceptedFiles) => {
      try {
        setError(null);
        setUploading(true);
        setUploadProgress(0);
        const file = acceptedFiles[0];
        if (!file) {
          throw new Error('No file selected');
        }
        createPreview(file);
        const formData = new FormData();
        formData.append('file', file);
        const response = await axiosInstance.post(
          '/extraction/upload/',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
            onUploadProgress: (progressEvent) => {
              const percentCompleted = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
              );
              setUploadProgress(percentCompleted);
            },
          }
        );
        onUpload(response.data);
        setUploadProgress(100);
      } catch (error) {
        handleError(error);
      } finally {
        setUploading(false);
      }
    },
    [onUpload]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
    },
    maxSize: 10 * 1024 * 1024,
    multiple: false,
    disabled: uploading,
  });

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold text-[#f3a340] mb-6">
        Upload Document
      </h2>
      {previewUrl && (
        <div className="mb-6">
          <div className="aspect-video bg-black/20 rounded-lg overflow-hidden">
            <img
              src={previewUrl}
              alt="Preview"
              className="w-full h-full object-contain"
            />
          </div>
        </div>
      )}
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 
          transition-all duration-200 ease-in-out
          ${isDragActive ? 'border-[#f3a340] bg-[#f3a340]/10' : 'border-[#f3a340]/50 hover:border-[#f3a340] hover:bg-[#f3a340]/5'}
          ${uploading ? 'opacity-50 pointer-events-none' : 'cursor-pointer'}
        `}
      >
        <input {...getInputProps()} disabled={uploading} />
        <div className="text-center">
          <p className="text-lg mb-2">
            {uploading
              ? 'Uploading...'
              : 'Drag & drop a document here, or click to select a file'}
          </p>
          <p className="text-sm text-gray-400">
            Supported formats: JPG, PNG (max 10 MB)
          </p>
        </div>
      </div>
      {(uploading || uploadProgress > 0) && (
        <div className="mt-4">
          <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-[#f3a340] transition-all duration-300 ease-out"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
          <p className="mt-2 text-center text-sm text-gray-600">
            {uploadProgress}% uploaded
          </p>
        </div>
      )}
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}
    </div>
  );
};

export default ImageUploader;
