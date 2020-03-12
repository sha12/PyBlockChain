import React, { useState } from "react";
import { PY_MILLISECONDS } from "../config";
import Transaction from "./Transaction";
import { Button } from "react-bootstrap";

const ToggleTransaction = ({ block }) => {
  const [displayTransaction, setDisplayTransaction] = useState(false);
  const { data } = block;

  const toggleDisplayTransaction = () => {
    setDisplayTransaction(!displayTransaction);
  };

  if (displayTransaction) {
    return (
      <div>
        {data.map(transaction => (
          <div key={transaction.id}>
            <hr />
            <Transaction transaction={transaction} />
          </div>
        ))}
        <br />
        <Button variant="danger" size="sm" onClick={toggleDisplayTransaction}>
          Hide Details
        </Button>
      </div>
    );
  }

  return (
    <div>
      <br />
      <Button
        variant="info"
        style={{ fontSize: 20 }}
        onClick={toggleDisplayTransaction}
      >
        Show Details
      </Button>
    </div>
  );
};

const Block = ({ block }) => {
  const { timestamp, hash } = block;

  const hashDisplay = `${hash.substring(0, 20)}...`;
  const timestampDisplay = new Date(
    timestamp / PY_MILLISECONDS
  ).toLocaleString();

  return (
    <div className="Block">
      <div>Hash: {hashDisplay}</div>
      <div>Timestamp: {timestampDisplay}</div>
      <ToggleTransaction block={block} />
    </div>
  );
};

export default Block;
