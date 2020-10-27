const express = require('express')
const axios = require('axios')
const dotenv = require('dotenv').config()

const API_KEY = process.env.FOOTBALL_API_KEY
const PORT = process.env.PORT

let app = express()

app.get('/', (req, res) => {
    res.send('welcome')
})

app.listen(PORT, () => {
    console.log("Listening on port => " + PORT)
})