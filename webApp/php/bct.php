<?php session_start(); ?>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>Smart Attendance</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <link rel="stylesheet" href="../css/bctStyle.css">
    <script src = "../js/functions.js"></script>
</head>

<body>
    <nav class="navbar">
        <div class="logo"><a href="departments.php">Smart Attendance</a></div>
        <div class="logOut-btn"><a href="../index.html">Log Out</a></div>
    </nav>
<div class="bg-image">
    <div class="bg">
    <div class="spacer">
        <div class ="search-form">
            <form method="POST" action="searchAttendance.php" id="SearchDataForm" onsubmit = "return compareDateFunc();">
                <label for="startDate">Start Date:</label>
                <input type="date" name="startDate" id="startDate" oninput=compareDateFunc()>
                <label for="startDate">End Date:</label>
                <input type="Date" name="endDate" id="endDate" oninput=compareDateFunc()>
                <?php include 'connectToDb.php';
                    if (!$sqldb->select_db('sas')) 
                    {
                        die("not connected to database");
                    }
                    $getSubjectQuery = "SELECT scode,name from subject";
                ?>
                <label for="subject">Subject:</label>
                <select name="subject">
                <?php
                    if($subjects = $sqldb->query($getSubjectQuery))
                    {
                        if (mysqli_num_rows($subjects) > 0)
                        {
                            while ($subjects_row = mysqli_fetch_assoc($subjects))
                            {
                                ?>
                                <option value ="<?php echo $subjects_row['scode'];?>" >
                                    <?php echo $subjects_row['name'];?>
                                </option>
                    <?php   }
                        }
                    }
                    else
                    {
                        echo "Error running query for fetching subjects";
                    }   ?>
                </select>
        </div>
        <?php
            $username = $_SESSION["username"];
            $dID = $_GET["dID"];
            $_SESSION["department"] = $dID;
            $getclassQuery = "SELECT cID,name from class WHERE dID = '$dID' and `sem`!=0";
            if($class = $sqldb->query($getclassQuery))
            {
                if (mysqli_num_rows($class) > 0)
                {
                    while ($class_row = mysqli_fetch_assoc($class)) 
                    {
                        // $dId = $class_row['dID'];
                        $className = $class_row['name'];
                        $cID = $class_row['cID'];
        ?>
        <div class="card-holder">
            <button class ="btn" name="class" value ="<?php echo $cID?>" on_pesss = "SearchDataForm.submit()"> <?php echo $className?></button>
        </div>            
                    <?php
                    }
                }
            }    
            else
            {
                echo "Error running fetch class query";
            }?>
            </form>
    </div>
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
