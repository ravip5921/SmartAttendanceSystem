<?php session_start(); ?>
<html>

<head>
    <title>Departments</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <link rel="stylesheet" href="../css/departStyle.css">
</head>

<body>
    <nav class="navbar">
        <div class="logo"><a href="departments.php">Smart Attendance</a></div>
        <div class="logOut-btn"><a href="../index.html">Log Out</a></div>
    </nav>
    <div class="bg-image">
        <div class="card-holder">
            <?php
            include 'connectToDb.php';
            $username = $_SESSION["username"];
            if (!$sqldb->select_db('sas')) 
            {
                die("not connected to database");
            }
            $getDepartmentsQuery = "SELECT name,dID from department WHERE 1";
            if($departments = $sqldb->query($getDepartmentsQuery))
            {
                if (mysqli_num_rows($departments) > 0)
                {
                
                    while ($departments_row = mysqli_fetch_assoc($departments)) 
                    {
                        $dID = $departments_row['dID'];
                        $departName = $departments_row['name'];       
                        ?>
                            <div class="card">
                                <div class="box">
                                    <a href="bct.php?dID=<?php echo $dID;?>" >
                                        <div class="text"><?php echo $departName?></div>                   
                                    </a>
                                </div>
                            </div>
                        <?php
                    }
                }
            }    
            else
            {
                echo "Error running fetch department query";
            }
            ?>
        </div>
    </div>
<footer>
    <span class="text1">Created By</span> <br>
    <span class="text2">Nikesh DC(PUL075BCT052) ,
        Ravi Pandey(PUL075BCT065) ,
        <br> Rohan Chhetry(PUL075BCT066) ,
        Yukta Bansal (PUL075BCT096)</span>
        <br> <span class="far fa-copyright"></span> <span class="text1">2022 All rights reserved.</span>
</footer>
</body>
</html>