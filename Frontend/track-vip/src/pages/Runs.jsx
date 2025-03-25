import { Box, Button, Input, Heading, HStack } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import ApiCall from "../components/apiCalls";
import CreateAthlete from "../components/createAthlete";
import RunsTable from "../components/runsTable";

function Runs() {

    return (
        <Box>
            <HStack padding={10} border={0} alignItems={"center"} margin={"auto"}>
                <Heading mb={6} color="white">Runs</Heading>
                <Button>New Run</Button>
            </HStack>
            
            <RunsTable />
        </Box>
    );
}

export default Runs