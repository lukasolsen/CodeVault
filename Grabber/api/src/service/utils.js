const generateId = () => {
  return Math.random().toString(36).slice(2, 10);
};

const bcrypt = require("bcryptjs");

const encryptPassword = (password) => {
  return bcrypt.hashSync(password, 10);
};

const comparePassword = (password, hash) => {
  return bcrypt.compareSync(password, hash);
};

module.exports = {
  generateId,
  encryptPassword,
  comparePassword,
};
