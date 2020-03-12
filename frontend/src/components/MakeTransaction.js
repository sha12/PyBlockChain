import React, { useState, useEffect } from "react";
import { FormGroup, FormControl, Button } from "react-bootstrap";
import { API_BASE_URL } from "../config";
import axios from "axios";
import { Link } from "react-router-dom";
import history from "../history";

const MakeTransaction = () => {
  const [amount, setAmount] = useState(0);
  const [recipient, setRecipient] = useState("");
  const [frequentAddresses, setFrequentAddresses] = useState([]);

  const updateRecipient = event => {
    setRecipient(event.target.value);
  };

  const updateAmount = event => {
    setAmount(Number(event.target.value));
  };

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/frequent-addresses`)
      .then(res => setFrequentAddresses(res.data));
  }, []);

  const doTransaction = () => {
    axios
      .post(
        `${API_BASE_URL}/wallet/transaction`,
        JSON.stringify({
          recipient,
          amount
        }),
        {
          headers: {
            "Content-Type": "application/json"
          }
        }
      )
      .then(res => {
        console.log("Submitted Transaction successfully", res.data);
        alert("Transaction Submitted");
        history.push("/transaction-pool");
      });
  };

  return (
    <div className="ConductTransaction">
      <Link to="/">Home</Link>
      <hr />
      <h3>Make Transaction</h3>
      <br />
      <FormGroup className="transactionInputs">
        <FormControl
          width="5px"
          input="text"
          placeholder="recipient"
          value={recipient}
          onChange={updateRecipient}
        />
      </FormGroup>
      <FormGroup className="transactionInputs">
        <FormControl
          input="number"
          placeholder="Amount"
          value={amount}
          onChange={updateAmount}
        />
      </FormGroup>
      <div>
        <Button size="lg" variant="danger" onClick={doTransaction}>
          Send
        </Button>

        <br />
        {frequentAddresses.length ? <h4>Frequent Addresses</h4> : null}

        <div>
          {frequentAddresses.map(frequentAddress => (
            <span key={frequentAddress}>
              <u>{frequentAddress}</u>{" "}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MakeTransaction;
