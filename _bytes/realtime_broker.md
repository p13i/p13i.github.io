---
layout: post
title: Simple Realtime WebSocket Message Broker
programming_language: TypeScript
date: 2021-03-12
---

# `server.ts`

Run on a publically-accessible IP port.

```ts
import express from "express";
import { createServer } from "http";
import { Server, Socket } from "socket.io";

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer);

const getRoomName = (userId: number) => {
  return `${userId}`;
};

io.on("connection", (socket: Socket) => {
  let thisUserId: number | undefined;

  socket.onAny((eventName: string, ...args: any[]) => {
    let data = args[0];
    let { recipientUserId, senderUserId } = data;

    {
      let dataStr = JSON.stringify(data);
      console.log(
        `Received ${eventName} from ${senderUserId} with data: ${dataStr.substr(
          0,
          64
        )}${dataStr.length >= 64 ? "..." : ""}`
      );
    }

    if (eventName === "join") {
      thisUserId = senderUserId as number;
      socket.join(getRoomName(thisUserId));
      return;
    }

    if (eventName === "time") {
      socket.emit("time", {
        recipientUserId: thisUserId,
        time: Date.now(),
      });
      return;
    }

    if (eventName === "disconnect") {
      console.log(`${thisUserId} has disconnected`);
      return;
    }

    let recipientRoomName = getRoomName(recipientUserId);
    console.log(`Sending to '${recipientRoomName}'`);

    io.to(recipientRoomName).emit(eventName, data);
  });
});

app.get("/", (req, res) => {
  res.send("Real-Time Signal Broker");
});

app.get("/time/", (req, res) => {
  res.status(200);
  res.send(`${Date.now()}`);
});

const PORT = process.env.PORT || 3000;

httpServer.listen(PORT, () => {
  let address = httpServer.address() as any;
  if ("address" in address) {
    address = address["address"];
  }
  console.log(`Listening at ${address}:${PORT}`);
});
```

# `client.ts`

Run on any node.js client (e.g., mobile, web, server).

```ts
import SocketIOClient from "socket.io-client";
import { AxiosInstance } from "axios";

export interface WebSocketBrokerRequiredData {
  recipientUserId: number;
}

export declare type EventsCallBackType<T = any> = (
  data: T
) => void;

export default class WebSocketBroker {
  private static _socket?: SocketIOClient.Socket;
  private _connectionTimeout?: NodeJS.Timeout;
  private _onEvents: Map<string, EventsCallBackType> =
    new Map();

  constructor(
    private _webSocketURL: string,
    private _axios: AxiosInstance,
    private thisUserId: number
  ) {}

  public start = async () => {
    console.log("this.start");
    console.debug(
      `Establishing websocket connection with ${this._webSocketURL}`
    );
    WebSocketBroker._socket = SocketIOClient(
      this._webSocketURL
    );
    WebSocketBroker._socket.on("connect", async () => {
      console.debug(`socket on connected`);
      await this._join();
    });
    WebSocketBroker._socket.on("disconnect", () => {
      console.debug(
        `Disconnected from ${this._webSocketURL}`
      );
    });
    WebSocketBroker._socket.connect();
  };

  public isConnected = (
    checkServerAvailability: boolean = false
  ): Promise<boolean> => {
    // TODO maybe use this._socket.connected ?
    return new Promise<boolean>(async (resolve) => {
      if (!WebSocketBroker._socket) {
        return resolve(false);
      }

      if (!checkServerAvailability) {
        return resolve(WebSocketBroker._socket.connected);
      }

      let timeoutFn = (shouldResolve: boolean) => {
        if (this._connectionTimeout) {
          clearTimeout(this._connectionTimeout);
          this._connectionTimeout = undefined;
        }
        this.off("time");
        resolve(shouldResolve);
      };

      // Timeout to resolve false
      this._connectionTimeout = setTimeout(
        () => timeoutFn(false),
        5 * 1000
      );

      await this._onInternal("time", (data: any) =>
        timeoutFn(true)
      );

      await this._sendInternal("time", {
        recipientUserId: this._thisUserId!,
      });
    });
  };

  private _join = async () => {
    console.debug("_join");
    if (!WebSocketBroker._socket) {
      console.error(
        `Socket connection not established! Cannot join room.`
      );
      return;
    }

    type JoinDetails = {
      senderUserId: number;
    } & WebSocketBrokerRequiredData;

    await this._sendInternal<JoinDetails>("join", {
      senderUserId: this._thisUserId,
      recipientUserId: -1,
    });
  };

  send = async <T extends WebSocketBrokerRequiredData>(
    event: string,
    data: T
  ) => {
    if (event === "join" || event === "time") {
      console.warn(
        `Attempting to use reserved event ${event}`
      );
    }

    await this._sendInternal(event, data);
  };

  on = async <T extends WebSocketBrokerRequiredData>(
    event: string,
    callback: EventsCallBackType<T>
  ) => {
    console.debug(`on`, event, callback);
    await this._onInternal(event, callback);
  };

  isOn = (event: string) => {
    console.debug(`isOn`, event);
    return this._onEvents.has(event);
  };

  off = async (event: string) => {
    console.debug(`off`, event);
    await this._offInternal(event);
  };

  private _sendInternal = async <
    T extends WebSocketBrokerRequiredData
  >(
    event: string,
    data: T
  ) => {
    console.debug("this._sendInternal", event, data);
    if (!WebSocketBroker._socket) {
      console.warn(
        `Attempting to send ${event} without a socket.`
      );
      return;
    }
    WebSocketBroker._socket!.emit(event, data);
  };

  private _onInternal = async <
    T extends WebSocketBrokerRequiredData
  >(
    event: string,
    callback: EventsCallBackType<T>
  ) => {
    console.debug("_onInternal", event, callback);
    if (!WebSocketBroker._socket) {
      console.warn(
        `Attempting to listen for ${event} without a socket.`
      );
      return;
    }

    if (this.isOn(event)) {
      console.warn(
        `Unable to register event ${event} because it is already on.`
      );
      return;
    }

    console.debug(`Listening for ${event}`);
    this._onEvents.set(event, callback);
    WebSocketBroker._socket.on(event, (data: T) => {
      console.debug(
        `Received ${event} with data ${JSON.stringify(
          data
        )}`
      );
      callback(data);
    });
  };

  private _offInternal = async (event: string) => {
    console.debug(`Stop listening for event ${event}`);
    WebSocketBroker._socket!.off(event);
    this._onEvents.delete(event);
  };

  public dispose = () => {
    this._disposeSocket();
  };

  private _disposeSocket = () => {
    if (WebSocketBroker._socket) {
      WebSocketBroker._socket.disconnect();
      WebSocketBroker._socket = undefined;
    }
  };
}
```

# `tsconfig.json`

Configuration for TypeScript compiler.

```json
{
  "compilerOptions": {
    "allowJs": true,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "isolatedModules": true,
    "jsx": "react",
    "lib": ["es6"],
    "moduleResolution": "node",
    "noEmit": true,
    "strict": true,
    "target": "esnext"
  },
  "exclude": [
    "node_modules",
    "babel.config.js",
    "metro.config.js",
    "jest.config.js"
  ]
}
```

`package.json`: NPM project definition

```json
{
  "name": "broker",
  "version": "1.0.0",
  "scripts": {
    "start": "npx ts-node server.ts"
  },
  "dependencies": {
    "@types/express": "^4.17.11",
    "express": "^4.17.1",
    "npx": "^10.2.2",
    "socket.io": "^3.1.0",
    "ts-node": "^9.1.1",
    "typescript": "^4.1.3"
  }
}
```

# `Procfile`

For deployment to Heroku.

```
web: npm start
```
