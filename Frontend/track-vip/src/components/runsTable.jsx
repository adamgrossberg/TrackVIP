import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import { Table, Button, Flex, Dialog, CloseButton, Portal, Select } from "@chakra-ui/react";

function RunsTable() {
  const [runsData, setRunsData] = useState([])
  const [athleteNames, setAthleteNames] = useState({})
  const [selection, setSelection] = useState("")
  const [selectedAthletes, setSelectedAthletes] = useState([])
  const [tableKey, setTableKey] = useState(0)

  useEffect(() => {
    axios
      .get("http://localhost:8000/runs")
      .then((response) => {
        setRunsData(response.data);
      })
    
    axios
      .get("http://localhost:8000/athletes")
      .then((response) => {
        const result = response.data.reduce((acc, item) => {
          acc[item.id] = `${item.first_name} ${item.last_name}`;
          return acc;
        }, {})
        setAthleteNames(result);
        setSelectedAthletes(Object.keys(result));
      })

  }, []);

  const navigate = useNavigate();

  const handleOpen = () => {
    if (selection !== "") {
      navigate('/runs/' + selection)
    }
  }

  const handleDelete = () => {
    if (selection !== "") {
      const conf = confirm("Are you sure you want to delete " + selection + "? Press OK to confirm.")
      if (conf) {
        axios.delete("http://localhost:8000/runs/" + selection)
        let newArray = runsData
        newArray.splice(runsData.findIndex((run) => run.id === selection), 1)
        setRunsData(newArray)
      }
      setTableKey(tableKey + 1)
    }
  }

  const handleEdit = () => {

  }

  const handleRowClick = (id) => {
    if (selection === id) {
      setSelection("")
    } else {
      setSelection(id)
    }
  }
  const handleRowDoubleClick = (id) => {
    navigate('/runs/' + id)
  }

  return (
      <>
        <Flex gap={4} marginBottom={4}>
          <Button bg="#25283D" color="#f6f2f2" onClick={handleOpen} disabled={selection === ""}>Open</Button>
          <Button bg="#25283D" color="#f6f2f2" onClick={handleDelete} disabled={selection === ""}>Delete</Button>
        </Flex>

        <Flex gap={4} marginBottom={4}>
        <Select.Root multiple width={300} color="#25283D" 
          value={selectedAthletes}
          onValueChange={(e) => {
            setSelectedAthletes(e.value)
          }}
        >
            <Select.HiddenSelect />
            <Select.Control>
              <Select.Trigger>
                <Select.ValueText>Filter by Athlete</Select.ValueText>
              </Select.Trigger>
              <Select.IndicatorGroup>
                <Select.Indicator />
                <Select.ClearTrigger />
              </Select.IndicatorGroup>
            </Select.Control>
            <Portal>
              <Select.Positioner>
                <Select.Content>
                  {Object.entries(athleteNames).map(([id, name]) => (
                    <Select.Item item={id} key={id} color="#25283D">
                      {name} ({id})
                      <Select.ItemIndicator />
                    </Select.Item>
                  ))}
                </Select.Content>
              </Select.Positioner>
            </Portal>
          </Select.Root>
        </Flex>

        <Table.Root size="lg" variant="outline" interactive key={tableKey}>
          <Table.ColumnGroup>
            <Table.Column htmlWidth={'33%'} />
            <Table.Column htmlWidth={'33%'} />
            <Table.Column />
          </Table.ColumnGroup>
          <Table.Header bg="#25283D" color="#f5f2f2">
            <Table.Row>
              <Table.ColumnHeader color="#f5f2f2" _hover={{cursor: "pointer"}} onClick={() => {
                setRunsData(runsData.sort((a, b) => {
                  if (a.id < b.id) {
                    return -1;
                  } else {
                    return 1;
                  }
                }))
                setTableKey(tableKey + 1)
              }}>Run ID</Table.ColumnHeader>
              <Table.ColumnHeader color="#f5f2f2" _hover={{cursor: "pointer"}} onClick={() => {
                setRunsData(runsData.sort((a, b) => {
                  if (athleteNames[a.athlete_id] < athleteNames[b.athlete_id]) {
                    return -1;
                  } else if (athleteNames[a.athlete_id] > athleteNames[b.athlete_id]) {
                    return 1;
                  } else {
                    return 0;
                  }
                }))
                setTableKey(tableKey + 1)  
              }}>Athlete</Table.ColumnHeader>
              <Table.ColumnHeader color="#f5f2f2">Video Path</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {runsData.filter(run => selectedAthletes.includes(run.athlete_id)).map((item) => (
              <Table.Row key={item.id} 
                onClick={() => handleRowClick(item.id)}
                onDoubleClick={() => handleRowDoubleClick(item.id)} 
                color="#25283D" 
                bgColor={selection === item.id ? '#CBD5E0' : 'transparent'} 
                _hover={{bgColor: "#CBD5E0", cursor: "pointer"}}
              >
                <Table.Cell>{item.id}</Table.Cell>
                <Table.Cell>{athleteNames[item.athlete_id]}</Table.Cell>
                <Table.Cell>{item.video_path}</Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table.Root>
      </>
    )
}

export default RunsTable;