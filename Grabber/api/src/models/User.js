const { User } = require("../database"); // Adjust the path based on your project structure

module.exports = {
  getUsers: function () {
    return User.find({}, { password: 0 }); // Exclude _id and password from the result
  },
  getUser: function (identifier) {
    return User.findOne({ _id: identifier }, { password: 0 }); // Exclude _id and password
  },
  getUserFromName: function (name) {
    return User.findOne({ name }, { password: 0 }); // Exclude _id and password
  },
  getUserFromEmail: function (email) {
    return User.findOne({ email }, { password: 0 }); // Exclude _id and password
  },
  verifyToken: function (user) {
    return new Promise((resolve, reject) => {
      if (!user) {
        reject({ message: "failure", status: "Unauthorized" });
      } else {
        // Check if the user exists
        User.findOne({ _id: user.id }, (err, row) => {
          if (err) {
            reject(err);
          }

          if (!row) {
            reject({ message: "failure", error: "Unauthorized" });
          }

          resolve({ message: "success", status: "Authorized" });
        });
      }
    });
  },
  createUser: function (userData) {
    const newUser = new User(userData);
    return newUser.save();
  },
  updateUser: function (userData) {
    const { id, ...updateData } = userData;
    return User.updateOne({ _id }, { $set: updateData });
  },
  deleteUser: function (identifier) {
    return User.deleteOne({ _id: identifier });
  },
  getUserPassword: function (identifier) {
    console.log("Identifier: ", identifier);
    return User.findOne({ _id: identifier }, { _id: 0, password: 1 });
  },
};
