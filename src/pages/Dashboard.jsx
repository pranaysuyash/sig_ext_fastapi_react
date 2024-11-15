// // // // src/pages/Dashboard.jsx

// // // import React, { useState } from 'react';
// // // import ImageUploader from '../components/Extraction/ImageUploader';
// // // import SignatureCropper from '../components/Extraction/SignatureCropper';
// // // import ColorPicker from '../components/Extraction/ColorPicker';
// // // import ThresholdSlider from '../components/Extraction/ThresholdSlider';
// // // import { useDispatch, useSelector } from 'react-redux';
// // // import {
// // //   selectRegion,
// // //   processImage,
// // //   clearError,
// // // } from '../store/slices/extractionSlice';
// // // import ExtractionResult from '../components/Extraction/ExtractionResult';

// // // const Dashboard = () => {
// // //   const dispatch = useDispatch();
// // //   const [sessionId, setSessionId] = useState(null);
// // //   const [uploadedImageUrl, setUploadedImageUrl] = useState(null);
// // //   const [selectedRegion, setSelectedRegion] = useState(null);
// // //   const [color, setColor] = useState('#0000ff');
// // //   const [threshold, setThreshold] = useState(150);
// // //   const { finalImage, loading, error } = useSelector(
// // //     (state) => state.extraction
// // //   );

// // //   const handleUploadComplete = (result) => {
// // //     console.log('Upload result:', result);
// // //     setSessionId(result.id);
// // //     let imageUrl = result.file_path.startsWith('http')
// // //       ? result.file_path
// // //       : `http://127.0.0.1:8000${result.file_path}`;
// // //     console.log('Uploaded Image URL:', imageUrl);
// // //     setUploadedImageUrl(imageUrl);
// // //   };

// // //   const handleRegionSelect = (region) => {
// // //     console.log('Region selected:', region); // Log the selected region
// // //     setSelectedRegion(region); // Temporarily store the region in state
// // //   };

// // //   // New function to confirm the region selection
// // //   const handleConfirmRegion = () => {
// // //     if (selectedRegion) {
// // //       console.log('Confirmed region:', selectedRegion); // Log confirmation
// // //       dispatch(selectRegion({ session_id: sessionId, ...selectedRegion }));
// // //     } else {
// // //       alert('Please select a region before confirming.');
// // //     }
// // //   };

// // //   const handleProcessImage = async () => {
// // //     console.log('Selected Region:', selectedRegion);
// // //     console.log('Selected Color:', color);
// // //     console.log('Selected Threshold:', threshold);

// // //     if (selectedRegion && color && threshold) {
// // //       try {
// // //         const response = await dispatch(
// // //           processImage({
// // //             session_id: sessionId,
// // //             x1: selectedRegion.x,
// // //             y1: selectedRegion.y,
// // //             x2: selectedRegion.x + selectedRegion.width,
// // //             y2: selectedRegion.y + selectedRegion.height,
// // //             color,
// // //             threshold,
// // //           })
// // //         );
// // //         if (response.error) {
// // //           console.error('Error during extraction:', response.error);
// // //         }
// // //       } catch (error) {
// // //         console.error('Extraction process failed:', error);
// // //       }
// // //     } else {
// // //       alert('Please select a region, color, and threshold before processing.');
// // //     }
// // //   };

// // //   return (
// // //     <div className="min-h-screen bg-gray-900 text-white">
// // //       <div className="max-w-4xl mx-auto px-6 py-10 space-y-10">
// // //         <h1 className="text-5xl font-bold text-center mb-8 text-white">
// // //           Signature Extractor
// // //         </h1>

// // //         {/* Step 1: Upload Document */}
// // //         <section className="bg-gray-800 rounded-lg p-6 space-y-4">
// // //           <h2 className="text-2xl font-semibold text-center mb-4">
// // //             Step 1: Upload Document
// // //           </h2>
// // //           <ImageUploader onUpload={handleUploadComplete} />
// // //         </section>

// // //         {/* Step 2: Select Signature Area */}
// // //         {sessionId && uploadedImageUrl && (
// // //           <>
// // //             <hr className="border-gray-700 my-8" />
// // //             <section className="space-y-8">
// // //               <div className="bg-gray-800 rounded-lg p-6 space-y-4">
// // //                 <h2 className="text-2xl font-semibold text-center">
// // //                   Step 2: Select Signature Area
// // //                 </h2>
// // //                 <SignatureCropper
// // //                   imageUrl={uploadedImageUrl}
// // //                   onRegionSelect={handleRegionSelect}
// // //                 />

// // //                 {/* New Confirm Selection Button */}
// // //                 <div className="flex justify-center mt-4">
// // //                   <button
// // //                     onClick={handleConfirmRegion}
// // //                     className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-6 rounded-lg shadow-md transition duration-300"
// // //                   >
// // //                     Confirm Selection
// // //                   </button>
// // //                 </div>
// // //               </div>

// // //               {/* Step 3 and 4 */}
// // //               <div className="flex flex-col md:flex-row md:space-x-8 space-y-8 md:space-y-0">
// // //                 <div className="bg-gray-800 rounded-lg p-6 flex-1">
// // //                   <h2 className="text-xl font-semibold mb-4">
// // //                     Step 3: Choose Signature Color
// // //                   </h2>
// // //                   <ColorPicker onColorSelect={setColor} />
// // //                 </div>
// // //                 <div className="bg-gray-800 rounded-lg p-6 flex-1">
// // //                   <h2 className="text-xl font-semibold mb-4">
// // //                     Step 4: Adjust Threshold
// // //                   </h2>
// // //                   <ThresholdSlider
// // //                     initialValue={threshold}
// // //                     onThresholdSelect={setThreshold}
// // //                   />
// // //                   <p className="text-sm text-gray-400 mt-2">
// // //                     Threshold Value: {threshold}
// // //                   </p>
// // //                 </div>
// // //               </div>

// // //               {/* Extract Button */}
// // //               <div className="flex justify-center">
// // //                 <button
// // //                   onClick={handleProcessImage}
// // //                   className="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold py-3 px-8 rounded-lg shadow-md transition duration-300"
// // //                 >
// // //                   Extract Signature
// // //                 </button>
// // //               </div>
// // //             </section>
// // //           </>
// // //         )}

// // //         {/* Extraction Result */}
// // //         {finalImage && (
// // //           <>
// // //             <hr className="border-gray-700 my-8" />
// // //             <section className="bg-gray-800 rounded-lg p-6 space-y-4">
// // //               <h2 className="text-2xl font-semibold text-center">
// // //                 Extracted Signature
// // //               </h2>
// // //               <ExtractionResult finalImageUrl={finalImage} />
// // //             </section>
// // //           </>
// // //         )}

// // //         {/* Error Handling */}
// // //         {error && (
// // //           <div className="mt-4 p-4 bg-red-600 text-white rounded-lg shadow-lg">
// // //             <h3 className="font-semibold">Error:</h3>
// // //             <p>{error}</p>
// // //             <button
// // //               onClick={() => dispatch(clearError())}
// // //               className="mt-2 bg-red-800 hover:bg-red-700 text-white py-1 px-3 rounded"
// // //             >
// // //               Dismiss
// // //             </button>
// // //           </div>
// // //         )}

// // //         {/* Loading Indicator */}
// // //         {loading && (
// // //           <div className="mt-4 text-center">
// // //             <p>Loading...</p>
// // //           </div>
// // //         )}
// // //       </div>
// // //     </div>
// // //   );
// // // };

// // // export default Dashboard;

// // // src/pages/Dashboard.jsx

// // import React, { useState } from 'react';
// // import ImageUploader from '../components/Extraction/ImageUploader';
// // import SignatureCropper from '../components/Extraction/SignatureCropper';
// // import ColorPicker from '../components/Extraction/ColorPicker';
// // import ThresholdSlider from '../components/Extraction/ThresholdSlider';
// // import { useDispatch, useSelector } from 'react-redux';
// // import {
// //   selectRegion,
// //   processImage,
// //   clearError,
// // } from '../store/slices/extractionSlice';
// // import ExtractionResult from '../components/Extraction/ExtractionResult';

// // const Dashboard = () => {
// //   const dispatch = useDispatch();
// //   const [sessionId, setSessionId] = useState(null);
// //   const [uploadedImageUrl, setUploadedImageUrl] = useState(null);
// //   const [selectedRegion, setSelectedRegion] = useState(null);
// //   const [color, setColor] = useState('#0000ff');
// //   const [threshold, setThreshold] = useState(150);
// //   const { finalImage, loading, error } = useSelector(
// //     (state) => state.extraction
// //   );

// //   const handleUploadComplete = (result) => {
// //     console.log('Upload result:', result);
// //     setSessionId(result.id);
// //     const imageUrl = result.file_path.startsWith('http')
// //       ? result.file_path
// //       : `http://127.0.0.1:8000${result.file_path}`;
// //     console.log('Uploaded Image URL:', imageUrl);
// //     setUploadedImageUrl(imageUrl);
// //   };

// //   const handleRegionSelect = (region) => {
// //     console.log('Region selected in handleRegionSelect:', region);
// //     setSelectedRegion(region);
// //   };

// //   const confirmRegionSelection = () => {
// //     if (selectedRegion) {
// //       console.log('Confirmed region:', selectedRegion);
// //       dispatch(selectRegion({ session_id: sessionId, ...selectedRegion }));
// //     } else {
// //       alert('Please select a region before confirming.');
// //     }
// //   };

// //   const handleProcessImage = async () => {
// //     console.log('Selected Region:', selectedRegion);
// //     console.log('Selected Color:', color);
// //     console.log('Selected Threshold:', threshold);

// //     if (selectedRegion && color && threshold) {
// //       try {
// //         const response = await dispatch(
// //           processImage({
// //             session_id: sessionId,
// //             x1: selectedRegion.x,
// //             y1: selectedRegion.y,
// //             x2: selectedRegion.x + selectedRegion.width,
// //             y2: selectedRegion.y + selectedRegion.height,
// //             color,
// //             threshold,
// //           })
// //         );
// //         if (response.error) {
// //           console.error('Error during extraction:', response.error);
// //         }
// //       } catch (error) {
// //         console.error('Extraction process failed:', error);
// //       }
// //     } else {
// //       alert('Please select a region, color, and threshold before processing.');
// //     }
// //   };

// //   return (
// //     <div className="min-h-screen bg-gray-900 text-white">
// //       <div className="max-w-4xl mx-auto px-6 py-10 space-y-10">
// //         <h1 className="text-5xl font-bold text-center mb-8 text-white">
// //           Signature Extractor
// //         </h1>

// //         <section className="bg-gray-800 rounded-lg p-6 space-y-4">
// //           <h2 className="text-2xl font-semibold text-center mb-4">
// //             Step 1: Upload Document
// //           </h2>
// //           <ImageUploader onUpload={handleUploadComplete} />
// //         </section>

// //         {sessionId && uploadedImageUrl && (
// //           <>
// //             <hr className="border-gray-700 my-8" />
// //             <section className="space-y-8">
// //               <div className="bg-gray-800 rounded-lg p-6 space-y-4">
// //                 <h2 className="text-2xl font-semibold text-center">
// //                   Step 2: Select Signature Area
// //                 </h2>
// //                 <SignatureCropper
// //                   imageUrl={uploadedImageUrl}
// //                   onRegionSelect={handleRegionSelect}
// //                 />

// //                 <div className="flex justify-center mt-4">
// //                   <button
// //                     onClick={confirmRegionSelection}
// //                     className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-6 rounded-lg shadow-md transition duration-300"
// //                   >
// //                     Confirm Selection
// //                   </button>
// //                 </div>
// //               </div>

// //               <div className="flex flex-col md:flex-row md:space-x-8 space-y-8 md:space-y-0">
// //                 <div className="bg-gray-800 rounded-lg p-6 flex-1">
// //                   <h2 className="text-xl font-semibold mb-4">
// //                     Step 3: Choose Signature Color
// //                   </h2>
// //                   <ColorPicker onColorSelect={setColor} />
// //                 </div>
// //                 <div className="bg-gray-800 rounded-lg p-6 flex-1">
// //                   <h2 className="text-xl font-semibold mb-4">
// //                     Step 4: Adjust Threshold
// //                   </h2>
// //                   <ThresholdSlider
// //                     initialValue={threshold}
// //                     onThresholdSelect={setThreshold}
// //                   />
// //                   <p className="text-sm text-gray-400 mt-2">
// //                     Threshold Value: {threshold}
// //                   </p>
// //                 </div>
// //               </div>

// //               <div className="flex justify-center">
// //                 <button
// //                   onClick={handleProcessImage}
// //                   className="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold py-3 px-8 rounded-lg shadow-md transition duration-300"
// //                 >
// //                   Extract Signature
// //                 </button>
// //               </div>
// //             </section>
// //           </>
// //         )}

// //         {finalImage && (
// //           <>
// //             <hr className="border-gray-700 my-8" />
// //             <section className="bg-gray-800 rounded-lg p-6 space-y-4">
// //               <h2 className="text-2xl font-semibold text-center">
// //                 Extracted Signature
// //               </h2>
// //               <ExtractionResult finalImageUrl={finalImage} />
// //             </section>
// //           </>
// //         )}

// //         {error && (
// //           <div className="mt-4 p-4 bg-red-600 text-white rounded-lg shadow-lg">
// //             <h3 className="font-semibold">Error:</h3>
// //             <p>{error}</p>
// //             <button
// //               onClick={() => dispatch(clearError())}
// //               className="mt-2 bg-red-800 hover:bg-red-700 text-white py-1 px-3 rounded"
// //             >
// //               Dismiss
// //             </button>
// //           </div>
// //         )}

// //         {loading && (
// //           <div className="mt-4 text-center">
// //             <p>Loading...</p>
// //           </div>
// //         )}
// //       </div>
// //     </div>
// //   );
// // };

// // export default Dashboard;

// import React, { useState } from 'react';
// import ImageUploader from '../components/Extraction/ImageUploader';
// import SignatureCropper from '../components/Extraction/SignatureCropper';
// import ColorPicker from '../components/Extraction/ColorPicker';
// import ThresholdSlider from '../components/Extraction/ThresholdSlider';
// import { useDispatch, useSelector } from 'react-redux';
// import {
//   selectRegion,
//   processImage,
//   clearError,
// } from '../store/slices/extractionSlice';
// import ExtractionResult from '../components/Extraction/ExtractionResult';

// const Dashboard = () => {
//   const dispatch = useDispatch();
//   const [sessionId, setSessionId] = useState(null);
//   const [uploadedImageUrl, setUploadedImageUrl] = useState(null);
//   const [selectedRegion, setSelectedRegion] = useState(null);
//   const [color, setColor] = useState('#0000ff');
//   const [threshold, setThreshold] = useState(150);
//   const { finalImage, loading, error } = useSelector(
//     (state) => state.extraction
//   );

//   const handleUploadComplete = (result) => {
//     console.log('Upload result:', result); // Debug log
//     setSessionId(result.id);
//     const imageUrl = result.file_path.startsWith('http')
//       ? result.file_path
//       : `http://127.0.0.1:8000${result.file_path}`;
//     console.log('Uploaded Image URL:', imageUrl); // Debug log
//     setUploadedImageUrl(imageUrl);
//   };

//   const handleRegionSelect = (region) => {
//     console.log('Region selected in handleRegionSelect:', region); // Debug log
//     setSelectedRegion(region);
//   };

//   const confirmRegionSelection = () => {
//     console.log('Attempting to confirm region selection'); // Debug log
//     console.log('Current sessionId:', sessionId); // Debug log
//     console.log('Current selectedRegion:', selectedRegion); // Debug log
//     if (selectedRegion) {
//       console.log('Confirmed region:', selectedRegion); // Debug log
//       dispatch(selectRegion({ session_id: sessionId, ...selectedRegion }));
//     } else {
//       alert('Please select a region before confirming.');
//     }
//   };

//   const handleProcessImage = async () => {
//     console.log('Processing image with the following values:'); // Debug log
//     console.log('Selected Region:', selectedRegion); // Debug log
//     console.log('Selected Color:', color); // Debug log
//     console.log('Selected Threshold:', threshold); // Debug log

//     if (selectedRegion && color && threshold) {
//       try {
//         const response = await dispatch(
//           processImage({
//             session_id: sessionId,
//             x1: selectedRegion.x,
//             y1: selectedRegion.y,
//             x2: selectedRegion.x + selectedRegion.width,
//             y2: selectedRegion.y + selectedRegion.height,
//             color,
//             threshold,
//           })
//         );
//         console.log('Process Image Response:', response); // Debug log
//         if (response.error) {
//           console.error('Error during extraction:', response.error);
//         }
//       } catch (error) {
//         console.error('Extraction process failed:', error);
//       }
//     } else {
//       alert('Please select a region, color, and threshold before processing.');
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gray-900 text-white">
//       <div className="max-w-4xl mx-auto px-6 py-10 space-y-10">
//         <h1 className="text-5xl font-bold text-center mb-8 text-white">
//           Signature Extractor
//         </h1>

//         <section className="bg-gray-800 rounded-lg p-6 space-y-4">
//           <h2 className="text-2xl font-semibold text-center mb-4">
//             Step 1: Upload Document
//           </h2>
//           <ImageUploader onUpload={handleUploadComplete} />
//         </section>

//         {sessionId && uploadedImageUrl && (
//           <>
//             <hr className="border-gray-700 my-8" />
//             <section className="space-y-8">
//               <div className="bg-gray-800 rounded-lg p-6 space-y-4">
//                 <h2 className="text-2xl font-semibold text-center">
//                   Step 2: Select Signature Area
//                 </h2>
//                 <SignatureCropper
//                   imageUrl={uploadedImageUrl}
//                   onRegionSelect={handleRegionSelect}
//                 />

//                 <div className="flex justify-center mt-4">
//                   <button
//                     onClick={confirmRegionSelection}
//                     className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-6 rounded-lg shadow-md transition duration-300"
//                   >
//                     Confirm Selection
//                   </button>
//                 </div>
//               </div>

//               <div className="flex flex-col md:flex-row md:space-x-8 space-y-8 md:space-y-0">
//                 <div className="bg-gray-800 rounded-lg p-6 flex-1">
//                   <h2 className="text-xl font-semibold mb-4">
//                     Step 3: Choose Signature Color
//                   </h2>
//                   <ColorPicker onColorSelect={setColor} />
//                 </div>
//                 <div className="bg-gray-800 rounded-lg p-6 flex-1">
//                   <h2 className="text-xl font-semibold mb-4">
//                     Step 4: Adjust Threshold
//                   </h2>
//                   <ThresholdSlider
//                     initialValue={threshold}
//                     onThresholdSelect={setThreshold}
//                   />
//                   <p className="text-sm text-gray-400 mt-2">
//                     Threshold Value: {threshold}
//                   </p>
//                 </div>
//               </div>

//               <div className="flex justify-center">
//                 <button
//                   onClick={handleProcessImage}
//                   className="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold py-3 px-8 rounded-lg shadow-md transition duration-300"
//                 >
//                   Extract Signature
//                 </button>
//               </div>
//             </section>
//           </>
//         )}

//         {finalImage && (
//           <>
//             <hr className="border-gray-700 my-8" />
//             <section className="bg-gray-800 rounded-lg p-6 space-y-4">
//               <h2 className="text-2xl font-semibold text-center">
//                 Extracted Signature
//               </h2>
//               <ExtractionResult finalImageUrl={finalImage} />
//             </section>
//           </>
//         )}

//         {error && (
//           <div className="mt-4 p-4 bg-red-600 text-white rounded-lg shadow-lg">
//             <h3 className="font-semibold">Error:</h3>
//             <p>{error}</p>
//             <button
//               onClick={() => dispatch(clearError())}
//               className="mt-2 bg-red-800 hover:bg-red-700 text-white py-1 px-3 rounded"
//             >
//               Dismiss
//             </button>
//           </div>
//         )}

//         {loading && (
//           <div className="mt-4 text-center">
//             <p>Loading...</p>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// export default Dashboard;

import React, { useState, useEffect } from 'react';
import ImageUploader from '../components/Extraction/ImageUploader';
import SignatureCropper from '../components/Extraction/SignatureCropper';
import ColorPicker from '../components/Extraction/ColorPicker';
import ThresholdSlider from '../components/Extraction/ThresholdSlider';
import { useDispatch, useSelector } from 'react-redux';
import {
  selectRegion,
  processImage,
  clearError,
} from '../store/slices/extractionSlice';
import ExtractionResult from '../components/Extraction/ExtractionResult';

const Dashboard = () => {
  const dispatch = useDispatch();
  const [sessionId, setSessionId] = useState(null);
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [color, setColor] = useState('#0000ff');
  const [threshold, setThreshold] = useState(150);
  const { finalImage, loading, error } = useSelector(
    (state) => state.extraction
  );

  // Debug to see selectedRegion changes
  useEffect(() => {
    console.log('Updated selectedRegion:', selectedRegion);
  }, [selectedRegion]);

  const handleUploadComplete = (result) => {
    console.log('Upload result:', result);
    setSessionId(result.id);
    const imageUrl = result.file_path.startsWith('http')
      ? result.file_path
      : `http://127.0.0.1:8000${result.file_path}`;
    console.log('Uploaded Image URL:', imageUrl);
    setUploadedImageUrl(imageUrl);
  };

  const handleRegionSelect = (region) => {
    console.log('Region selected in handleRegionSelect:', region);
    setSelectedRegion(region); // Should update selectedRegion
  };

  const confirmRegionSelection = () => {
    console.log('Attempting to confirm region selection');
    console.log('Current sessionId:', sessionId);
    console.log('Current selectedRegion:', selectedRegion);
    if (selectedRegion) {
      console.log('Confirmed region:', selectedRegion);
      dispatch(selectRegion({ session_id: sessionId, ...selectedRegion }));
    } else {
      alert('Please select a region before confirming.');
    }
  };

  const handleProcessImage = async () => {
    console.log('Processing image with the following values:');
    console.log('Selected Region:', selectedRegion);
    console.log('Selected Color:', color);
    console.log('Selected Threshold:', threshold);

    if (selectedRegion && color && threshold) {
      try {
        const response = await dispatch(
          processImage({
            session_id: sessionId,
            x1: selectedRegion.x,
            y1: selectedRegion.y,
            x2: selectedRegion.x + selectedRegion.width,
            y2: selectedRegion.y + selectedRegion.height,
            color,
            threshold,
          })
        );
        console.log('Process Image Response:', response);
        if (response.error) {
          console.error('Error during extraction:', response.error);
        }
      } catch (error) {
        console.error('Extraction process failed:', error);
      }
    } else {
      alert('Please select a region, color, and threshold before processing.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="max-w-4xl mx-auto px-6 py-10 space-y-10">
        <h1 className="text-5xl font-bold text-center mb-8 text-white">
          Signature Extractor
        </h1>

        <section className="bg-gray-800 rounded-lg p-6 space-y-4">
          <h2 className="text-2xl font-semibold text-center mb-4">
            Step 1: Upload Document
          </h2>
          <ImageUploader onUpload={handleUploadComplete} />
        </section>

        {sessionId && uploadedImageUrl && (
          <>
            <hr className="border-gray-700 my-8" />
            <section className="space-y-8">
              <div className="bg-gray-800 rounded-lg p-6 space-y-4">
                <h2 className="text-2xl font-semibold text-center">
                  Step 2: Select Signature Area
                </h2>
                <SignatureCropper
                  imageUrl={uploadedImageUrl}
                  onRegionSelect={handleRegionSelect}
                />

                <div className="flex justify-center mt-4">
                  <button
                    onClick={confirmRegionSelection}
                    className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-6 rounded-lg shadow-md transition duration-300"
                  >
                    Confirm Selection
                  </button>
                </div>
              </div>

              <div className="flex flex-col md:flex-row md:space-x-8 space-y-8 md:space-y-0">
                <div className="bg-gray-800 rounded-lg p-6 flex-1">
                  <h2 className="text-xl font-semibold mb-4">
                    Step 3: Choose Signature Color
                  </h2>
                  <ColorPicker onColorSelect={setColor} />
                </div>
                <div className="bg-gray-800 rounded-lg p-6 flex-1">
                  <h2 className="text-xl font-semibold mb-4">
                    Step 4: Adjust Threshold
                  </h2>
                  <ThresholdSlider
                    initialValue={threshold}
                    onThresholdSelect={setThreshold}
                  />
                  <p className="text-sm text-gray-400 mt-2">
                    Threshold Value: {threshold}
                  </p>
                </div>
              </div>

              <div className="flex justify-center">
                <button
                  onClick={handleProcessImage}
                  className="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold py-3 px-8 rounded-lg shadow-md transition duration-300"
                >
                  Extract Signature
                </button>
              </div>
            </section>
          </>
        )}

        {finalImage && (
          <>
            <hr className="border-gray-700 my-8" />
            <section className="bg-gray-800 rounded-lg p-6 space-y-4">
              <h2 className="text-2xl font-semibold text-center">
                Extracted Signature
              </h2>
              <ExtractionResult finalImageUrl={finalImage} />
            </section>
          </>
        )}

        {error && (
          <div className="mt-4 p-4 bg-red-600 text-white rounded-lg shadow-lg">
            <h3 className="font-semibold">Error:</h3>
            <p>{error}</p>
            <button
              onClick={() => dispatch(clearError())}
              className="mt-2 bg-red-800 hover:bg-red-700 text-white py-1 px-3 rounded"
            >
              Dismiss
            </button>
          </div>
        )}

        {loading && (
          <div className="mt-4 text-center">
            <p>Loading...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
