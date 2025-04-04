import { useState, useEffect } from "react";
import { Box, Button, Input, Heading, VStack, HStack} from "@chakra-ui/react";
import CreateRunForm from "../components/createRunForm";

const CreateRunPage = () => {
    return (
      <Box p={4}>
        <Heading as="h2" size="lg" mb={2} color="#25283D" textAlign={'center'}>Create a New Run</Heading>
        <CreateRunForm />
      </Box>
    );
  };
  
  export default CreateRunPage;
