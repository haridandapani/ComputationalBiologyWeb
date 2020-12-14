$(document).ready(function(){

  $('input[type="radio"]').click(function(){
  if (document.getElementById("local").checked){
    $("#opter").hide();
    $("#affiner").hide();
    $("#affinelogger").hide();
  } else if (document.getElementById("global").checked){
    $("#opter").show();
    $("#affiner").hide();
    $("#affinelogger").hide();
  } else if (document.getElementById("affine").checked){
    $("#opter").show();
    $("#affiner").show();
    $("#affinelogger").hide();
  } else if (document.getElementById("affinelog").checked){
    $("#opter").show();
    $("#affiner").hide();
    $("#affinelogger").show();
  }
  });
});

function loader(){
  console.log("here");
  if (document.getElementById("local").checked){
    $("#opter").hide();
    $("#affiner").hide();
    $("#affinelogger").hide();
  } else if (document.getElementById("global").checked){
    $("#opter").show();
    $("#affiner").hide();
    $("#affinelogger").hide();
  } else if (document.getElementById("affine").checked){
    $("#opter").show();
    $("#affiner").show();
    $("#affinelogger").hide();
  } else if (document.getElementById("affinelog").checked){
    $("#opter").show();
    $("#affiner").hide();
    $("#affinelogger").show();
  }
}