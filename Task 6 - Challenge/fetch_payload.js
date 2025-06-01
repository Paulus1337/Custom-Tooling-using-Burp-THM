await fetch("http://<insert_ip>/server.php", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*"
  },
  body: JSON.stringify({
    data: "<payload>"
  })
})
.then(res => res.json())
.then(res => console.log("Decrypted Response:", res));