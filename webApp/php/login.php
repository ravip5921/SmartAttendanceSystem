<?php session_start(); ?>
<html>

<head>
    <title>Login</title>
</head>

<body>
    <?php
    include 'connectToDb.php';

    $username = $_POST["username"];
    $password = $_POST["password"];

    if($username =="" || $password == "")
    {
         ?>
        <script>
        alert("Username or password empty!");
        </script>
        <?php
        header("Refresh:0;url=../index.html");
        
    }
    else
    {

        if (!$sqldb->select_db('sas')) {
            die("not connected to database");
        }
        $getUserPWquery = "SELECT userName, password from admin WHERE userName= '$username'";
        $credentials = $sqldb->query($getUserPWquery);

        if ($vals_row = mysqli_fetch_assoc($credentials)) 
        {
            $name = $vals_row['username'];
            $password = $vals_row['password'];
            $_SESSION["username"] =$username;
            header("Location: ../php/departments.php");
                    
        } 
        else 
        {
            ?>
            <script>
            alert("Username or password incorrect!")
            </script><?php
        }
    }
?>
</body>
</html>