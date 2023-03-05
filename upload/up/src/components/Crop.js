import React, { useState, useCallback } from "react";
import Cropper from "react-easy-crop";
import axios from "axios";
import getCroppedImg from "./cropImage";
import "./styles.css";
// Function to convert Blob URL to Image
function convertBlobToImage(blobUrl) {
  return new Promise((resolve, reject) => {
    // Fetch the Blob object from the URL
    fetch(blobUrl)
      .then((response) => response.blob())
      .then((blob) => {
        // Read the data from the Blob object and convert it to a data URL
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = () => {
          // Resolve with the converted data URL
          resolve(reader.result);
          var base64String = reader["result"];
          const req = async () => {
            const response = await axios.post("/upload", {
              image_data: base64String,
            });
            console.log(response.data);
            window.location.href = "/text";
          };
          req();
        };
      })
      .catch((error) => {
        // Reject with the error
        reject(error);
      });
  });
}

const Crop = (props) => {
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null);
  // eslint-disable-next-line
  const [croppedImage, setCroppedImage] = useState(null);
  // eslint-disable-next-line
  const onCropComplete = useCallback((croppedArea, croppedAreaPixels) => {
    setCroppedAreaPixels(croppedAreaPixels);
  }, []);
  const showCroppedImage = useCallback(async () => {
    try {
      const croppedImage = await getCroppedImg(
        props["img"],
        croppedAreaPixels,
        0
      );
      console.log("donee", { croppedImage });
      convertBlobToImage(croppedImage);
      setCroppedImage(croppedImage);
    } catch (e) {
      console.error(e);
    }
    // eslint-disable-next-line
  }, [croppedAreaPixels]);

  return (
    <div className="App">
      <div className="crop-container">
        <Cropper
          image={props["img"]}
          crop={crop}
          zoom={zoom}
          zoomSpeed={0.1}
          aspect={1 / 1.4}
          onCropChange={setCrop}
          onCropComplete={onCropComplete}
          onZoomChange={setZoom}
        />
      </div>
      <div>
        <br></br>
        <button onClick={showCroppedImage}>Click here</button>
      </div>
    </div>
  );
};

export default Crop;
