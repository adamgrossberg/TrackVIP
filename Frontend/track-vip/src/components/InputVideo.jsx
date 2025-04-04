import { useState, useRef } from "react";
import { Box, Input, Text } from "@chakra-ui/react";
import DraggableStart from "./start10m"; 
import DraggableEnd from "./end10m"; 

const InputVideo = ({ onFileSelect, onStartCoordsChange, onEndCoordsChange }) => {
  const [videoPreview, setVideoPreview] = useState(null);

  const videoRef = useRef(null);
  const videoContainerRef = useRef(null);

  // Handle file change and video preview
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onFileSelect(file.name);

      const videoURL = URL.createObjectURL(file);
      const video = document.createElement("video");
      video.src = videoURL;
      video.crossOrigin = "anonymous";
      video.onloadeddata = () => {
        video.currentTime = 0;
      };
      video.onseeked = () => {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        setVideoPreview(canvas.toDataURL("image/png"));
        URL.revokeObjectURL(videoURL);
      };
    }
  };

  // Update the start and end coordinates when the draggable component moves
  const handleStartCoordsChange = (x, y) => {
    onStartCoordsChange(x, y); // Pass coordinates to parent
  };

  const handleEndCoordsChange = (x, y) => {
    onEndCoordsChange(x, y); // Pass coordinates to parent
  };

  return (
    <Box
      ref={videoContainerRef}
      width="100%"
      height="400px"
      maxWidth="800px"
      aspectRatio="16/9"
      bg="gray.700"
      display="flex"
      alignItems="center"
      justifyContent="center"
      borderRadius="md"
      position="relative"
      overflow="hidden"
      cursor="pointer"
      onClick={() => videoRef.current.click()}
    >
      {videoPreview ? (
        <img src={videoPreview} alt="Video Preview" style={{ width: "100%" }} />
      ) : (
        <Text color="white">Select Video</Text>
      )}

      <Input
        type="file"
        accept="video/*"
        ref={videoRef}
        onChange={handleFileChange}
        style={{ display: "none" }}
      />

      {videoPreview && (
        <>
          <DraggableStart onDragEnd={handleStartCoordsChange} />
          <DraggableEnd onDragEnd={handleEndCoordsChange} />
        </>
      )}
    </Box>
  );
};

export default InputVideo;
