function get_data(guild_id){
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.open("GET", "/guild_data?guild_id="+guild_id);


    xmlhttp.onload = function () {
        var result = JSON.parse(xmlhttp.responseText);
        load_complete(result);

    };

    xmlhttp.send();
}

function load_complete(data){
        var loading_image = document.getElementById("loading_image");
        loading_image.parentNode.removeChild(loading_image);

        document.getElementById("guild_data").style.display = "block";
        document.getElementById("filter_controls").style.display = "block";

        document.getElementById("character_data").innerHTML = tmpl("character_data_template", data);

        prepare_character_filter(data);
        init_events();
}

function set_col_visibility(col_num){
    col_num = parseInt(col_num);

    for(var rarity =1; rarity < col_num; rarity++){
        var items = document.getElementsByClassName(rarity + "_star");
        for (var i  = 0; i < items.length; i++){
            items[i].style.display = "none";
        }
    }

    for(var rarity = col_num; rarity <= 7; rarity++) {
        var items = document.getElementsByClassName(rarity + "_star");
        for (var i  = 0; i < items.length; i++) {
            items[i].style.display = "table-cell";
        }
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
    var star_filter = document.getElementById("star-filter");
    star_filter.addEventListener("change", function(){
        set_col_visibility(star_filter.value);
    });


    items = document.getElementsByClassName("force_side_checkbox");

    for (var i  = 0; i < items.length; i++){
        items[i].addEventListener("click", function(){
            set_force_visibility(this.getAttribute("data-force-side"), this.checked);
        })
    }

    var character_list = document.getElementById("character_list");
    character_list.addEventListener("change",  function(){
        filter_character(character_list.value);
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

    var character_list = document.getElementById("character_list");

    for (var i =0; i < characters.length; i++){
        var option = document.createElement("option");
        option.text = characters[i];
        option.value = replace_all(characters[i], ' ', '_')

        character_list.add(option);
    }
}

function replace_all(str, find, replace) {
    return str.replace(new RegExp(find, 'g'), replace);
}

function format_entry(entry){
    return entry["player"] + " ("+ entry["power"] + ')';
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