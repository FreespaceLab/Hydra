package com.hydra.core;

import com.hydra.commands.ConnectionCommand;
import com.hydra.commands.KeepAlive;
import com.hydra.commands.ServiceRegistrationCommand;
import com.hydra.commands.SummaryRegistrationCommand;
import java.util.concurrent.ConcurrentHashMap;

/**
 *
 * @author Hwaipy
 */
public class Commands {

  private static final ConcurrentHashMap<String, Command> COMMAND_MAP = new ConcurrentHashMap<>();

  public static boolean registerCommand(Command command) {
    Command previous = COMMAND_MAP.putIfAbsent(command.getName(), command);
    return previous == null;
  }

  public static Command getCommand(String name) {
    return COMMAND_MAP.get(name);
  }

  static {
    registerCommand(new ConnectionCommand());
    registerCommand(new ServiceRegistrationCommand());
    registerCommand(new SummaryRegistrationCommand());
    registerCommand(new KeepAlive());
  }
}
