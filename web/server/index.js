const express = require('express')
const path = require('path');
const app = express()
const PORT = 7900

const root = path.join(__dirname, '..', 'public')

app.use(express.static(root))

app.get('/', (req, res) => {
    res.sendFile('index.html')
})

app.listen(PORT, () => {
    console.log(`Web-UI server running on http://localhost:${PORT}`)
})