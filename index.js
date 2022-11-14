const express = require('express');
const multer  = require('multer');
const fs = require('fs');
const path = require("path");
const { exec } = require("child_process");
const { createDiffieHellmanGroup } = require('crypto');
const app = express();

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, '/tmp/');
    },
    filename: function (req, file, cb) {
      const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
      const extension = file.originalname.split('.').pop();
      cb(null, uniqueSuffix + '.' + extension);
    }
  });
  
const upload = multer({ storage: storage })

app.use(express.static('public'));
app.get('/', function (req, res) {
   res.sendFile( __dirname + "/" + "index.html" );
})

app.post('/stats', upload.single('uploaded_file'), function (req, res) {
   // req.file is the name of your file in the form above, here 'uploaded_file'
   // req.body will hold the text fields, if there were any 
   // console.log(req.file, req.body);

   if(req.file.mimetype != 'audio/mpeg') {
    console.log('Wrong filetype!');
    return;
   }

   exec("whisper " + req.file.path + " --output_dir ./tmp/" + " --model tiny" + " --language de --fp16 False", (error, stdout, stderr) => {
        if (error) {
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
        }
        console.log(`stdout: ${stdout}`);

        fs.readFile("." + req.file.path + ".txt", 'utf8', function(err, data) {
            if (err) throw err;
            console.log(data);
            res.send(data);
            // TODO send data as response!
        });

        cleanUp();
    });
});

async function cleanUp() {
    const directory = "./tmp";

    fs.readdir(directory, (err, files) => {
        if (err) throw err;
      
        for (const file of files) {
            if(file != '.gitkeep') {
                fs.unlink(path.join(directory, file), (err) => {
                    if (err) throw err;
                });
            }
        }
      });
}

var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port
   
   console.log("Example app listening at http://%s:%s", host, port)
})