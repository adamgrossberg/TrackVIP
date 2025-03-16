import { Box, Button, Input, Heading, VStack} from "@chakra-ui/react";
import {FormControl, FormLabel} from "@chakra-ui/form-control";
import { useNavigate } from "react-router-dom";

function Login() {
    const navigate = useNavigate();
    
    const handleLogin = () => {
        navigate("/home")
    };
    return (
        <Box display="flex" justifyContent="center" alignItems="center" height="100vh" bg="none">

        <Box p={8} maxWidth="400px" borderWidth={1} borderRadius="lg" boxShadow="lg" bg="white">
            <Heading mb={6} textAlign="center" color="black">Login</Heading>
            <VStack spacing={4}>
            <FormControl id="email">
                <FormLabel color="grey">Email</FormLabel>
                <Input type="email" placeholder="Enter your email" />
            </FormControl>
            <FormControl id="password">
                <FormLabel color="grey">Password</FormLabel>
                <Input type="password" placeholder="Enter your password" />
            </FormControl>
            <Button colorScheme="blue" width="full" onClick={handleLogin}>
                Login
            </Button>
            </VStack>
        </Box>
        </Box>
    );
}

export default Login;