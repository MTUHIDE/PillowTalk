function send_command(str_value) {
  document.getElementById("command").value = str_value;
  document.getElementById("command_form").submit();
}

/**
 * Saves the current settings to local storage in the browser
 */
function save_settings() {
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
