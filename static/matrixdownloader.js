function download(){
      let file = new Blob([userInput], { type: "text/plain;charset=utf-8" });
      saveAs(file, "testmatrix.m");
  }