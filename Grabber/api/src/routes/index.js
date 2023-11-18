const express = require("express");
const router = express.Router();

const user = require("./user/index.js");
const scan = require("./scan/index.js");

router.use("/user", user);
router.use("/scan", scan);

module.exports = router;
