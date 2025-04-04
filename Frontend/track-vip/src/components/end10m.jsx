import React, { useRef } from "react";
import Draggable from "react-draggable";
import { TfiTarget } from "react-icons/tfi";

const DraggableEnd = ({ onDragEnd }) => {
  const nodeRef = useRef(null);
  const handleClick = (e) => {
    e.stopPropagation();
  };

  const handleDrag = (e, data) => {
    const Scale = 1920 / 711;
    const xRelativeToImage = ((691 + data.x) * Scale);
    const yRelativeToImage = ((200 - data.y) * Scale);
    if (onDragEnd) {
        onDragEnd(xRelativeToImage, yRelativeToImage);
      }
  }

  return (
    <Draggable bounds="parent" nodeRef={nodeRef} onDrag={handleDrag}>
        <div
            ref={nodeRef}
            style={{
            width: "40px",
            height: "40px",
            backgroundColor: "rgba(255, 0, 0, 0.5)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            borderRadius: "50%",
            cursor: "grab",
            position: "absolute",
            right: "0", // optional, for default position
            top: "50%", // optional
            transform: "translateY(-50%)",
            }}
            onClick={handleClick} // Stop click event from propagating,
        >
    <TfiTarget color="white" style={{ fontSize: "40px" }}/>
    </div>
    </Draggable>  
  );
};

export default DraggableEnd;
