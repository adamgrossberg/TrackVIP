import { useState, useEffect } from "react";
import {
  Box,
  Button,
  Input,
  VStack,
  HStack,
  ProgressCircle,
  Alert,
  CloseButton,
} from "@chakra-ui/react";
import { FormControl, FormLabel } from "@chakra-ui/form-control";
import InputVideo from "./InputVideo";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const CreateRunForm = () => {
  const [runData, setRunData] = useState({
    id: "",
    athlete_id: "",
    run_name: "",
    video_path: "",
    start_10m_coords_x: 57,
    start_10m_coords_y: 540,
    end_10m_coords_x: 1866,
    end_10m_coords_y: 540,
  });

  const [athletes, setAthletes] = useState([]);
  const [runs, setRuns] = useState([]);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);

  const navigate = useNavigate();

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
  };

  const handleStartCoordsChange = (x, y) => {
    setRunData({
      ...runData,
      start_10m_coords_x: Math.round(x),
      start_10m_coords_y: Math.round(y),
    });
  };

  const handleEndCoordsChange = (x, y) => {
    setRunData({
      ...runData,
      end_10m_coords_x: Math.round(x),
      end_10m_coords_y: Math.round(y),
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    if (runs.some((run) => run.id === runData.id)) {
      setError("Run ID must be unique.");
      return;
    }

    setIsSubmitting(true);
    const videoPathWithPrefix = `./input/${runData.video_path}`;

    try {
      const newRun = { ...runData, video_path: videoPathWithPrefix };
      const response = await axios.post("http://127.0.0.1:8000/runs/", newRun);
      setSuccess(true);
    } catch (err) {
      console.error("Error submitting form:", err);
      setError("Failed to create run. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };


  return (
    <Box
      p={4}
      maxWidth="90vw"
      mx="auto"
      shadow="md"
      borderWidth="1px"
      borderRadius="md"
      bg="#25283D"
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
    >
      <form onSubmit={handleSubmit}>
        <VStack spacing={4} width="100%">
          {error && (
            <Alert status="error" borderRadius="md">
              <AlertIcon />
              <AlertTitle mr={2}>Error:</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
              <CloseButton position="absolute" right="8px" top="8px" onClick={() => setError("")} />
            </Alert>
          )}

          {success && (
            <Alert.Root status="success" borderRadius="md" flexDirection="column" alignItems="start">
              <HStack justify="space-between" width="100%">
                <Box>
                <Alert.Indicator />
                  <Alert.Title>Run Created!</Alert.Title>
                  <Alert.Description>
                    You can now view this run’s page.
                  </Alert.Description>
                </Box>
                <Button size="sm" colorScheme="teal" onClick={() => navigate(`/runs/${runData.id}`)}>
                  View Run
                </Button>
              </HStack>
            </Alert.Root>
          )}

          <HStack spacing={4} align="start" wrap="wrap">
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
            <InputVideo
              onFileSelect={(fileName) => setRunData({ ...runData, video_path: fileName })}
              onStartCoordsChange={handleStartCoordsChange}
              onEndCoordsChange={handleEndCoordsChange}
            />
          </FormControl>

          <Button type="submit" width="full" loading={isSubmitting} disabled={isSubmitting} loadingText="This may take a minute...">
            Submit
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default CreateRunForm;
