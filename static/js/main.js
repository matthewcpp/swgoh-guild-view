function get_data(){
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.open("GET", "/guild_data");


    xmlhttp.onload = function () {
        var result = JSON.parse(xmlhttp.responseText);

        if (result.status === "processing"){
            setTimeout(get_data, 1000);
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