import { Box, Button, Input, Heading, VStack} from "@chakra-ui/react";
import ApiCall from "../components/apiCalls";
import CreateAthlete from "../components/createAthlete";
import CreateRun from "../components/videoUpload";
function HomePage() {

    return (
        <Box p={4}>
            <Heading mb={6} textAlign="center" color="#25283D">Home Page</Heading>
            <CreateRun />
            <ApiCall />
            <CreateAthlete />
            <CreateAthlete />
            <CreateAthlete />
        </Box>
    );
}

export default HomePage