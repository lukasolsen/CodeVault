const express = require("express");
const router = express.Router();
const grabber = require("./grabber.js");
const { getScans, getAllScan, getScan } = require("../../models/Scan.js");
const db = require("../../database.js");

router.use("/admin", grabber);

router.get("/scans", (req, res) => {
  console.log("Current user: ", req.user);
  if (!req.user || !req.user.id || req.user.type !== "user") {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }

  getScans(db).then((result) => {
    res.json({ message: "success", data: result });
  });
});

router.get("/scan/:id", (req, res) => {
  if (!req.user || !req.user.id || req.user.type !== "user") {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }

  const id = req.params.id;

  getScan(id).then((result) => {
    res.json({ message: "success", data: result });
  });
});

router.get("/scan/:id/attacks/browsers/pre", (req, res) => {
  if (!req.user || !req.user.id || req.user.type !== "user") {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }

  const id = req.params.id;

  getAllScan(id).then((result) => {
    if (!result[0]) {
      res.status(400).json({ error: "Scan not found" });
      return;
    }
    //console.log("Result: ", result);
    // We're now getting all data, filter out everything but browsers
    const browserData = JSON.parse(result[0].browser);
    //console.log("Browser data: ", browserData);
    // Looks like the json is not valid, even tho we parse it

    browserDataFormatted = Object.entries(browserData).map(
      ([browserKey, browser]) => {
        console.log("Browser: ", browser, "Browser key: ", browserKey);
        let data = {};

        Object.keys(browser).forEach((v) => {
          // Check the typeof a single result, if string JSON parse it, if not, leave it
          const typeOfResults = typeof browser[v]?.results[0];
          data[v] =
            typeOfResults === "string"
              ? JSON.parse(browser[v]?.results).length
              : browser[v]?.results?.length || 0;
        });

        return {
          name: browserKey,
          data: data,
        };
      }
    );
    const sortedBrowserData = browserDataFormatted.sort((a, b) => {
      return (
        Object.values(b.data).reduce((a, b) => a + b) -
        Object.values(a.data).reduce((a, b) => a + b)
      );
    });
    res.json({
      message: "success",
      data: sortedBrowserData,
    });
  });
});

router.get("/scan/:id/attacks/browser/:browser/:type", (req, res) => {
  if (!req.user || !req.user.id || req.user.type !== "user") {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }

  const id = req.params.id;
  const browser = req.params.browser;
  const type = req.params.type;

  getAllScan(id).then((result) => {
    if (!result[0]) {
      res.status(400).json({ error: "Scan not found" });
      return;
    }

    const browserData = JSON.parse(result[0].browser);

    res.json({
      message: "success",
      data: browserData[browser][type] || {},
    });
  });
});

router.get("/scan/:id/attacks/network/overview", (req, res) => {
  if (!req.user || !req.user.id || req.user.type !== "user") {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }

  const id = req.params.id;

  getAllScan(id).then((result) => {
    if (!result[0]) {
      res.status(400).json({ error: "Scan not found" });
      return;
    }

    //Only include the Interfaces, and Profiles.

    const networkData = JSON.parse(result[0].network);

    const filteredNetworkData = {
      interfaces: networkData.Interfaces,
      profiles: networkData.Profiles,
    };

    res.json({
      message: "success",
      data: filteredNetworkData || {},
    });
  });
});

router.get("/scan/:id/attacks/network/:type", (req, res) => {
  if (!req.user || !req.user.id || req.user.type !== "user") {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }

  const id = req.params.id;
  const type = req.params.type;

  getAllScan(id).then((result) => {
    if (!result[0]) {
      res.status(400).json({ error: "Scan not found" });
      return;
    }

    const networkData = JSON.parse(result[0].network);

    if (!networkData["More"]) {
      res.json({
        message: "success",
        data: {},
      });
      return;
    } else if (!networkData["More"][type]) {
      res.json({
        message: "success",
        data: {},
      });
      return;
    }

    res.json({
      message: "success",
      data: networkData["More"][type] || {},
    });
  });
});

router.get("/scan/:id/attacks/discord/overview", (req, res) => {
  if (!req.user || !req.user.id || req.user.type !== "user") {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }

  const id = req.params.id;

  getAllScan(id).then((result) => {
    console.log("Result: ", result[0].discord);
    if (!result[0]) {
      res.status(400).json({ error: "Scan not found" });
      return;
    }

    //Only include the Interfaces, and Profiles.

    const discordData = JSON.parse(result[0].discord);
    console.log("Discord data: ", discordData);

    res.json({
      message: "success",
      data: discordData || {},
    });
  });
});

module.exports = router;
