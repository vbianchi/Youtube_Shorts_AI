const express = require('express');
const router = express.Router();
const shortsController = require('../controllers/shortsController');
const multer = require('multer');
const path = require('path');

// Configure file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, '../../public/uploads/'));
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const upload = multer({ storage: storage });

// Routes
router.post('/generate', shortsController.generateShort);
router.get('/status/:id', shortsController.getStatus);
router.get('/list', shortsController.listShorts);
router.get('/download/:id', shortsController.downloadShort);

module.exports = router;
