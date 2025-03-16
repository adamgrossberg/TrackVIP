import { useState } from 'react';
import axios from "axios";
import { Box, Button, Input, Heading, VStack} from "@chakra-ui/react";
import {FormControl, FormLabel} from "@chakra-ui/form-control";

function CreateAthlete() {
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
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            console.log('Response:', response.data);
        } catch (err) {
            console.error('Error:', err);
        } finally {
            console.log('Finished');
        }
    };
    
    return (
        <Box p={4} maxWidth="600px" mx="auto" borderWidth="1px" borderRadius="md" justifyContent="center" alignItems="center">
        <Heading mb={4}>Create New Athlete</Heading>
        
        <form onSubmit={postCreateAthlete}>
            <VStack spacing={4} align="flex-start" justifyContent="center" alignItems="center">
            <FormControl id="athleteId">
                <FormLabel>Athlete ID</FormLabel>
                <Input
                type="text" 
                id="id"
                name="id"
                value={newAthleteData.id}
                onChange={handleAthleteDataChange}
                placeholder="Create Athlete ID"
                />
            </FormControl>
            <FormControl id="athleteFName">
                <FormLabel>First Name</FormLabel>
                <Input
                type="text" 
                id="first_name"
                name="first_name"
                value={newAthleteData.first_name}
                onChange={handleAthleteDataChange}
                placeholder="Athlete First Name"
                />
            </FormControl>
            <FormControl id="athleteLName">
                <FormLabel>Last Name</FormLabel>
                <Input
                type="text" 
                id="last_name"
                name="last_name"
                value={newAthleteData.last_name}
                onChange={handleAthleteDataChange}
                placeholder="Athlete Last Name"
                />
            </FormControl>
            <Button
                type="submit"
                colorScheme="teal"
                width="full"
            >
            Submit
            </Button>            
          </VStack>
        </form>
        </Box>
    );     
}

export default CreateAthlete;