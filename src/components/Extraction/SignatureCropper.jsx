// // // src/components/Extraction/SignatureCropper.jsx

// // import React, { useRef, useEffect } from 'react';
// // import Cropper from 'react-cropper';
// // import 'cropperjs/dist/cropper.css';

// // const SignatureCropper = ({ imageUrl, onRegionSelect }) => {
// //   const cropperRef = useRef(null);

// //   // Function to handle crop region change
// //   const handleCrop = () => {
// //     if (cropperRef.current) {
// //       const cropper = cropperRef.current.cropper;

// //       // Get the cropped area coordinates and dimensions
// //       const cropData = cropper.getData();
// //       const region = {
// //         x: cropData.x,
// //         y: cropData.y,
// //         width: cropData.width,
// //         height: cropData.height,
// //       };

// //       // Pass the selected region back to the parent
// //       onRegionSelect(region);
// //     }
// //   };

// //   useEffect(() => {
// //     console.log('Image URL in SignatureCropper:', imageUrl); // Debugging
// //   }, [imageUrl]);

// //   return (
// //     <div className="signature-cropper-container">
// //       {imageUrl ? (
// //         <Cropper
// //           src={imageUrl}
// //           style={{ height: 400, width: '100%' }}
// //           // Cropper settings
// //           initialAspectRatio={16 / 9}
// //           aspectRatio={0} // Allows free selection of crop area
// //           guides={true}
// //           viewMode={1}
// //           background={false}
// //           responsive={true}
// //           autoCropArea={1}
// //           checkOrientation={false}
// //           ref={cropperRef}
// //           onCropEnd={handleCrop} // Trigger handleCrop when cropping ends
// //         />
// //       ) : (
// //         <p>Loading image...</p>
// //       )}
// //     </div>
// //   );
// // };

// // export default SignatureCropper;

// // src/components/Extraction/SignatureCropper.jsx

// import React, { useRef, useEffect } from 'react';
// import Cropper from 'react-cropper';
// import 'cropperjs/dist/cropper.css';

// const SignatureCropper = ({ imageUrl, onRegionSelect }) => {
//   const cropperRef = useRef(null);

//   // Function to handle crop region selection
//   const handleCrop = () => {
//     if (cropperRef.current) {
//       const cropper = cropperRef.current.cropper;

//       // Extract coordinates and dimensions of the cropped area
//       const cropData = cropper.getData();
//       const region = {
//         x: cropData.x,
//         y: cropData.y,
//         width: cropData.width,
//         height: cropData.height,
//       };

//       // Send the selected region back to the parent component
//       onRegionSelect(region);
//     }
//   };

//   useEffect(() => {
//     console.log('Image URL in SignatureCropper:', imageUrl); // Debugging
//   }, [imageUrl]);

//   return (
//     <div className="signature-cropper-container">
//       {imageUrl ? (
//         <Cropper
//           src={imageUrl}
//           style={{ height: 400, width: '100%' }}
//           initialAspectRatio={16 / 9}
//           aspectRatio={0} // Allows free selection of crop area
//           guides={true}
//           viewMode={1}
//           background={false}
//           responsive={true}
//           autoCropArea={1}
//           checkOrientation={false}
//           ref={cropperRef}
//           onCropEnd={handleCrop} // Call handleCrop on cropping end
//         />
//       ) : (
//         <p>Loading image...</p>
//       )}
//     </div>
//   );
// };

// export default SignatureCropper;

import React, { useRef, useEffect, useState } from 'react';
import Cropper from 'react-cropper'; // Replace with your cropping library if different
import 'cropperjs/dist/cropper.css'; // Import any required CSS for Cropper.js

const SignatureCropper = ({ imageUrl, onRegionSelect }) => {
  const cropperRef = useRef(null);
  const [cropData, setCropData] = useState(null);

  useEffect(() => {
    if (cropData) {
      console.log('Crop data updated:', cropData);
      if (typeof onRegionSelect === 'function') {
        onRegionSelect(cropData);
      }
    }
  }, [cropData, onRegionSelect]);

  const handleCrop = () => {
    const cropper = cropperRef.current?.cropper;
    if (cropper) {
      const cropBoxData = cropper.getCropBoxData();
      const canvasData = cropper.getCanvasData();

      const region = {
        x: cropBoxData.left - canvasData.left,
        y: cropBoxData.top - canvasData.top,
        width: cropBoxData.width,
        height: cropBoxData.height,
      };

      console.log('Region selected in handleCrop:', region);
      setCropData(region);
    }
  };

  return (
    <div style={{ width: '100%' }}>
      <Cropper
        src={imageUrl}
        style={{ height: 400, width: '100%' }}
        initialAspectRatio={16 / 9}
        guides={true}
        ref={cropperRef}
        crop={handleCrop}
        viewMode={1}
        dragMode="crop"
      />
    </div>
  );
};

export default SignatureCropper;
