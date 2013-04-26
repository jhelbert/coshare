var selected_content_ids = [];
var selected_content_map = {};

var album_map = {}

function add_objects(id) {
  var foo = "/add/?album=" + id;
  for (var i = 0; i < selected_content_ids.length;i++) {
    foo += "&eles=" + selected_content_ids[i];
  }
  var link = $("<a/>")
  .attr('href', function() {
    return foo;

  })
  .text("Add");
  var add_to_album = album_map[id];
  for (key in selected_content_map) {
    add_to_album.add_content(key,selected_content_map[key]);
  }
}

$(function() {
  $('#new_plist').watermark('New Playlist');
  $("#new_plist").keyup(function (e) {
    if (e.keyCode == 13) {
      new_plist(e.target.value);
    }
  });

  // instantiate model
  var model = new Model();

  // listen for add_album event
  // occurs when a new album is added to the model
  // also used on load
  model.addEventListener("add_album", function(e) {

    var album_div = $("<div />");
    if (e.album.is_user_generated()) {
      album_div
      .addClass("album-name")
      .attr("id", "album-" + e.album.id)
      .text(e.album.get_name())
      .click(function() {
        model.select_album(e.album);
      });

      if (e.album.is_user_generated()) {
        album_div.droppable({
                    //activeClass: "ui-state-default",
                    activeClass: "droppable-album",
                    hoverClass: "hover-drop-album",
                    accept: ".content",
                    drop: function( event, ui ) {
                    },
                  });
      }

      $("#dynamic-albums").append(album_div);
    }
    else{
      var icon = document.createElement("img");
      icon.setAttribute("id", "icon")
      icon.setAttribute("src", "/static/assets/img/static_playlist_icon.png");
      icon.setAttribute("alt", "static playlist");
      icon.setAttribute("height", "25");
      icon.setAttribute("width", "25");

      album_div
      .addClass("album-name")
            //.addClass("ui-widget-content")
            .attr("id", "album-" + e.album.id)
            .click(function() {
              model.select_album(e.album);
            });
            album_div.append(icon);
            album_div.append(e.album.get_name()); 

            $("#static-albums").append(album_div);
          }
          model.addEventListener("rename_album", function(e2) {

            if (e2.album.equals(e.album)) {
              album_div.text(e2.album.get_name());
              $("#album-title").text(e2.album.get_name());
            }});
        });

  // listen for select_albym event
  // occurs when User selects an album to view
  // e is an event object with an e.album attribute
  // this is the album selected
  model.addEventListener("select_album", function(e) {
    selected_content_ids = [];
    selected_content_map = {};
    selected_album = e.album.id;
        // refresh title
        $("#album-title").text(e.album.get_name());
        if (e.album.get_name() == "All Content") {
          $("#youtube")[0].style.display = "block";
          $("#youtube")[0].style.float = "right";
        }
        else {
          $("#youtube")[0].style.display = "none";
        }

        // update display
        // TODO: fix rep exposure
        if (e.album.is_auto) {
          $("#album-" + e.album.id).addClass("selected-auto-album");
        } else {
          $("#album-" + e.album.id).addClass("selected-album");
        }
        

        // show/hide relevant pictures
        if (e.album.can_rename()) {
          $("#btnRenameAlbum").removeAttr("disabled");
        } else {
          $("#btnRenameAlbum").attr("disabled", "disabled");
        }

        if (e.album.can_remove()) {
          $("#btnRemoveAlbum").removeAttr("disabled");
        } else {
          $("#btnRemoveAlbum").attr("disabled", "disabled");
        }

        if (e.album.can_edit_content()) {
          $("#btnRemoveSelectedContent").removeAttr("disabled");
        } else {
          $("#btnRemoveSelectedContent").attr("disabled", "disabled");
        }

        // refresh contents
        $("#contents-container .content").remove();
        var contents = e.album.get_contents();
        for (var i in contents) {
            // FUCK JAVASCRIPT -- it doesn't even have block level scoping???
            // whatever. use this closure to ensure the meaning of i doesn't suck.
            (function(content) {

              var div = $("<div />")
              .append(content.get_content())
              .addClass("content")
              .attr("id", "content-" + content.id)
              .attr("id-num", content.id)
              .click(function() {
                model.toggle_content(content);
              });
              $("#contents-container").append(div);

              model.addEventListener("select_content", function(e2) {
                if (e2.content.equals(content)) {
                  div.addClass("selected-content");
                  selected_content_ids.push(e2.content.id);
                  selected_content_map[e2.content.id] = e2.content.get_content().src.split("/media/")[1];;
                }
              });
              model.addEventListener("deselect_content", function(e2) {
                if (e2.content.equals(content)) {
                  div.removeClass("selected-content");
                  var index = selected_content_ids.indexOf(e2.content.id);
                  delete selected_content_map[e2.content.id];
                  selected_content_ids.splice(index,1);
                }
              });
            })(contents[i]);
          }
          $("#content").text("content from " + e.album.get_name());

          $(".content").dblclick(function() {
            $(".alert").alert('close');
            $(".playlistList").empty();
            $("#openModal").css("opacity",1);
            $("#openModal").css("pointer-events","auto");
            var image = $(this).children("img").attr("src");
            var id_val = $(this).attr("id-num");
            $(".imageHolder").attr("src",image);
            $(".imageHolder").attr("id-num",id_val);
            $
            // Add playlists info to list
            $.ajax({
              type: "POST",
              url: "/open_modal_view/",
              data: {id: id_val}
            }).done(function( msg ) {
                // upload picture description
                var description = msg["des"];
                var pls = msg["playlists"];
                var photo_table = msg["photos"];
                if (description == "") {
                  description = "No Description";
                }
                $(".imageDescription").text(description);

                for (var i = 0; i < pls.length; i++) {
                  var plName = pls[i];
                  var uiElement = $("<ui class='outerUI'> <h5>" + plName + "</h5></ui>");
                  var ulPhoto = $("<ul class='previewPhoto'> </ul>");
                  for (var j=0; j < photo_table[plName].length; j++) {
                    ulPhoto.append($("<ui class='innerUI'> <img class='thumbnail' src='"+photo_table[plName][j]+"'></img></ui"));
                  }
                  uiElement.append(ulPhoto);
                  $(".playlistList").append(uiElement);
                }
              });

          }).draggable({
            revert: true,
            start: function(event, ui) {
              $(this).addClass('noclick');
            },
            helper: function( event ) {
              return $("<div />").addClass("helper").text("" + model.get_num_selected_contents());
            },
            distance: 20,
            cursorAt: { top: 0, left: -25 },
            cursor: "default",
          });

        });

model.addEventListener("deselect_album", function(e) {
  $("#album-" + e.album.id)
  .removeClass("selected-album")
  .removeClass("selected-auto-album");
});

model.addEventListener("remove_album", function(e) {
  $("#album-" + e.album.id).fadeOut();
});

model.addEventListener("remove_content", function(e) {
  $("#content-" + e.content.id).fadeOut();
});


// create stubbed out albums

{% for playlist in playlists %}
  var album = new Album({{playlist.id}},"{{playlist.name}}");
  model.add_album(album);
  album_map[{{playlist.id}}] = album;
  {% for content in playlist.content.all %}
    album.add_content({{content.id}},"{{content.image}}",{{content.metric}});
  {% endfor %}
{% endfor %}


model.select_album(model.albums[0]);
function new_plist(name) {
  $("#new_plist")[0].value = "";
  var album = new Album(100,name);
  model.add_album(album);

}

    // CRUD operations on albums

    // crea
    $("#btnNewAlbum").click(function() {
        // add stubbed out
        model.add_album(new Album(new Date().getTime() % 100));
      });

    $("#btnRenameAlbum").click(function() {
      model.rename_selected_album();
    });

    $("#btnRemoveAlbum").click(function() {
      model.remove_selected_album();
    });

    // Select/Deselect All
    $("#btnSelectAll").click(function() {
      model.select_all();
    });

    $("#btnDeselectAll").click(function() {
      model.deselect_all();
    });

    $("#btnRemoveSelectedContent").click(function() {
      model.remove_selected_contents_from_selected_album();
    });

    
    $(".imageDescription").click(function() {
      var text = $(".imageDescription").text();
      text = text.trim();
      $(".alert").alert('close');
      $(".descriptionInput").val(text);
      $(".descriptionInput").removeClass("hidden");
      $(".imageDescription").addClass("hidden");
      $(".descriptionInput").focus();
    });


    // Both of below functions need support to update backend
    
    $(".descriptionInput").blur(function() {
      var text = $(".descriptionInput").val();
      text = text.trim();
      $(".imageDescription").text(text);
      $(".descriptionInput").addClass("hidden");
      $(".imageDescription").removeClass("hidden");
      var id_val = $(".imageHolder").attr("id-num").toString();
        // send new text value to the server
        $.ajax({
          type: "POST",
          url: "/save_description/",
          data: { id: id_val, description: text}
        }).done(function( msg ) {
          $(".alert").alert('close');
          if (msg != "error") {
            var alertBox = $("<div class='alert alert-block alert-success'> Description was updated. </div>");

            $("#leftCol").append(alertBox);
          } else {
            var alertBox = $("<div class='alert alert-block alert-error'> <strong> ERROR!</strong> Description was not updated. </div>");

            $("#leftCol").append(alertBox);
          }
        });
      });

    $(".descriptionInput").bind('keypress',function(e) {
      var code = (e.keyCode ? e.keyCode : e.which);
      if (code ==13) {
        var text = $(".descriptionInput").val();
        text = text.trim();
        $(".imageDescription").text(text);
        $(".descriptionInput").addClass("hidden");
        $(".imageDescription").removeClass("hidden");
      }
    });

    $("#closeModal").click(function() {
      $("#openModal").css("opacity",0);
      $("#openModal").css("pointer-events","none");
      $(".alert").alert('close');
    });

    $(".favorited").click(function() {
      $(".favorited").toggleClass("btn-success");
    })

  });