function get_data(guild_name, guild_id){
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.open("GET", "/guild_data?guild_name="+guild_name+"&guild_id="+guild_id);


    xmlhttp.onload = function () {
        var result = JSON.parse(xmlhttp.responseText);

        if (result.status === "processing"){
            update_progress(result.progress, guild_name, guild_id);
        }
        else{
            var loading_image = document.getElementById("loading_image");
            loading_image.parentNode.removeChild(loading_image);

            document.getElementById("guild_data").style.display = "block";
            document.getElementById("filter_controls").style.display = "block";

            document.getElementById("character_data").innerHTML = tmpl("character_data_template", result.data);

            prepare_character_filter(result.data);
            init_events();
        }
    };

    xmlhttp.send();
}

var prev_progress = 0;

function update_progress(progress, guild_name, guild_id){
    if (progress.processed >= prev_progress){
        prev_progress = progress.processed;

        var guild_progress = document.getElementById("guild_progress");
        guild_progress.innerHTML = "Processed: " + progress.processed + "/"+progress.total;

        setTimeout(function() {
            get_data(guild_name, guild_id);
        }, 1000);
    }
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function set_col_visibility(col_num, visibility){
    var items = document.getElementsByClassName(col_num + "_star");
    var display_text = visibility ? "table-cell" : "none";

    for (var i  = 0; i < items.length; i++){
        items[i].style.display = display_text;
    }
}

function set_force_visibility(force_side, visibility){
    var items = document.getElementsByClassName(force_side);
    var display_text = visibility ? "table-row" : "none";

    for (var i  = 0; i < items.length; i++) {
        items[i].style.display = display_text;
    }
}

function init_events(){
    var items = document.getElementsByClassName("star_filter_checkbox");

    for (var i  = 0; i < items.length; i++){
        items[i].addEventListener("click", function(){
            set_col_visibility(this.getAttribute("data-col"), this.checked);
        })
    }

    items = document.getElementsByClassName("force_side_checkbox");

    for (var i  = 0; i < items.length; i++){
        items[i].addEventListener("click", function(){
            set_force_visibility(this.getAttribute("data-force-side"), this.checked);
        })
    }

    var character_filter = document.getElementById("character_filter");
    character_filter.addEventListener("change",  function(){
        filter_character(character_filter.value);
    });

}

function filter_character(character_name){
    if (character_name ==="all"){
        var items = document.getElementsByClassName("character");
        for (var i  = 0; i < items.length; i++) {
            items[i].style.display = "table-row";
        }

        var light_side_filter = document.getElementById("light_side_filter");
        var dark_side_filter = document.getElementById("dark_side_filter");

        if (!light_side_filter.checked)
            set_force_visibility(light_side_filter.getAttribute("data-force-side"), false);

        if (!dark_side_filter.checked)
            set_force_visibility(dark_side_filter.getAttribute("data-force-side"), false);

            items = document.getElementsByClassName("force_side_checkbox");
        for (var i  = 0; i < items.length; i++) {
            items[i].disabled = false;
        }
    }
    else{
        var items = document.getElementsByClassName("character");
        for (var i  = 0; i < items.length; i++) {
            items[i].style.display = "none";
        }

        items = document.getElementsByClassName("force_side_checkbox");
        for (var i  = 0; i < items.length; i++) {
            items[i].disabled = true;
        }

        document.getElementById(character_name).style.display = "table-row";
    }
}



function prepare_character_filter(data){
    var characters = Object.keys(data);

    var character_filter = document.getElementById("character_filter");

    for (var i =0; i < characters.length; i++){
        var option = document.createElement("option");
        option.text = characters[i];
        option.value = replace_all(characters[i], ' ', '_');

        character_filter.add(option);
    }
}

function replace_all(str, find, replace) {
    return str.replace(new RegExp(find, 'g'), replace);
}