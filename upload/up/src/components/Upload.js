import React, { useState } from "react";
import Crop from "./Crop";

function Upload() {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFileSelect} />
      <br />
      {selectedFile && (
        <div>
          {" "}
          <div className="imgpr-con">
            <Crop img={URL.createObjectURL(selectedFile)} />
          </div>
        </div>
      )}
    </div>
  );
}
export default Upload;
