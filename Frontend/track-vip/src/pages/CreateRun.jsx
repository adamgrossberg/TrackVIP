import { useState, useEffect } from "react";
import { Box, Button, Input, Heading, VStack} from "@chakra-ui/react";
import {FormControl, FormLabel} from "@chakra-ui/form-control";
import axios from "axios";

const CreateRunPage = () => {
  const [runData, setRunData] = useState({
    id: "",
    athlete_id: "",
    run_name: "",
    video_path: "",
  });
  
  const [athletes, setAthletes] = useState([]);
  const [runs, setRuns] = useState([]);
  const [error, setError] = useState("");

  // Fetch existing athletes and runs when the component mounts
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

  useEffect(() => {
    // Log athletes every time the athletes state changes
    console.log("Updated Athletes:", athletes);
  }, [athletes]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setRunData({
      ...runData,
      [name]: value,
    });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setRunData({ ...runData, video_path: file.name });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if runID is unique
    if (runs.some(run => run.id === runData.id)) {
      setError("Run ID must be unique.");
      return;
    }

    // Prepend './input/' to the video path
    const videoPathWithPrefix = `./input/${runData.video_path}`;

    try {
      const newRun = { ...runData, video_path: videoPathWithPrefix };
      const response = await axios.post("http://127.0.0.1:8000/runs/", newRun);
      console.log("Success:", response.data);
      // Handle success (e.g., navigate to another page or reset the form)
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  return (
    <Box p={4} maxWidth="400px" mx="auto" shadow="md" borderWidth="1px" borderRadius="md" bg="#25283D">
      <form onSubmit={handleSubmit}>
        <VStack spacing={4}>
          {error && <Text color="red.500">{error}</Text>}

          <FormControl>
            <FormLabel>Run ID</FormLabel>
            <Input
              type="text"
              name="id"
              value={runData.id}
              onChange={handleChange}
              required
            />
          </FormControl>
{/* need to change this to take in the full name of the athletes */}
          <FormControl>
            <FormLabel>Athlete</FormLabel>
            <select
                name="athlete_id"
                value={runData.athlete_id}
                onChange={handleChange}
                required
                style={{
                backgroundColor: "#2D3748", /* Select background color */
                color: "white", /* Select text color */
                border: "none",
                padding: "8px",
                borderRadius: "4px",
                }}
            >
                <option value="">Select an athlete</option>
                {athletes.map((athlete) => (
                <option key={athlete.id} value={athlete.id}>
                    {athlete.first_name}
                </option>
                ))}
            </select>
        </FormControl>

          <FormControl>
            <FormLabel>Run Name</FormLabel>
            <Input
              type="text"
              name="run_name"
              value={runData.run_name}
              onChange={handleChange}
              required
            />
          </FormControl>

          <FormControl>
            <FormLabel>Select Video File</FormLabel>
            <Input type="file" accept="video/*" onChange={handleFileChange} required />
          </FormControl>

          <Button type="submit" width="full">
            Submit
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default CreateRunPage;
