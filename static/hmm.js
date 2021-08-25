let currstates = -1;
let curroutputs = -1;

function changeStates(){
  let states = parseInt(document.getElementById('states').value, 10);
  console.log(states);
  console.log(Number.isInteger(states));
  if (Number.isInteger(states) && states >= 1){
    currstates = states;
    onStateUpdate();
  }
}

function onStateUpdate(){
  document.getElementById('statenames').innerHTML="";
  console.log("onStateUpdate");
  for (var i=1; i<= currstates; i++) {
      let wheel = document.createElement("input");
      wheel.type = "text";
      wheel.name = "state" + i;
      wheel.id = "state" + i;
      wheel.width = "30"
      wheel.required = true;

      let labeler = document.createElement("label");
      labeler.for = wheel.id;
      labeler.id = "statelabel" + i;
      labeler.innerHTML = "State " + i +"";
      
      document.getElementById("statenames").appendChild(labeler);
      document.getElementById("statenames").appendChild(wheel);
  }
}

function changeOutputs(){
  let outputs = parseInt(document.getElementById('outputs').value, 10);
  console.log(outputs);
  if (Number.isInteger(outputs) && outputs >= 1){
    curroutputs = outputs;
    onOutputUpdate();
  }
}

function onOutputUpdate(){
  document.getElementById('outputnames').innerHTML="";
  console.log("onoutputUpdate");
  for (var i=1; i<= curroutputs; i++) {
      let wheel = document.createElement("input");
      wheel.type = "text";
      wheel.name = "output" + i;
      wheel.id = "output" + i;
      wheel.width = "30"
      wheel.required = true;

      let labeler = document.createElement("label");
      labeler.for = wheel.id;
      labeler.id = "outputlabel" + i;
      labeler.innerHTML = "Output " + i +"";
      
      document.getElementById("outputnames").appendChild(labeler);
      document.getElementById("outputnames").appendChild(wheel);
  }
}
