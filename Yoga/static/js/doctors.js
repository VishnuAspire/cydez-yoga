// function getDoctor(){
//     var departmentSelected = document.getElementById('departmentSelect').value;

//     if ( departmentSelected != ''){
        
//         x = new XMLHttpRequest;
//         x.open('GET','requestAppoinment?department='+departmentSelected);
//         x.send();
//         x.onreadystatechange = function(){
//             if (this.readyState == 4 && this.status == 200){
//                 var ca = document.getElementById('doctorSelect');
//                 ca.innerHTML = x.response;
//             }
//         };
//     }
// }