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

/* ฟังก์ชัน check วันที่ ไม่ก่อนปัจจุบัน */
/* ฟังก์ชัน check วันที่เริ่มต้น ต้องก่อนวันที่สิ้นสุด*/
/* ฟังก์ชัน คำนวณจำนวนวัน */
/* ฟังก์ชัน check จำนวนวัน ที่ไม่เกินวันที่สิ้นสุด - วันเริ่มต้น */
/* ฟังก์ชัน check จำนวนเงิน ต้องเป็น 0 กรณีไม่ใช้งบประมาณ  */

/* ฟังก์ชัน check งบประมาณ กรณีที่ไม่ใช้งบประมาณ */
updateBudget = function () {
    var output = document.getElementById('id_budget');
    var input = document.getElementById('id_budgetType').selectedIndex;
    if (input == 3){
        output.value = "0.00";
        output.readOnly = true;
    }else{
        output.readOnly = false;
    }
}


