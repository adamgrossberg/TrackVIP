import { useState } from 'react';
import axios from "axios";
import { Box, Button, Input, HStack } from "@chakra-ui/react";
import { FormControl, FormLabel } from '@chakra-ui/form-control';

function CreateAthlete({ onCreateSuccess }) {
  const [newAthleteData, setNewAthleteData] = useState({
    id: '',
    first_name: '',
    last_name: '',
  });

  const handleAthleteDataChange = (e) => {
    const { name, value } = e.target;
    setNewAthleteData({ ...newAthleteData, [name]: value });
  };

  const postCreateAthlete = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(`http://127.0.0.1:8000/athletes/`, newAthleteData, {
        headers: { 'Content-Type': 'application/json' },
      });

      console.log('Response:', response.data);
      if (onCreateSuccess) {
        onCreateSuccess(); // 🚀 refresh the table
      }

      // Optional: Clear form after submission
      setNewAthleteData({
        id: '',
        first_name: '',
        last_name: '',
      });

    } catch (err) {
      console.error('Error:', err);
    } finally {
      console.log('Finished');
    }
  };

  return (
    <Box p={4} maxWidth="40vw" mx="auto" borderWidth="1px" borderRadius="md" bg="#25283D">
      <form onSubmit={postCreateAthlete}>
        <HStack spacing={4} alignItems="flex-end">
          <FormControl id="athleteId">
            <FormLabel color="white">Athlete ID</FormLabel>
            <Input
              type="text"
              name="id"
              value={newAthleteData.id}
              onChange={handleAthleteDataChange}
              placeholder="Create Athlete ID"
              height="40px"
            />
          </FormControl>
          <FormControl id="athleteFName">
            <FormLabel color="white">First Name</FormLabel>
            <Input
              type="text"
              name="first_name"
              value={newAthleteData.first_name}
              onChange={handleAthleteDataChange}
              placeholder="Athlete First Name"
              height="40px"
            />
          </FormControl>
          <FormControl id="athleteLName">
            <FormLabel color="white">Last Name</FormLabel>
            <Input
              type="text"
              name="last_name"
              value={newAthleteData.last_name}
              onChange={handleAthleteDataChange}
              placeholder="Athlete Last Name"
              height="40px"
            />
          </FormControl>
          <Button type="submit" bg="none" _hover={{ bg: "#43486b" }} height="42px">
            Submit
          </Button>
        </HStack>
      </form>
    </Box>
  );
}

export default CreateAthlete;
