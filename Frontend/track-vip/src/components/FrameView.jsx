import { Box } from "@chakra-ui/react";
import { useRef, useEffect } from "react";

const FrameView = ({ videoPath, frameNumber, fps }) => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);

    useEffect(() => {
            const video = videoRef.current;
            const canvas = canvasRef.current;

            if (!video || !canvas) return;

            const ctx = canvas.getContext("2d");

            const drawFrame = () => {
                const { width, height } = canvas.getBoundingClientRect();
                canvas.width = width
                canvas.height = height
                ctx.drawImage(video, 0, 0, width, height);
            };

            const handleSeeked = () => {
                drawFrame();
            };

            const targetTime = frameNumber / fps;
            video.removeEventListener("seeked", handleSeeked);
            video.addEventListener("seeked", handleSeeked);
            video.currentTime = targetTime;

            return () => {
            video.removeEventListener("seeked", handleSeeked);
            };
    }, [frameNumber, fps]);

    return (
        <Box width="100%">
            <video
                ref={videoRef}
                src={videoPath}
                crossOrigin="anonymous"
                preload="auto"
                style={{display: "none"}}
            />
            <canvas ref={canvasRef} style={{ width: '100%', height: 'auto', display: "block"}} />
        </Box>
    );
}
export default FrameView