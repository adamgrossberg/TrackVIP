//TODO
import { useState, useEffect } from 'react';
import axios from "axios";
import { Table } from "@chakra-ui/react";

function RunsTable() {
  const [runsData, setRunsData] = useState([])
  const [athleteNames, setAthleteNames] = useState({})
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
    })

  }, []);

  return (
      <Table.Root size="lg" variant="outline" interactive>
        <Table.Header>
          <Table.Row>
            <Table.ColumnHeader>Run ID</Table.ColumnHeader>
            <Table.ColumnHeader>Athlete</Table.ColumnHeader>
            <Table.ColumnHeader>Video Path</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {runsData.map((item) => (
            <Table.Row key={item.id} _hover={{bgColor: "#999999", cursor: "pointer"}}>
              <Table.Cell>{item.id}</Table.Cell>
              <Table.Cell>{athleteNames[item.athlete_id]}</Table.Cell>
              <Table.Cell>{item.video_path}</Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
    )
}

export default RunsTable;