import React, { useState, useEffect } from "react";
import axios from "axios";
import { API_BASE_URL } from "../config";
import Block from "./Block";
import { Link } from "react-router-dom";
import { Button } from "react-bootstrap";

const PAGE_LIMIT = 3;

const BlockChain = () => {
  const [blockchain, setBlockChain] = useState([]);
  const [blockchainlength, setBlockChainLength] = useState(0);
  useEffect(() => {
    fetchBlockchainBlocks({ start: 0, end: PAGE_LIMIT });
    axios
      .get(`${API_BASE_URL}/blockchain/length`)
      .then(res => setBlockChainLength(res.data));
  }, []);

  const buttonNumbers = [
    ...Array(Math.ceil(blockchainlength / PAGE_LIMIT)).keys()
  ];

  const fetchBlockchainBlocks = ({ start, end }) => {
    axios
      .get(`${API_BASE_URL}/blockchain/range?start=${start}&end=${end}`)
      .then(res => setBlockChain(res.data));
  };

  return (
    <div className="Blockchain">
      <Link to="/">Home</Link>
      <hr />
      <h3>Blockchain</h3>
      <div>
        {blockchain.map(block => (
          <Block key={block.hash} block={block} />
        ))}
      </div>
      <div>
        {buttonNumbers.map(number => {
          const start = number * PAGE_LIMIT;
          const end = (number + 1) * PAGE_LIMIT;
          return (
            <span
              key={number}
              onClick={() => fetchBlockchainBlocks({ start, end })}
            >
              <Button size="sm" variant="info">
                {number + 1}
              </Button>{" "}
            </span>
          );
        })}
      </div>
    </div>
  );
};

export default BlockChain;
