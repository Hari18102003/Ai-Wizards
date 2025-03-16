"use client";
import { useRef, useState } from "react";
import { FaImage } from "react-icons/fa";
import Image from "next/image";
import axios from "axios";

export default function Home() {
  const fileInputRef = useRef(null);
  const [selectedLanguage, setSelectedLanguage] = useState("english");
  const [imagePreview, setImagePreview] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [pdfBlob, setPdfBlob] = useState(null); // Store the PDF response
  const [isProcessing, setIsProcessing] = useState(false); // Track translation state

  const handleClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
      setSelectedFile(file); // Store file for console log
      setPdfBlob(null); // Reset PDF when new file is uploaded
    }
  };

  const handleTranslate = async () => {
    if (selectedFile) {
      setIsProcessing(true); // Disable button and show "Processing..."

      try {
        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("language", selectedLanguage);

        const response = await axios.post("http://localhost:5000/upload", formData, {
          responseType: "blob",
        });

        setPdfBlob(response.data); // Store the received PDF blob
      } catch (error) {
        console.error("Error uploading file:", error);
      } finally {
        setIsProcessing(false); // Re-enable button after processing
      }
    }
  };

  const handleDownload = () => {
    if (!pdfBlob) return;

    const url = window.URL.createObjectURL(pdfBlob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "translated_text.pdf";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="w-full flex items-center p-[2rem]">
      {/* Left Section */}
      <div className="flex-1 mt-[4rem] flex items-center justify-center flex-col">
        <div className="relative w-[400px] h-[300px] rounded-2xl mb-5">
          <Image
            alt="picture"
            src={"/images/photo.png"}
            fill
            className="rounded-2xl"
          />
        </div>

        <h1 className="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 bg-clip-text text-transparent font-semibold text-xl font-poppins italic text-center">
          Translate handwritten text from images to digital.<br /> Upload, process, and download as a PDF!
        </h1>
      </div>

      {/* Right Section (Image Upload) */}
      <div className="flex-1 flex flex-col mt-[4rem] items-center justify-center space-y-6">
        {/* Image Upload Box */}
        <div
          className="w-[300px] h-[300px] relative flex items-center justify-center border-2 border-dashed border-gray-400 rounded-lg cursor-pointer hover:border-gray-600 overflow-hidden"
          onClick={handleClick}
        >
          {imagePreview ? (
            <Image src={imagePreview} alt="Uploaded" fill objectFit="cover" className="rounded-lg" />
          ) : (
            <FaImage className="text-gray-500 text-6xl" />
          )}
        </div>
        <input
          type="file"
          ref={fileInputRef}
          className="hidden"
          accept="image/*"
          onChange={handleFileChange}
        />

        {/* Language Selection Dropdown */}
        <select
          className="w-[300px] cursor-pointer p-3 border border-gray-400 rounded-lg text-gray-700"
          value={selectedLanguage}
          onChange={(e) => setSelectedLanguage(e.target.value)}
        >
          <option value="english">English</option>
          <option value="hindi">Hindi</option>
          <option value="tamil">Tamil</option>
          <option value="bengali">Bengali</option>
          <option value="kannada">Kannada</option>
          <option value="malayalam">Malayalam</option>
        </select>

        {/* Translate Button */}
        <button
          className={`w-[300px] cursor-pointer py-3 text-lg font-semibold text-white rounded-lg 
          bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 
          ${!selectedFile || isProcessing ? "opacity-50 cursor-not-allowed" : "hover:opacity-90"}`}
          disabled={!selectedFile || isProcessing}
          onClick={handleTranslate}
        >
          {isProcessing ? "Processing..." : "Translate"}
        </button>

        {/* Download PDF Button (Visible after translation) */}
        {pdfBlob && (
          <button
            className="w-[300px] cursor-pointer py-3 text-lg font-semibold text-white rounded-lg 
            bg-green-500 hover:bg-green-600"
            onClick={handleDownload}
          >
            Download PDF
          </button>
        )}
      </div>
    </div>
  );
}
