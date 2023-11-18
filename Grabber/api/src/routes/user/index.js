const express = require("express");
const router = express.Router();
const {
  getUser,
  getUserFromName,
  createUser,
  getUsers,
  getUserFromEmail,
  getUserPassword,
} = require("../../models/User");
const jwt = require("jsonwebtoken");
const { encryptPassword, comparePassword } = require("../../service/utils.js");

router.get("/current_user", async function (req, res) {
  console.log("Current user: ", req.user);
  if (!req.user || !req.user.id || req.user.type !== "user") {
    res.status(401).json({ error: "Unauthorized" });
    return;
  }

  try {
    /*const user = await User.findOne(
      { id: req.user.id },
      { __v: 0, password: 0 }
    );*/
    console.log("User id: ", req.user.id);
    const user = await getUser(req.user.id);

    if (!user) {
      res.status(401).json({ message: "failure", error: "Unauthorized" });
      return;
    }

    const customUser = {
      id: user.id,
      name: user.name,
      email: user.email,
      role: user.role,
    };

    res.json({
      message: "success",
      data: customUser,
    });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.post("/login", async function (req, res) {
  const body = req.body;
  const email = body.email;
  const password = body.password;

  try {
    //const user = await User.findOne({ email }, { __v: 0 });
    const user = await getUserFromEmail(email);

    const userPassword = await getUserPassword(user._id);

    if (!user || !comparePassword(password, userPassword.password)) {
      res.status(401).json({ error: "Unauthorized" });
      return;
    }

    res.json({
      message: "success",
      data: user,
      token: jwt.sign({ type: "user", id: user._id }, "secret", {
        expiresIn: "1d",
      }),
    });
    return;
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.post("/register", async function (req, res) {
  const body = req.body;
  const name = body.name;
  const email = body.email;
  const password = body.password;

  try {
    //const existingUser = await User.findOne({ name });
    const existingUser = await getUserFromName(name);

    if (existingUser) {
      res.status(401).json({ error: "User already exists" });
      return;
    }

    const encryptedPassword = encryptPassword(password);
    // const newUser = new User({
    //   name,
    //   email,
    //   password: encryptedPassword,
    //   role: "user",
    // });

    // await newUser.save();

    await createUser({
      name,
      email,
      password: encryptedPassword,
      role: "user",
    });

    res.json({
      message: "success",
    });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.get("/users", async function (req, res) {
  try {
    //const users = await User.find({}, { __v: 0, password: 0 });
    const users = await getUsers();

    res.json({
      message: "success",
      data: users,
    });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.get("/user/:id", async function (req, res) {
  const userId = req.params.id;

  try {
    //const user = await User.findOne({ id: userId }, { __v: 0, password: 0 });
    const user = await getUser(userId);

    if (!user) {
      res.status(404).json({ message: "User not found" });
      return;
    }

    res.json({
      message: "success",
      data: user,
    });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.post("/verify-token", async function (req, res) {
  if (!req.user) {
    res.status(200).json({ message: "failure", status: "Unauthorized" });
    return;
  }

  try {
    //const user = await User.findOne({ id: req.user.id });
    const user = await getUser(req.user.id);

    if (!user) {
      res.status(401).json({ message: "failure", error: "Unauthorized" });
      return;
    }

    res.status(200).json({ message: "success", status: "Authorized" });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

module.exports = router;
