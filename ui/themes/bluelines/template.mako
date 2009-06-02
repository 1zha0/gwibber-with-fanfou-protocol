<%namespace name="base" file="base.mako">
  <%def name="msgstyle(data)">
    background: -webkit-gradient(linear, left top, left 220%, from(rgba(${data.color.rgb}, 0.6)), to(black));
  </%def>
</%namespace>

<html>
  <head>
    <style>
      <%include file="theme.css" />
    </style>
    <script src="jquery.js"></script>
    <script>
      $(document).ready(function() {
        $(".message").hover(
          function() {$(this).find(".replybutton").fadeIn(100)},
          function() {$(this).find(".replybutton").hide(0)});

        $(".toggledupe").show(0).unbind().toggle(
          function() {$(this).parent().find(".dupes").show(100)},
          function() {$(this).parent().find(".dupes").hide(100)});
      });
    </script>
  </head>
  <body style="background: url(blue_stripe.png);">
    ${base.messages(message_store)}
  </body>
</html>
