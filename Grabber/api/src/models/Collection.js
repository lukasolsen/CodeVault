const { Collection } = require("../database"); // Adjust the path based on your project structure

module.exports = {
  getCollections: function () {
    return Collection.find({}, { _id: 0 });
  },
  getCollection: function (identifier) {
    return Collection.findOne({ id: identifier }, { _id: 0 });
  },
  createCollection: function (collectionData) {
    const newCollection = new Collection(collectionData);
    return newCollection.save();
  },
  updateCollection: function (collectionData) {
    const { id, ...updateData } = collectionData;
    return Collection.updateOne({ id }, { $set: updateData });
  },
  deleteCollection: function (identifier) {
    return Collection.deleteOne({ id: identifier });
  },
  getScanInCollections: function (identifier) {
    return Collection.findOne({ scan_id: identifier }, { _id: 0 });
  },
};
