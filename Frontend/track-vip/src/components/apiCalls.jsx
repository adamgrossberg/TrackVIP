//TODO
import { useState } from 'react';
import axios from "axios";
import { Box, Button, Input, Heading, VStack} from "@chakra-ui/react";
import {FormControl, FormLabel} from "@chakra-ui/form-control";

function ApiCall() {
    const [inputGet, setApiGetCall] = useState("");
    const [responseData, setResponseData] = useState(null);
    
    const handleGetInputChange = (event) => {
        setApiGetCall(event.target.value);
    };

    const getRequest = (e) => {
        e.preventDefault();
        axios
            .get(`http://127.0.0.1:8000/${inputGet}`)
            .then((response) => {
                setResponseData(response.data);
                console.log(response.data);  // Log the response data to the console
              })
            .catch(error => console.log(error));
    };
    
    return (
        <Box p={4} maxWidth="400px" mx="auto" borderWidth="1px" borderRadius="md" justifyContent="center" alignItems="center" bg="#25283D">
        <Heading mb={4} justifySelf={"center"}>API Call Test</Heading>
        
        <form onSubmit={getRequest}>
            <VStack spacing={4} align="flex-start" justifyContent="center" alignItems="center">
            <FormControl id="getCall">
                <FormLabel>Test FastApi Get Methods</FormLabel>
                <Input
                type="text" 
                value={inputGet}
                onChange={handleGetInputChange}
                placeholder="Input Api Get Call"
                />
            </FormControl>
            
            <Button colorScheme="teal" type="submit">
                Make API Call
            </Button>
            </VStack>
        </form>

        {responseData && (
            <Box mt={4}>
            <Heading size="md">Response Data:</Heading>
            <pre>{JSON.stringify(responseData, null, 2)}</pre>
            </Box>
        )}
        </Box>
  );
}

export default ApiCall;