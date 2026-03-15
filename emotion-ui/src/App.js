import React, { useRef, useState } from "react";
import Webcam from "react-webcam";
import axios from "axios";
import "./App.css";
import ImageEmotion from "./components/ImageEmotion";

function App() {

  const webcamRef = useRef(null);
  const [page, setPage] = useState("home");
  const [emotion, setEmotion] = useState("");

  const capture = async () => {

    console.log("Capturing image...");

    const imageSrc = webcamRef.current.getScreenshot();

    const response = await axios.post("http://localhost:5000/detect", {
      image: imageSrc
    });

    setEmotion(response.data.emotion);
    setPage("result");

  };

  return (
    <div className="container">

      {page === "home" && (
        <div className="home">
          <h1>AI Emotion Detector</h1>
          <p>Welcome On Board 🚀</p>
          <p>Ready to detect your facial emotions?</p>

          <button onClick={() => setPage("camera")}>
            Use Camera
          </button>

          <button onClick={() => setPage("upload")}>
            Upload Image
          </button>
        </div>
      )}

      {page === "camera" && (
        <div className="camera">

          <h2>Look at the Camera</h2>

          <Webcam
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            width={500}
            height={400}
            videoConstraints={{
              facingMode: "user"
            }}
          />

          <br />

          <button onClick={capture}>
            Detect Emotion
          </button>

        </div>
      )}

      {page === "result" && (
        <div className="result">
          <h2>Your Emotion is</h2>

          <h1>{emotion}</h1>

          <button onClick={() => setPage("camera")}>
            Try Again
          </button>
        </div>
      )}

      {page === "upload" && (
        <div className="upload">
          <h2>Upload Image for Emotion Detection</h2>

          <ImageEmotion />

          <button onClick={() => setPage("home")}>
            Go Back
          </button>
        </div>
      )}

    </div>
  );
}

export default App;