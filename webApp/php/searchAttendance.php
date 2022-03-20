<?php session_start(); ?>
<html>

<head>
    <title>Departments</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <link rel="stylesheet" href="../css/searchStyle.css">
    <script src = "../js/functions.js"></script>
</head>
<body>
    <div class="bg-image">
        <div class="bg">
            <?php
            include 'connectToDb.php';
            $dID = $_SESSION["department"];
            if (!$sqldb->select_db('sas')) 
            {
                die("not connected to database");
            }
            $startDate = $_POST["startDate"];
            $endDate = $_POST["endDate"];
            $diff = abs(strtotime($endDate) - strtotime($startDate));
            $days = floor($diff / (60*60*24));
            
            $subject = $_POST["subject"];
            $cID = $_POST["class"];

            $individualAttendanceRecordQuery = 'SELECT sID, name, sum(presence) as presentDays FROM record INNER JOIN student USING (sID) WHERE aID IN (';

            $getAttendanceQuery ="SELECT aID FROM attendance WHERE scode = '$subject' AND DATE(time) >= '$startDate' AND DATE(time) <= '$endDate' AND cID = '$cID'";
            if ($attendanceRecords = $sqldb->query($getAttendanceQuery))
            {
                if (mysqli_num_rows($attendanceRecords) > 0)
                    {
                        $aID = mysqli_fetch_assoc($attendanceRecords);
                        $aID = $aID['aID'];
                        $individualAttendanceRecordQuery.="'$aID'";

                        while ($aID = mysqli_fetch_assoc($attendanceRecords))
                        {
                            $aID = $aID['aID'];
                            $individualAttendanceRecordQuery.=",'$aID'";
                        }
                        $individualAttendanceRecordQuery.=") GROUP BY student.sID";
                    }
                if ($individualAttendanceRecords = $sqldb->query($individualAttendanceRecordQuery))
                {
                    ?>
                    <h2 class="dateDisplay" style="color: white; margin-left:1%;">
                        <?php 
                            echo "Total Days = $days";   
                        ?>
                    </h2>
                    <table class = "styled-table" id="Attendance_Data">
                        <tr class="top">
                            <th>Name</th>
                            <th>Roll Number</th>
                            <th>Present Days</th>
                        </tr>
                    <?php
                    while($records = mysqli_fetch_assoc($individualAttendanceRecords))
                    {
                        $name = $records["name"];
                        $roll = $records["sID"];
                        $presentDays = $records["presentDays"];
                        ?>
                        <tr>
                            <td><?php echo "$name";?></td>
                            <td><?php echo "$roll";?></td>
                            <td><?php echo "$presentDays";?></td>
                        </tr> 
                    <?php
                    }
                    ?>
                    </table>
                    <?php
                }
                else
                {
                    echo "Error running fetch individual attendance records query.";
                }
            }
            else
            {
                echo "Error running fetch attendance records query.";
            }
            ?>
            <div class="card-holder">
                <div class="card-search">
                    <div class="box">
                        <a href="bct.php?dID=<?php echo $dID;?>" >
                            <div class="text"><?php echo "Go Back"?></div>                   
                        </a>
                    </div>
                </div>
                <button class="box-btn" onclick = "downloadRecordTable('<?php echo $cID.'_'.$subject.'_'.$startDate.'_'.$endDate; ?>')">
                        Print Records
                </button>
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
