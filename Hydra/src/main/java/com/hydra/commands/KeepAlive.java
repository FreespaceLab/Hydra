package com.hydra.commands;

import com.hydra.core.Client;
import com.hydra.core.Command;
import com.hydra.core.Message;

/**
 *
 * @author Hwaipy
 */
public class KeepAlive extends Command {

  public KeepAlive() {
    super("KeepAlive");
  }

  @Override
  protected void executeCommand(Message message, Client client) {
    Message response = message.response();
    client.write(response);
  }
}
