import gtk, microblog, gintegration, resources

class MessageAction:
  icon = None
  label = None

  @classmethod
  def get_icon_path(self, size=16, use_theme=True):
    return resources.icon(self.icon, size, use_theme)
    
  @classmethod
  def include(self, client, msg):
    return True

  @classmethod
  def action(self, w, client, msg):
    pass

class Reply(MessageAction):
  icon = "mail-reply-sender"
  label = "_Reply"

  @classmethod
  def include(self, client, msg):
    return msg.account.supports(microblog.can.REPLY)

  @classmethod
  def action(self, w, client, msg):
    client.reply(msg)

class ViewThread(MessageAction):
  icon = "mail-reply-all"
  label = "View reply t_hread"

  @classmethod
  def action(self, w, client, msg):
    tab_label = msg.original_title if hasattr(msg, "original_title") else msg.text
    t = client.add_msg_tab(lambda: client.client.thread(msg),
      microblog.support.truncate(tab_label), True, "mail-reply-all", True)
    client.update([t.get_parent()])

  @classmethod
  def include(self, client, msg):
    return hasattr(msg, "can_thread")

class Retweet(MessageAction):
  icon = "mail-forward"
  label = "R_etweet"

  @classmethod
  def action(self, w, client, msg):
    if not client.preferences["global_retweet"]:
      client.message_target = msg

    if client.preferences["retweet_style_via"]:
      client.input.set_text("%s (via @%s)" % (msg.text, msg.sender_nick))
    else:
      client.input.set_text(u"\u267a @%s: %s" % (msg.sender_nick, msg.text))

    client.cancel_button.show()
    client.input.grab_focus()
    client.input.set_position(-1)

  @classmethod
  def include(self, client, msg):
    return msg.account.supports(microblog.can.RETWEET)

class Like(MessageAction):
  icon = "bookmark_add"
  label = "_Like this message"

  @classmethod
  def action(self, w, client, msg):
    msg.account.get_client().like(msg)
    d = gtk.MessageDialog(buttons=gtk.BUTTONS_OK)
    d.set_markup("You have marked this message as liked.")
    if d.run(): d.destroy()

  @classmethod
  def include(self, client, msg):
    return msg.account.supports(microblog.can.LIKE)

class Delete(MessageAction):
  icon = "gtk-delete"
  label = "_Delete this message"

  @classmethod
  def action(self, w, client, msg):
    msg.account.get_client().delete(msg)
    d = gtk.MessageDialog(buttons=gtk.BUTTONS_OK)
    d.set_markup("The message has been deleted.")
    if d.run(): d.destroy()

  @classmethod
  def include(self, client, msg):
    return msg.account.supports(microblog.can.DELETE) and \
      msg.sender_nick == msg.account["username"]

class Tomboy(MessageAction):
  icon = "tomboy"
  label = "Save to _Tomboy"

  @classmethod
  def action(self, w, client, msg):
    gintegration.create_tomboy_note(
      "%s message from %s at %s\n\n%s\n\nSource: %s" % (
        msg.account["protocol"].capitalize(),
        msg.sender, msg.time, msg.text, msg.url))

  @classmethod
  def include(self, client, msg):
    return gintegration.service_is_running("org.gnome.Tomboy")

MENU_ITEMS = [Reply, ViewThread, Retweet, Like, Delete, Tomboy]
