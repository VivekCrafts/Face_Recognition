Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "/", // Dummy URL
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Drop an image or click to upload",
        autoProcessQueue: false,
        acceptedFiles: "image/*"
    });

    dz.on("addedfile", function () {
        // Limit to one file at a time
        if (dz.files[1] != null) {
            dz.removeFile(dz.files[0]);
        }
        // Reset UI state
        $("#error").hide();
        $("#resultHolder").hide();
        $("#loading").hide();
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;
        let url = "http://127.0.0.1:5000/classify_image";

        // Show loading state
        $("#loading").show();
        $("#error").hide();
        $("#resultHolder").hide();

        $.post(url, {
            image_data: imageData
        }, function (data, status) {
            $("#loading").hide();
            
            if (status !== "success") {
                showError("Network error occurred. Please try again.");
                return;
            }

            if (!data || data.length === 0) {
                showError("No faces detected in the image. Please upload an image with a clear face.");
                return;
            }

            if (data.error) {
                showError(data.error);
                return;
            }

            const players = ["lionel_messi", "maria_sharapova", "roger_federer", "serena_williams", "virat_kohli"];

            let match = null;
            let bestScore = -1;

            // Find the classification with the highest score
            for (let i = 0; i < data.length; ++i) {
                let maxScore = Math.max(...data[i].class_probability);
                if (maxScore > bestScore) {
                    match = data[i];
                    bestScore = maxScore;
                }
            }

            if (match) {
                showResult(match, bestScore);
            } else {
                showError("Unable to classify the image. Please try a different image.");
            }
        }).fail(function(xhr, status, error) {
            $("#loading").hide();
            showError("Server error occurred. Please try again later.");
        });
    });

    // Trigger processing on button click
    $("#submitBtn").on('click', function () {
        if (dz.files.length === 0) {
            showError("Please upload an image first.");
            return;
        }
        dz.processQueue();
    });
}

function showError(message) {
    $("#error").show().find("p").text(message);
    $("#resultHolder").hide();
}

function showResult(match, confidence) {
    $("#error").hide();
    $("#resultHolder").show();

    // Create result card with confidence score
    let resultHtml = `
        <div class="card border-success">
            <div class="card-header bg-success text-white text-center">
                <h5 class="mb-0">Classification Result</h5>
            </div>
            <div class="card-body text-center">
                ${$(`[data-player="${match.class}"]`).find('.card-body').html()}
                <div class="mt-3">
                    <span class="badge badge-success">Confidence: ${confidence.toFixed(1)}%</span>
                </div>
            </div>
        </div>
    `;
    
    $("#resultHolder").html(resultHtml);
}

$(document).ready(function () {
    $("#error").hide();
    $("#resultHolder").hide();
    $("#loading").hide();
    init();
});
