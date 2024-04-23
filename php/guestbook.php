<!--#include virtual="/pages/header.html" -->
<?php
$config = require "../../config.php";
$conn = mysqli_connect($config['DB_ADDR'], $config['DB_USR'], $config['DB_PASSWD'], $config['DB_NAME']);

if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['name'];
    $message = $_POST['message'];

    $sql = "INSERT INTO " . $config['DB_NAME'] . " (name, message) VALUES ('$name', '$message')";
    mysqli_query($conn, $sql);

    header("Location: " . $_SERVER['PHP_SELF']);
    exit;
} else {
    $name = "";
    $message = "";
}

$sql = "SELECT * FROM " . $config['DB_NAME'];
$result = mysqli_query($conn, $sql);

echo "<p>Welcome to my guestbook, be free to leave a message !</p>";
echo "<br><br>";
echo "<form action='" . $_SERVER['PHP_SELF'] . "' method='post'>";
echo "<label for='name'>Name: </label>";
echo "<input type='text' name='name' value='" . $name . "' required>";
echo "<br><br>";
echo "<label for='message'>Message: </label>";
echo "<textarea name='message' required>" . $message . "</textarea><br><br>";
echo "<input type='submit' value='Submit'>";
echo "</form>";

echo "<br><br>";
echo "<table id='guestbook_table' border='1'>";
echo "<tr><th>Name</th><th>Message</th></tr>";
while ($row = mysqli_fetch_assoc($result)) {
    echo "<tr>";
    echo "<td id='guestbook_name'>" . htmlspecialchars($row['name'], ENT_QUOTES, 'UTF-8') . "</td>";
    echo "<td>" . htmlspecialchars($row['message'], ENT_QUOTES, 'UTF-8') . "</td>";
    echo "</tr>";
}
echo "</table>";

mysqli_close($conn);
?>
<!--#include virtual="/pages/footer.html" -->