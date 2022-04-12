function send_command(str_value) {
  document.getElementById("command").value = str_value;
  document.getElementById("command_form").submit();
}

/**
 * Saves the current settings to local storage in the browser
 */
function save_settings() {
  console.log("Saving settings to local storage")

  var cushion_1_nick = document.getElementById("cushion_1_nickname").value;
  var cushion_2_nick = document.getElementById("cushion_2_nickname").value;
  var cushion_1_time = document.getElementById("cushion_1_time").value;
  var cushion_2_time = document.getElementById("cushion_2_time").value;

  if (cushion_1_nick) {
    localStorage.setItem("cushion_1_nick", cushion_1_nick);
  }

  if (cushion_2_nick) {
    localStorage.setItem("cushion_2_nick", cushion_2_nick);
  }

  if (cushion_1_time) {
    localStorage.setItem("cushion_1_time", cushion_1_time);
  }

  if (cushion_2_time) {
    localStorage.setItem("cushion_2_time", cushion_2_time);
  }
}

/**
 * Loads settings in the browser's local storage
 */
function load_stored_settings() {
  console.log("Loading stored settings")

  if (localStorage.getItem("cushion_1_nick") != 'null') {
    document.getElementById("cushion_1_nickname").value = localStorage.getItem("cushion_1_nick");
  }

  if (localStorage.getItem("cushion_2_nick") != null) {
    document.getElementById("cushion_2_nickname").value = localStorage.getItem("cushion_2_nick");
  }

  if (localStorage.getItem("cushion_1_time") != null) {
    document.getElementById("cushion_1_time").value = localStorage.getItem("cushion_1_time");
  }

  if (localStorage.getItem("cushion_2_time") != null) {
    document.getElementById("cushion_2_time").value = localStorage.getItem("cushion_2_time");
  }
}

/**
 * Resets settings to default values
 */
function reset_settings() {
  // TODO: Implement this
}

function saveCushionNames(event) {
  if (event.keyCode !== 13) {
    return
  }

  var settings = {
    "cushion_1_nickname": document.getElementById("cushion-1-nickname").value,
    "cushion_2_nickname": document.getElementById("cushion-2-nickname").value,
  }

  var xhttp = new XMLHttpRequest()
  
  xhttp.open("POST", "/settings")
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
  xhttp.send(JSON.stringify(settings))
}

function inflate(cushion, side) {
  var xhttp = new XMLHttpRequest()
  
  xhttp.open("POST", "/motorcontrol")
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
  xhttp.send(JSON.stringify({"motors": [{"motor": cushion, "time": parseInt(document.getElementById(`cushion-${side}-time`).value)}]}))
}

function deflate(cushion, side) {
  var xhttp = new XMLHttpRequest()
  
  xhttp.open("POST", "/motorcontrol")
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
  xhttp.send(JSON.stringify({"motors": [{"motor": cushion, "time": parseInt(document.getElementById(`cushion-${side}-time`).value)}]}))
}

function stopAll() {
  var xhttp = new XMLHttpRequest()
  
  xhttp.open("POST", "/motorcontrol")
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
  xhttp.send(JSON.stringify({"motors": []}))
}
