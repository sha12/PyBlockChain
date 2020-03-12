import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button } from "react-bootstrap";
import Transaction from "./Transaction";
import { API_BASE_URL, JS_SECONDS } from "../config";
import axios from "axios";
import history from "../history";

const POLL_INTERVAL = 10 * JS_SECONDS;

const TransactionPool = () => {
  const [transactions, setTransactions] = useState([]);

  const getTransactions = () => {
    axios.get(`${API_BASE_URL}/all-transactions`).then(res => {
      console.log("Transactions fetched: ", res.data);
      setTransactions(res.data);
    });
  };

  const fetchTransactionsToMine = () => {
    axios.get(`${API_BASE_URL}/blockchain/mine`).then(res => {
      console.log(res);
      alert("Success!!. A Block is Mined");
      history.push("/blockchain");
    });
  };

  useEffect(() => {
    getTransactions();
    const intervalId = setInterval(getTransactions, POLL_INTERVAL);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="TransactionPool">
      <Link to="/">Home</Link>
      <hr />
      <h4>Transaction Pool</h4>
      <div>
        {transactions.map(transaction => (
          <div key={transaction.id}>
            <hr />
            <Transaction transaction={transaction} />
          </div>
        ))}
      </div>
      <hr />
      {transactions.length ? (
        <Button onClick={fetchTransactionsToMine}>
          Mine a block with these Transactions
        </Button>
      ) : null}
    </div>
  );
};

export default TransactionPool;
