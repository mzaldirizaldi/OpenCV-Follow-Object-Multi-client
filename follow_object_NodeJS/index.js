var net = require("net");
const http = require("http");
var Host = '192.168.18.229';
var Port = 9999;
var client = new net.Socket();
var result, a, b, e, f, g, h, X, Y, Azimuth, Elevasi;

client.connect(Port, Host, function (){
    console.log("Connected to " + Host + ":" + Port);
});

client.on('data', function (data) {
    a = data.toString();
    // a = "120X30Y40.12A60.8374B"
    result = a.split("X");
    if(result.length > 1) {
    b = a.split("Y");
    c = b[0];
    d = c.split("X");
    e = b[1];
    f = e.split("B");
    g = f[0];
    h = g.split("A");
    Azimuth = h[0];
    Elevasi = h[1];
    Y = d[1];
    X = result[0];
    console.log("Data received: " + a);
    // console.log("Data received: " + result);
    console.log("X: " + X);
    console.log("Y: " + Y);
    console.log("Azimuth: " + Azimuth + "°");
    console.log("Elevasi: " + Elevasi + "°");
}
    return X, Y, Azimuth, Elevasi;
});

client.on('close', function () { 
    console.log("Connection closed"); 
});

client.on('error', function (err) { 
    console.log("Error: " + err); 
});

http
.createServer((req, res) => {
    res.writeHead(200, {
        'Content-Type': 'text/html',
    });

    const url = req.url;
    res.write(`
    <head>
    <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0.25; URL=http://localhost:9000/">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
        <title>Follow Object</title>
    </head>
        <body style="background-color: #1A1A1D;">
            <div>
                <!-- navbar -->
                <nav class="navbar navbar-dark" style="background-color: #c3073f">
                    <div class="container-fluid">
                    <p class="navbar-brand mt-2 ms-2 text-uppercase" style="color: #1A1A1D;"> Follow <span class="fw-bold">Object</span></p>
                    </div>
                </nav>
                <!-- navbar end -->
                <!-- main interface -->
                <div class="container mt-5">
                    <!-- Container Koordinat Objek -->
                    <div class="container-fluid me-5 rounded-3 text-center" style="background-color: #c3073f;">
                    <h2 class="mt-3 text-uppercase" style="color: #1A1A1D;"><span class="fw-bold">Koordinat</span> Objek</h2></div>
                    <div class="container-fluid me-3 rounded-3 text-center" style="background-color: #6f2232;">
                        <h3 class="mt-3 text-uppercase" style="color: #1a1a1d;">X: <span class="fw-bold" style="color: white">${X}</span></h3>
                        <h3 class="mt-3 text-uppercase" style="color: #1a1a1d;">Y: <span class="fw-bold" style="color: white">${Y}</span></h3>
                    </div>
                    <div class="container-fluid me-3 rounded-3 mt-5 text-center" style="background-color: #c3073f;">
                    <h2 class="mt-3 text-uppercase" style="color: #1A1A1D;"><span class="fw-bold">Posisi</span> Servo</h2></div>
                    <div class="container-fluid mt-3 me-3 rounded-3 text-center" style="background-color: #6f2232;">
                        <h3 class="mt-3 text-uppercase" style="color: #1a1a1d;">Azimuth: <span class="fw-bold" style="color: white">${Azimuth}°</span></h3>
                        <h3 class="mt-3 text-uppercase" style="color: #1a1a1d;">Elevasi: <span class="fw-bold" style="color: white">${Elevasi}°</span></h3>
                    </div>
                    <!-- Container Koordinat Objek end-->
                </div>
                <!-- main interface end-->
            </div>
    
    
            <!-- JavaScript Bundle with Popper -->
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script>
        </body>
    `);
    res.end();
})
.listen(9000, () => {
    console.log(`Server is listening on port ${9000}..`)
});