import React, { useRef } from "react";
import Draggable from "react-draggable";
import { TfiTarget } from "react-icons/tfi";

const DraggableStart = ({ onDragEnd }) => {
  const nodeRef = useRef(null);
  const handleClick = (e) => {
    e.stopPropagation();
  };

  const handleDrag = (e, data) => {
    const Scale = 1920 / 711;
    const xRelativeToImage = ((20 + data.x) * Scale);
    const yRelativeToImage = ((200 - data.y) * Scale);
    if (onDragEnd) {
        onDragEnd(xRelativeToImage, yRelativeToImage);
      }
  };

  return (
    <Draggable bounds="parent" nodeRef={nodeRef} onDrag={handleDrag}>
      <div
        ref={nodeRef}
        style={{
          width: "40px",
          height: "40px",
          backgroundColor: "rgba(52, 236, 27, 0.5)",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          borderRadius: "50%",
          cursor: "grab",
          position: "absolute",
          left: 0,
          top: "50%",
          transform: "translateY(-50%)",
        }}
        onClick={handleClick}
      >
    <TfiTarget color="white" style={{ fontSize: "40px" }}/>
      </div>
    </Draggable>
  );
};

export default DraggableStart;