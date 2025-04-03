//important -- this component is quite incomplete, will get fixed soon.

// also important - for this to work the input video must be in the input folder already

import { useState } from "react";
import { Box, Button, Input, VStack } from "@chakra-ui/react";
import { FormControl, FormLabel } from "@chakra-ui/form-control";
import axios from "axios";


const CreateRun = () => {
  const [runData, setRunData] = useState({
    id: "", // we will want to change this so that it is randomly generated by the backend and stored somewhere -> what do we want this id to represent?
    athlete_id: "",
    video_path: "",
    start_10m_coords_x: 0, //need to implement this as a ui selection tool with a first frame visual
    start_10m_coords_y: 0,
    end_10m_coords_x: 0,
    end_10m_coords_y: 0,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setRunData({
      ...runData,
      [name]: name.includes("coords") ? parseFloat(value) || 0 : value,
    });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Prepending './input/' to the video file name
      const videoPath = `./input/${file.name}`;
      setRunData({ ...runData, video_path: videoPath });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`http://127.0.0.1:8000/runs/`, runData);
      console.log("Success:", response.data); //need to find something more meaningful for this
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <Box p={4} maxWidth="400px" mx="auto" shadow="md" borderWidth="1px" borderRadius="md" bg="#25283D" justifyContent={"center"} alignItems={"center"}>
      <form onSubmit={handleSubmit}>
        <VStack spacing={4}>
          {Object.keys(runData).map((key) => (
            key !== "video_path" ? (
              <FormControl key={key}>
                <FormLabel textTransform="capitalize">{key.replace(/_/g, " ")}</FormLabel>
                <Input
                  type={key.includes("coords") ? "number" : "text"}
                  name={key}
                  value={runData[key]}
                  onChange={handleChange}
                  required
                />
              </FormControl>
            ) : (
              <FormControl key={key} justifyContent={"center"}>
                <FormLabel>Select Video File</FormLabel>
                <Input type="file" accept="video/*" onChange={handleFileChange} />
              </FormControl>
            )
          ))}
          <Button type="submit" width="full">
            Submit
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default CreateRun;
