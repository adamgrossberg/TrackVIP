import React from "react";
import { Flex, Text, Button } from "@chakra-ui/react";
import Logo from "./Logo";
const NavBar = () => {
  return (
    <Flex
      position="sticky"
      top="0"
      zIndex="10"
      bg="#25283D"
      w="100%"
      p={4}
      justify="space-between"
      align="center"
      >
      <Logo />
      <Flex>
        <Button colorScheme="teal" variant="outline" mr={4} color='white'
        _hover={{ bg: 'snow', color: '#25283D' }}>
          Home
        </Button>
        <Button colorScheme="teal" variant="outline" mr={4} color='white'
        _hover={{ bg: 'snow', color: '#25283D' }}>
          About
        </Button>
      </Flex>
    </Flex>
  );
};

export default NavBar;
