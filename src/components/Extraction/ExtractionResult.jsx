// src/components/Extraction/ExtractionResult.jsx

import React from 'react';
import { useSelector } from 'react-redux';

const ExtractionResult = () => {
  const { finalImage, loading, error } = useSelector(
    (state) => state.extraction
  );

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return (
      <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-800 rounded">
        <div className="flex items-start">
          <svg
            className="w-5 h-5 text-red-500 dark:text-red-400 mt-0.5 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <div>
            <h4 className="text-sm font-medium text-red-800 dark:text-red-400">
              Error
            </h4>
            <p className="mt-1 text-sm text-red-700 dark:text-red-300 whitespace-pre-line">
              {error}
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!finalImage) {
    return null;
  }

  return (
    <div className="mt-4 p-4 bg-green-50 dark:bg-green-900/10 border border-green-200 dark:border-green-800 rounded">
      <h3 className="text-xl font-semibold mb-4 text-primary dark:text-secondary">
        Extracted Signature
      </h3>
      <div className="relative w-full h-48 rounded overflow-hidden">
        <img
          src={finalImage}
          alt="Extracted Signature"
          className="object-contain w-full h-full"
        />
      </div>
    </div>
  );
};

export default ExtractionResult;
