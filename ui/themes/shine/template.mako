<%namespace name="base" file="base.mako">
  <%def name="shine_heading_style(data, a)" filter="trim">
    background: rgba(${data.color.rgb}, ${a}) -webkit-gradient(linear, left top, left bottom,
          from(rgba(255, 255, 255, 0.45)), to(rgba(255, 255, 255, 0.50)),
          color-stop(0.4, rgba(255, 255, 255, 0.25)),
          color-stop(0.6, rgba(255, 255, 255, 0.0)),
          color-stop(0.9, rgba(255, 255, 255, 0.10)));
    border-top: 2px solid rgba(${data.color.rgb}, ${a});
    border-bottom: 2px solid rgba(${data.color.rgb}, ${a});
  </%def>

  <%def name="image(data)">
    <a href="${data.profile_url}">
      <img class="imgbox" title="${data.sender_nick}" src="${data.image}" />
    </a>
  </%def>

  <%def name="message(data)">
    <%call expr="base.messagebox(data)">
      <div class="heading" style="${shine_heading_style(data, 1)}">
        ${base.image(data)}
        ${base.title(data)}
        <div class="bottom">
          <span class="time">(${base.timestring(data)})</span>
          ${base.toggledupe(data)}
          ${base.buttons(data)}
        </div>
      </div>
      <div class="content"><span class="text">${data.html_string}</span></div>
      ${base.fold(data)}
      ${base.dupes(data)}
    </%call>
  </%def>
</%namespace>

<html>
  <head>
    <link rel="stylesheet" type="text/css" href="theme.css?20" />
    <script src="jquery.js"></script>
    <script>
      $(document).ready(function() {
        $(".message").hover(
          function() {$(this).find(".replybutton").fadeIn(100)},
          function() {$(this).find(".replybutton").hide(0)});

        $(".toggledupe").show(0).unbind().toggle(
          function() {$(this).parent().parent().parent().find(".dupes").show(100)},
          function() {$(this).parent().parent().parent().find(".dupes").hide(100)});
      });
    </script>
    <style>
      <%include file="theme.css" />
    </style>
  </head>
  <body>
    ${base.messages(message_store)}
  </body>
</html>
