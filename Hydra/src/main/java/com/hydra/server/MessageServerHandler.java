package com.hydra.server;

import com.hydra.core.Client;
import com.hydra.core.Message;
import com.hydra.core.ProtocolException;
import java.util.Collection;
import java.util.Timer;
import java.util.TimerTask;
import org.apache.mina.api.IdleStatus;
import org.apache.mina.api.IoHandler;
import org.apache.mina.api.IoService;
import org.apache.mina.api.IoSession;
import org.apache.mina.session.AttributeKey;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 *
 * @author Hwaipy
 */
public class MessageServerHandler implements IoHandler {

  private static final Logger LOGGER = LoggerFactory.getLogger(MessageServerHandler.class);
  private static final AttributeKey<Client> CLIENT_KEY = AttributeKey.createKey(Client.class, "Client");

  @Override
  public void sessionOpened(IoSession session) {
    Client client = Client.create(session);
    session.setAttribute(CLIENT_KEY, client);
    session.getConfig().setIdleTimeInMillis(IdleStatus.READ_IDLE, 20000);
  }

  @Override
  public void sessionClosed(IoSession session) {
    Client client = session.getAttribute(CLIENT_KEY);
    client.close();
  }

  @Override
  public void sessionIdle(IoSession session, IdleStatus status) {
    LOGGER.info("Session[" + session.getId() + "] idled for "
            + session.getConfig().getIdleTimeInMillis(IdleStatus.READ_IDLE)
            + " ms, time to close.");
    session.close(true);
  }

  @Override
  public void messageReceived(IoSession session, Object messageObject) {
    if (messageObject instanceof Collection) {
      Collection<Message> messageList = (Collection<Message>) messageObject;
      Client client = session.getAttribute(CLIENT_KEY);
      client.feed(messageList);
    } else {
      throw new IllegalArgumentException("message passed should be a list of Message.");
    }
  }

  @Override
  public void messageSent(IoSession session, Object message) {
  }

  @Override
  public void serviceActivated(IoService service) {
  }

  @Override
  public void serviceInactivated(IoService service) {
  }

  @Override
  public void exceptionCaught(final IoSession session, Exception cause) {
    if (cause instanceof ProtocolException) {
      LOGGER.warn("ProtocolException caught, Session[" + session.getId() + "] is about to close.", cause);
      Client client = session.getAttribute(CLIENT_KEY);
      Message message = new Message();
      message.put(Message.KEY_ERROR, "").put(Message.KEY_MESSAGE_ID, -1).put(Message.KEY_ERROR_MESSAGE, cause);
      client.write(message);
      timer.schedule(new TimerTask() {

        @Override
        public void run() {
          session.close(true);
        }
      }, 3000);
    } else {
      LOGGER.warn("Exception caught, Session[" + session.getId() + "] is about to close.", cause);
      session.close(true);
    }
  }
  private static final Timer timer = new Timer("Session Idler Timer", true);
}
