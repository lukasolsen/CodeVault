const mongoose = require("mongoose");
const dotenv = require("dotenv");
dotenv.config();

// Connect to MongoDB
mongoose.connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  //useCreateIndex: true, // Add this line to avoid deprecation warning
});

const Schema = mongoose.Schema;

// Users Schema
const userSchema = new Schema({
  name: { type: String },
  email: { type: String, unique: true },
  password: { type: String },
  role: { type: String },
});

// Collections Schema
const collectionSchema = new Schema({
  name: { type: String },
  description: { type: String },
  tags: { type: String },
  owner: { type: Schema.Types.ObjectId, ref: "User" }, // Reference to the User model

  scan: { type: Schema.Types.ObjectId, ref: "Scan" }, // Reference to the Scan model
});

// Scans Schema
const scanSchema = new Schema({
  name: { type: String },
  description: { type: String },
  tags: { type: String },
  browser: { type: String },
  discord: { type: String },
  network: { type: String },
  computer: { type: String },

  timestamp: { type: Date, default: Date.now },
});

// Create models
const User = mongoose.model("User", userSchema);
const Collection = mongoose.model("Collection", collectionSchema);
const Scan = mongoose.model("Scan", scanSchema);

// Export the models
module.exports = {
  User,
  Collection,
  Scan,
};
