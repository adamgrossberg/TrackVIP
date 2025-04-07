import { Box, Button, Heading, HStack, Grid, GridItem } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import AthletesTable from "../components/athletesTable";

function Athletes() {
    const navigate = useNavigate();
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
                    <Heading mb={6} color="#25283D">Athletes</Heading>
                </GridItem>
                <GridItem colSpan={5}>
                    <AthletesTable />
                </GridItem>
            </Grid>
        </Box>
    );
}

export default Athletes