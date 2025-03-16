import { Box, Button, Input, Heading, VStack} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import ApiCall from "../components/apiCalls";
function HomePage() {

    return (
        <Box p={4}>
            <Heading mb={6} textAlign="center" color="white">Home</Heading>
            <ApiCall />
        </Box>
    );
}

export default HomePage