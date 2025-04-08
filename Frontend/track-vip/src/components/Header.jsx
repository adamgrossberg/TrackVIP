import {React} from "react";
import { useNavigate } from "react-router-dom";
import { Flex, Text, Button } from "@chakra-ui/react";
import Logo from "./Logo";
const NavBar = () => {
  const navigate = useNavigate();

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
      <Button bg="none" color="#f6f2f2" onClick={() => navigate('/runs')}><Logo /></Button>
      <Flex>
        <Button variant="subtle" bg={"none"}  _hover={{ bg: "#43486b" }} color="#f6f2f2" onClick={() => navigate('/runs')}>
          Runs
        </Button>
        <Button variant="subtle" bg={"none"} _hover={{ bg: "#43486b" }} color="#f6f2f2" onClick={() => navigate('/athletes')}>
          Athletes
        </Button>
        <Button variant="subtle" bg={"none"} _hover={{ bg: "#43486b" }} color="#f6f2f2" onClick={() => navigate('/runs')}>
          About
        </Button>
      </Flex>
    </Flex>
  );
};

export default NavBar;
