import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { API_BASE_URL } from "../config";

function App() {
  const [walletDetails, setWalletDetails] = useState({});

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/wallet/details`)
      .then(res => setWalletDetails(res.data));
  }, []);

  return (
    <div className="App">
      <h3>PyBlockChain</h3>
      <br />
      <Link to="/blockchain">Blockchain</Link>
      <Link to="/make-transaction">Make Transaction</Link>
      <Link to="/transaction-pool">Transaction Pool</Link>
      <br />
      <div className="WalletInfo">
        <div>Address: {walletDetails.address}</div>
        <div>Balance: {walletDetails.balance}</div>
      </div>
    </div>
  );
}

export default App;
