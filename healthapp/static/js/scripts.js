// Script for searching centers using Ajax
var href = document.location.href;
var lastPathSegment = href.lastIndexOf("/") + 1;

const endpoint = "/centers/";
function ajax_query() {
  $.ajax({
    type: "POST",
    url: endpoint,
    data: {
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      query: $("#user-input").val().trim(),
    },
    success: function (data) {
      var current_title = $(document).attr("title");
      if (data.centers.length == 0) {
        anchor = document.createElement("a");
        link = "#";

        anchor.href = link;
        anchor.text = "No Results Found";
        liList = document.createElement("li");
        liList.appendChild(anchor);
        $("#search-results").append(liList);
      } else {
        $.each(data, function () {
          $.each(data.centers, function (k, v) {
            // create link
            anchor = document.createElement("a");
            if (current_title == "District Wellness Centers") {
              link = "/center/" + v.center_abbreviation + "/";
            } else {
              anchor = document.createElement("a");
              link = "/center/" + v.center_abbreviation + "/";
            }

            anchor.href = link;
            anchor.text = v.name;
            liList = document.createElement("li");
            liList.appendChild(anchor);
            $("#search-results").append(liList);
          });
        });
      }
    },

    failure: function (data) {
      console.log("FAIL");
      console.log(data);
    },
  });
}
$(document).ready(function () {
  $("#user-input").on(
    "keyup keypress",
    $.debounce(500, function () {
      if ($("#user-input").val() != 0) {
        console.log("working debauncing");
        ajax_query();
      } else {
        return false;
      }
    })
  );

  $("#user-input").keyup(function (e) {
    if ($.trim($(this).val()).length) {
      $("#search-icon").addClass("blink");
      $("#search-popup").addClass("search-popup-populated");
    } else {
      $("#search-icon").removeClass("blink");
      $("#search-popup").removeClass("search-popup-populated");
    }
    $("#search-results").empty();
  });
  $("#user-input").keydown(function () {
    $("#search-results").empty();
  });

  $("#center-query-form").submit(function (e) {
    e.preventDefault();
  });
});

// Read a page's GET URL variables and return them as an associative array.
function getUrlVars() {
  var vars = [],
    hash;
  var hashes = window.location.href
    .slice(window.location.href.indexOf("?") + 1)
    .split("&");
  for (var i = 0; i < hashes.length; i++) {
    hash = hashes[i].split("=");
    vars.push(hash[0]);
    vars[hash[0]] = hash[1];
  }
  return vars;
}
function getPageName(url) {
  var index = url.lastIndexOf("/") + 1;
  var filenameWithExtension = url.substr(index);
  var filename = filenameWithExtension.split(".")[0]; // <-- added this line
  return filename; // <-- added this line
}
