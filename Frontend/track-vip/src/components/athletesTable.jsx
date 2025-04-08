import { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Button, Flex, Box } from '@chakra-ui/react';
import CreateAthlete from './createAthlete';

function AthletesTable() {
  const [athletes, setAthletes] = useState([]);
  const [selection, setSelection] = useState(null);
  const [tableKey, setTableKey] = useState(0);
  const [isRendered, setIsRendered] = useState(false);

  // Function to toggle the state
  const handleNewAthleteButtonClick = () => {
    setIsRendered(!isRendered);
  };

  const fetchAthletes = () => {
    axios.get("http://localhost:8000/athletes")
      .then((response) => {
        setAthletes(response.data);
      })
      .catch((error) => {
        console.error("Error fetching athletes:", error);
      });
  };

  useEffect(() => {
  fetchAthletes();
  }, []);

  const handleDelete = () => {
    if (selection !== null) {
      const conf = confirm(`Are you sure you want to delete athlete ${selection}? Press OK to confirm.`);
      if (conf) {
        axios.delete(`http://localhost:8000/athletes/${selection}`)
          .then(() => {
            const newArray = athletes.filter(athlete => athlete.id !== selection);
            setAthletes(newArray);
            setSelection("");
            setTableKey(tableKey + 1);
          })
          .catch((error) => {
            console.error("Error deleting athlete:", error);
          });
      }
    }
  };

  const handleRowClick = (id) => {
    if (selection === id) {
      setSelection(null);
    } else {
      setSelection(id);
    }
  };

  const sortBy = (key) => {
    const sorted = [...athletes].sort((a, b) => {
      const valA = typeof a[key] === "string" ? a[key].toLowerCase() : a[key];
      const valB = typeof b[key] === "string" ? b[key].toLowerCase() : b[key];
  
      if (valA < valB) return -1;
      else if (valA > valB) return 1;
      else return 0;
    });
    setAthletes(sorted);
    setTableKey(tableKey + 1);
  };

  return (
    <>
      <Flex gap={4} marginBottom={4}>
        <Button bg="#25283D" color="#f6f2f2" _hover={{ bg: "#43486b" }} onClick={handleDelete} disabled={selection === null}>
          Delete
        </Button>
        <Button bg="#25283D" color="#f6f2f2" _hover={{ bg: "#43486b" }} onClick={handleNewAthleteButtonClick}>
            {isRendered ? 'Hide' : 'New Athlete'}
        </Button>
      </Flex>
      {isRendered && (
        <Box width="100%" display="flex" justifyContent="flex-start" mb={4}>
            <Box maxWidth="500px" width="100%">
            <CreateAthlete onCreateSuccess={fetchAthletes} />
            </Box>
        </Box>
        )}
      <Table.Root size="lg" variant="outline" key={tableKey}>
        <Table.ColumnGroup>
          <Table.Column htmlWidth={'33%'} />
          <Table.Column htmlWidth={'33%'} />
          <Table.Column />
        </Table.ColumnGroup>

        <Table.Header bg="#25283D" color="#f5f2f2">
          <Table.Row>
            <Table.ColumnHeader
              color="#f5f2f2"
              _hover={{ cursor: "pointer" }}
              onClick={() => sortBy("id")}
            >
              ID
            </Table.ColumnHeader>
            <Table.ColumnHeader
              color="#f5f2f2"
              _hover={{ cursor: "pointer" }}
              onClick={() => sortBy("first_name")}
            >
              First Name
            </Table.ColumnHeader>
            <Table.ColumnHeader
              color="#f5f2f2"
              _hover={{ cursor: "pointer" }}
              onClick={() => sortBy("last_name")}
            >
              Last Name
            </Table.ColumnHeader>
          </Table.Row>
        </Table.Header>

        <Table.Body>
          {athletes.map((athlete) => (
            <Table.Row
              key={athlete.id}
              onClick={() => handleRowClick(athlete.id)}
              color="#25283D"
              bgColor={selection === athlete.id ? '#CBD5E0' : 'transparent'}
              _hover={{ bgColor: "#CBD5E0", cursor: "pointer" }}
            >
              <Table.Cell>{athlete.id}</Table.Cell>
              <Table.Cell>{athlete.first_name}</Table.Cell>
              <Table.Cell>{athlete.last_name}</Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
    </>
  );
}

export default AthletesTable;
