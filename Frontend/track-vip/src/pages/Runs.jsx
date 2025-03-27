import { Box, Button, Heading, HStack, Grid, GridItem } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import ApiCall from "../components/apiCalls";
import CreateAthlete from "../components/createAthlete";
import RunsTable from "../components/runsTable";

function Runs() {

    return (
        <Box>
            <Grid
                templateRows="repeat(2, 1fr)"
                templateColumns="repeat(5, 1fr)"
                gap={4}
                h={200}
                padding={30}
            >
                <GridItem colSpan="4">
                    <Heading mb={6} color="#25283D">Runs</Heading>
                </GridItem>
                <GridItem textAlign={"right"}>
                    <Button bg="#25283D" color="#f6f2f2" marginTop={"auto"}>New Run</Button>
                </GridItem>
                <GridItem colSpan={5}>
                    <RunsTable />
                </GridItem>
            </Grid>
        </Box>
    );
}

export default Runs