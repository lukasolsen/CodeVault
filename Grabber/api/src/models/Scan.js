const { Scan } = require("../database"); // Adjust the path based on your project structure

module.exports = {
  getScans: function () {
    return Scan.find(
      {},
      {
        name: 1,
        description: 1,
        _id: 1,
      }
    );
  },
  getScan: function (identifier) {
    return Scan.findOne(
      { _id: identifier },
      { name: 1, description: 1, _id: 1, timestamp: 1 }
    );
  },
  createScan: function (scanData) {
    const newScan = new Scan(scanData);
    return newScan.save();
  },
  updateScan: function (scanData) {
    const { id, ...updateData } = scanData;
    return Scan.updateOne({ _id }, { $set: updateData });
  },
  deleteScan: function (identifier) {
    return Scan.deleteOne({ _id: identifier });
  },
  getAllScan: function (identifier) {
    return Scan.find({ _id: identifier }, { _id: 0 });
  },
};
