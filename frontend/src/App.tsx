import React from "react";
import {Routes, Route, Link} from "react-router-dom";
import Home from "./pages/Home";
import Work from "./pages/Work";

export default function App() {
    return (
        <div className="min-h-screen bg-gray-50 text-gray-800">
            <header className="bg-blue-600 text-white p-4">
                <Link to="/" className="text-lg font-bold">
                    ToolCheck
                </Link>
            </header>
            <main className="p-4">
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/work/:workId" element={<Work/>}/>
                </Routes>
            </main>
        </div>
    );
}
