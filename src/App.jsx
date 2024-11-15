// // // src/App.jsx
// // import React from 'react';
// // import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// // import Navbar from './components/Layout/Navbar';
// // import Home from './pages/Home';
// // import Login from './pages/Login';
// // import Register from './pages/Register';
// // import Dashboard from './pages/Dashboard';
// // import NotFound from './pages/NotFound';
// // import ProtectedRoute from './components/Common/ProtectedRoute';
// // import './App.css';

// // function App() {
// //   return (
// //     <Router>
// //       <div className="flex flex-col min-h-screen">
// //         <Navbar />
// //         <div className="flex-grow">
// //           <Routes>
// //             <Route path="/" element={<Home />} />
// //             <Route path="/login" element={<Login />} />
// //             <Route path="/register" element={<Register />} />
// //             <Route
// //               path="/dashboard"
// //               element={
// //                 <ProtectedRoute>
// //                   <Dashboard />
// //                 </ProtectedRoute>
// //               }
// //             />
// //             <Route path="*" element={<NotFound />} />
// //           </Routes>
// //         </div>
// //       </div>
// //     </Router>
// //   );
// // }

// // export default App;

// // src/App.js
// import React from 'react';
// import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import Navbar from './components/Layout/Navbar';
// import Home from './pages/Home';
// import Login from './pages/Login';
// import Register from './pages/Register';
// import Dashboard from './pages/Dashboard';
// import NotFound from './pages/NotFound';
// import ProtectedRoute from './components/Common/ProtectedRoute';
// import './index.css';

// function App() {
//   return (
//     <Router>
//       <div className="flex flex-col min-h-screen">
//         <Navbar />
//         <div className="flex-grow">
//           <Routes>
//             <Route path="/" element={<Home />} />
//             <Route path="/login" element={<Login />} />
//             <Route path="/register" element={<Register />} />
//             <Route
//               path="/dashboard"
//               element={
//                 <ProtectedRoute>
//                   <Dashboard />
//                 </ProtectedRoute>
//               }
//             />
//             <Route path="*" element={<NotFound />} />
//           </Routes>
//         </div>
//       </div>
//     </Router>
//   );
// }

// export default App;

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Layout/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import NotFound from './pages/NotFound';
import ProtectedRoute from './components/Common/ProtectedRoute';
import './index.css';

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <div className="flex-grow">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard/*"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
