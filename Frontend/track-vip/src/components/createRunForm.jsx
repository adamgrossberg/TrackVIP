import { useState, useEffect } from "react";
import { Box, Button, Input, Heading, VStack, HStack, Text } from "@chakra-ui/react";
import { FormControl, FormLabel } from "@chakra-ui/form-control";
import FileUpload from "./InputVideo";
import axios from "axios";

const CreateRunForm = () => {
    const [runData, setRunData] = useState({
        id: "",
        athlete_id: "",
        run_name: "",
        video_path: "",
        start_10m_coords_x: 0, //need to implement this as a ui selection tool with a first frame visual
        start_10m_coords_y: 0,
        end_10m_coords_x: 1000,
        end_10m_coords_y: 1000,
    });
  
    const [athletes, setAthletes] = useState([]);
    const [runs, setRuns] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchData = async () => {
        try {
            const athletesResponse = await axios.get("http://127.0.0.1:8000/athletes");
            const runsResponse = await axios.get("http://127.0.0.1:8000/runs");
            setAthletes(athletesResponse.data);
            setRuns(runsResponse.data);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
        };
        fetchData();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setRunData({ ...runData, [name]: value });
        console.log(runData)
    };

    // const handleFileChange = (e) => {
    //     const file = e.target.files[0];
    //     if (file) {
    //     setRunData({ ...runData, video_path: file.name });
    //     }
    // };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (runs.some(run => run.id === runData.id)) {
        setError("Run ID must be unique.");
        return;
        }

        const videoPathWithPrefix = `./input/${runData.video_path}`;

        try {
        const newRun = { ...runData, video_path: videoPathWithPrefix };
        const response = await axios.post("http://127.0.0.1:8000/runs/", newRun);
        console.log("Success:", response.data);
        } catch (error) {
        console.error("Error submitting form:", error);
        }
    };

    return (
        <Box p={4} maxWidth="90vw" mx="auto" shadow="md" borderWidth="1px" borderRadius="md" bg="#25283D" display="flex" flexDirection="column" alignItems="center" justifyContent="center">
        <form onSubmit={handleSubmit}>
            <VStack>
            <HStack spacing={4} align="start" wrap="wrap">
            {error && <Text color="red.500">{error}</Text>}

            <FormControl>
                <FormLabel>Run ID</FormLabel>
                <Input type="text" name="id" value={runData.id} onChange={handleChange} required />
            </FormControl>
            <FormControl>
                <FormLabel>Run Name</FormLabel>
                <Input type="text" name="run_name" value={runData.run_name} onChange={handleChange} required />
            </FormControl>
            <FormControl>
                <FormLabel>Athlete</FormLabel>
                <select
                name="athlete_id"
                value={runData.athlete_id}
                onChange={handleChange}
                required
                style={{
                    backgroundColor: "#2D3748",
                    color: "white",
                    border: "none",
                    padding: "8px",
                    borderRadius: "4px",
                }}
                >
                <option value="">Select an athlete</option>
                {athletes.map((athlete) => (
                    <option key={athlete.id} value={athlete.id}>
                    {`${athlete.first_name} ${athlete.last_name}`}
                    </option>
                ))}
                </select>
            </FormControl>
            </HStack>
            <FormControl>
                <FormLabel>Video Upload</FormLabel>
                <FileUpload onFileSelect={(fileName) => setRunData({ ...runData, video_path: fileName })} />
            </FormControl>

            <Button type="submit" width="full">Submit</Button>
            </VStack>
        </form>
    </Box>
    );
}
export default CreateRunForm;