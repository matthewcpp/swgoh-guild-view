function get_data(guild_name, guild_id){
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.open("GET", "/guild_data?guild_name="+guild_name+"&guild_id="+guild_id);


    xmlhttp.onload = function () {
        var result = JSON.parse(xmlhttp.responseText);

        if (result.status === "processing"){
            update_progress(result.progress, guild_name, guild_id);
        }
        else{
            var content = document.getElementById("content");
            content.removeChild(document.getElementById("loading_image"));


            document.getElementById("character_data").innerHTML = tmpl("character_data_template", result.data);
            var character_table = document.getElementById("character_table")
            character_table.style.display="block";
        }
    };

    xmlhttp.send();
}

function update_progress(progress, guild_name, guild_id){
    var guild_progress = document.getElementById("guild_progress");
    guild_progress.innerHTML = "Processed: " + progress.processed + "/"+progress.total;

    setTimeout(function() {
        get_data(guild_name, guild_id);
    }, 1000);
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