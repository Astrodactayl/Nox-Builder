const mongoose = require("mongoose")


const webhookSchema = new mongoose.Schema({
    webhook: String,
    rid: String
})

module.exports = mongoose.model("webhook", webhookSchema)