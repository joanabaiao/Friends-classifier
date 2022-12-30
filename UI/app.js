Dropzone.autoDiscover = false;

function init() {

    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });

    dz.on("addedfile", function () {
        if (dz.files[1] != null) {
            dz.removeFile(dz.files[0]);
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;
        var url = "http://127.0.0.1:5000/classify_image";

        $.post(url, {
            image_data: imageData
        }, function (data, status) {
            console.log(data);

            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }

            // let players = ["David_Schwimmer", "Jennifer_Aniston", "Lisa_Kudrow", "Courteney_Cox", "Matt_LeBlanc", "Matthew_Perry"];
            
            let match = null;
            console.log(data.length)
            let bestScore = -1;
            for (let i=0; i<data.length; ++i) {
                //let maxScoreForThisClass = Math.max.apply(Math, data[i].class_probability);
                let maxScoreForThisClass = Math.max.apply(Math, data[i].class_probability);
                if(maxScoreForThisClass >= bestScore) {
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }

            console.log(match);
            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                $("#resultHolder").html($(`[data-actor="${match.class_predicted}"`).html());

                let classDictionary = match.class_dictionary;
                for(let personName in classDictionary) {
                    let index = classDictionary[personName];
                    let probabilityScore = match.class_probability[index];
                    let elementName = "#score_" + personName;
                    $(elementName).html(probabilityScore);
                }
            }
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();
    });
}

$(document).ready(function () {
    console.log("ready!");
    $("#error").hide(); // hide error
    $("#resultHolder").hide();
    $("#divClassTable").hide();
    init();
});