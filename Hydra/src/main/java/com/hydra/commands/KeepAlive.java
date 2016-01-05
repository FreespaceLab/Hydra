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
  public void execute(Message message, Client client) {
  }

  @Override
  protected void executeCommand(Message message, Client client) {
  }
}
