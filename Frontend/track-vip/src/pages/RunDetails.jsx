import { Box, VStack, Heading, Button, HStack, Slider, Wrap, 
    IconButton, Icon,
    Dialog, Portal, CloseButton,
    NumberInput
} from "@chakra-ui/react";
import { MdDownload, MdEdit, MdOutlineArrowLeft, MdOutlineArrowRight, MdZoomIn, MdZoomOut } from "react-icons/md";
import { FaArrowLeft, FaArrowRight, FaBackward, FaExpand, FaForward } from "react-icons/fa";
import { LineChart, Line, XAxis, YAxis, ReferenceLine, Tooltip, ResponsiveContainer } from "recharts";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import FrameView from "../components/FrameView";

function RunDetails() {
    const { id } = useParams()
    const [runDetails, setRunDetails] = useState({})
    const [velocityData, setVelocityData] = useState([])
    const [frameNumber, setFrameNumber] = useState(1)
    const [currentVelocity, setCurrentVelocity] = useState(0)
    const [xDomain, setXDomain] = useState([0, 1]);
    const [graphFreeze, setGraphFreeze] = useState(false)
    const [editAthlete, setEditAthlete] = useState(false)

    useEffect(() => {
        axios
            .get("http://localhost:8000/runs/" + id)
            .then((response) => {
                setRunDetails(response.data)
                const v = JSON.parse(response.data.velocity_data)
                setVelocityData(v.map((velocity, index) => ({
                    frame: index,
                    velocity: velocity[2]
                })))
                setXDomain([0, v.length])
            })
    }, []);

    useEffect(() => {
        const result = velocityData.find(d => d.frame === frameNumber);
        const v = result ? result.velocity : 0
        setCurrentVelocity(v)
    }, [frameNumber])

    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            if (!graphFreeze) {
                setFrameNumber(payload[0].payload.frame)
            }
            return (
            <div className="custom-tooltip">
                <p>Frame {payload[0].payload.frame}</p>
                <Heading size="md">Velocity: {payload[0].payload.velocity} m/s</Heading>
            </div>
            );
        }
        return null;
    };

    return (
        <Box p={4} color='#25283D'>
            <Heading size="3xl">Run: {id}</Heading>
            <HStack>
                <Heading size="xl">Athlete: </Heading>
                <Button variant="subtle">
                    {runDetails.athlete_id} <Icon size="sm"><MdEdit /></Icon>
                </Button>
            </HStack>
        
            <Wrap justify={"center"}>
                    <VStack minWidth={500} width="45%">
                        <p>Frame: {frameNumber} | Velocity: {currentVelocity.toFixed(5)} m/s</p>
                        <FrameView videoPath={"/videos/run1_pose_browser_iframe.mp4"} frameNumber={frameNumber} fps={60} />

                        <HStack width="100%">
                            <IconButton onClick={() => setFrameNumber(frameNumber - 1)} variant="subtle" size="sm"><FaBackward color="#25283D"/></IconButton>
                            <IconButton onClick={() => setFrameNumber(frameNumber + 1)} variant="subtle" size="sm"><FaForward color="#25283D"/></IconButton>

                            <Slider.Root width="100%" 
                            size="sm"
                            thumbAlignment="center"
                            max={velocityData.length}
                            value={[frameNumber]} 
                            onValueChange={(e) => setFrameNumber(e.value[0])}
                            >  
                                <Slider.Control>
                                    <Slider.Track>
                                    <Slider.Range bg="#25283D"/>
                                    </Slider.Track>
                                    <Slider.Thumbs />
                                </Slider.Control>
                            </Slider.Root>

                            <Dialog.Root size="cover" >
                                <Dialog.Trigger asChild>
                                    <IconButton variant="subtle" size="sm"><FaExpand color="#25283D"/></IconButton>
                                </Dialog.Trigger>
                                <Portal>
                                    <Dialog.Backdrop />
                                    <Dialog.Positioner>
                                    <Dialog.Content color="#25283D">
                                        <Dialog.Body alignItems={"center"} justifyItems={"center"} alignContent={"center"}>
                                            <VStack width={"80%"}>
                                                <HStack>
                                                    <Heading size="lg">Frame </Heading>
                                                    <NumberInput.Root value={frameNumber} onValueChange={(e) => setFrameNumber(e.valueAsNumber)} 
                                                        min={0} max={velocityData.length} width={70}>
                                                        <NumberInput.Control />
                                                        <NumberInput.Input />
                                                    </NumberInput.Root>
                                                    <Heading size="lg">Velocity: {currentVelocity.toFixed(5)} m/s</Heading>
                                                </HStack>
                                                <FrameView videoPath={"/videos/run1_pose_browser_iframe.mp4"} frameNumber={frameNumber} fps={60} />
                                            </VStack>
                                        </Dialog.Body>
                                        <Dialog.CloseTrigger asChild>
                                        <CloseButton size="sm" />
                                        </Dialog.CloseTrigger>
                                    </Dialog.Content>
                                    </Dialog.Positioner>
                                </Portal>
                            </Dialog.Root>

                        </HStack>
                        
                    </VStack>

                    <VStack minWidth={500} width="45%">                     
                        <ResponsiveContainer width={"100%"} height={"100%"}>
                        <LineChart data={velocityData} onClick={() => {setGraphFreeze(!graphFreeze)}}>
                            <XAxis 
                                dataKey="frame" 
                                domain={xDomain} 
                                type="number" 
                                allowDataOverflow
                                tickCount={10}
                                label={{ value: 'Frame', position: 'insideBottomRight', offset: -5 }} 
                            />
                            <YAxis label={{ value: 'Velocity (m/s)', angle: -90, position: 'insideLeft' }} />
                            <Tooltip position={{x: 100, y: 10}} content={<CustomTooltip />} />
                            <ReferenceLine x={frameNumber} />
                            <Line type="monotone" dataKey="velocity" stroke="#25283D" yAxisId={0} />
                        </LineChart>
                        </ResponsiveContainer>

                        <HStack>
                            <IconButton variant="subtle" onClick={() => setXDomain([xDomain[0] - 10, xDomain[1] + 10])}><MdZoomOut color="#25283D" /></IconButton>
                            <IconButton variant="subtle" onClick={() => setXDomain([xDomain[0] + 10, xDomain[1] - 10])}><MdZoomIn color="#25283D" /></IconButton>
                            <IconButton variant="subtle" onClick={() => setXDomain([xDomain[0] - 10, xDomain[1] - 10])}><MdOutlineArrowLeft color="#25283D" /></IconButton>
                            <IconButton variant="subtle" onClick={() => setXDomain([xDomain[0] + 10, xDomain[1] + 10])}><MdOutlineArrowRight  color="#25283D" /></IconButton>
                            <IconButton variant="subtle" onClick={() => setXDomain([0, velocityData.length])}>Reset</IconButton>
                            <IconButton variant="subtle" onClick={() => setXDomain([0, velocityData.length])}><MdDownload /></IconButton>
                        </HStack>
                    </VStack>
            </Wrap>
        </Box>
    );
}

export default RunDetails