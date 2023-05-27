/***** ฟังก์ชันแสดงรายชื่อไฟล์แนบ *****/
updateList = function () {
    var output = document.getElementById('fileList');
    var input = document.getElementById('id_file');
    var children = "";
    output.innerHTML = "";

    for (var i = 0; i < input.files.length; ++i) {
        children += "<input type=text size=100 readonly disabled value='" + input.files.item(i).name +
            "' class='form-control text-dark bg-light'  />";
    }
    if (children != "") {
        output.innerHTML = children;
    }
}
/***************************************/


/* ฟังก์ชัน check จำนวนเงิน ต้องเป็น 0 กรณีไม่ใช้งบประมาณ  */
chkBudgetType = function () {
    var output = document.getElementById('id_budget');
    var input = document.getElementById('id_budgetType').selectedIndex;
    if (input == 3){
        output.value = "0.00";
        output.readOnly = true;
    }else{
        output.readOnly = false;
    }
}

/* ฟังก์ชัน check วันที่เริ่มต้น ต้องก่อนวันที่สิ้นสุด  */
chkDateDiff = function () {
    var output = document.getElementById('id_days');
    var startDate = document.getElementById('id_startDate');
    var endDate = document.getElementById('id_endDate');
    var start_date = new Date(document.getElementById('id_startDate').value);
    var end_date = new Date(document.getElementById('id_endDate').value);
    if (end_date < start_date)  {
        endDate.value = startDate.value
        output.value =  1;
    }else {
        if (start_date && end_date) {
            var time_difference = end_date.getTime() - start_date.getTime();
            var days_difference = (time_difference / (1000*3600*24))+1;
            output.value = days_difference;
        } else{
            output.value =  "";
        }
    }
}

/* ฟังก์ชัน คำนวณจำนวนวัน */
chkDays = function () {
    var output = document.getElementById('id_days');
    var start_date = new Date(document.getElementById('id_startDate').value);
    var end_date = new Date(document.getElementById('id_endDate').value);
    var days = document.getElementById('id_days').value;
    if (start_date && end_date) {
        var time_difference = end_date.getTime() - start_date.getTime();
        var days_difference = (time_difference / (1000 * 3600 * 24)) + 1;
        // alert("Day: "+days.toString() + ", Diff: " + days_difference.toString());
        if (days> days_difference) {
            alert("ระบุจำนวนวันไม่ถูกต้อง");
            output.value = days_difference;
        }
    }
}

/* ฟังก์ชัน เลือก Selectbox บุคลากร */
chkSelect = function (name, chkAll) {
    var checkBox = document.getElementById(chkAll);
    var allname = document.getElementsByName(name);
    var nameId="";
    for(i=0; i<allname.length;i++){
        nameId = "id_"+name+"_" + i.toString();
        if(checkBox.checked==true) {
            document.getElementById(nameId).setAttribute('checked', 'checked');
        }else{
            document.getElementById(nameId).removeAttribute('checked');
        }
    }
}

// chkSelect = function () {
//     var checkBox = document.getElementById("chkAll");
//     var personnels = document.getElementsByName("personnel")
//     var personnelID="";
//     for(i=0; i<personnels.length;i++){
//         personnelID = "id_personnel_" + i.toString();
//         if(checkBox.checked==true) {
//             document.getElementById(personnelID).setAttribute('checked', 'checked');
//         }else{
//             document.getElementById(personnelID).removeAttribute('checked');
//         }
//     }
// }


