import http, {type IncomingMessage, type Server, type ServerResponse} from "node:http";
import type {AddressInfo} from "node:net";

export type TestServer = ReturnType<typeof createTestServer>;

export const createTestServer = () => {
  let events: string[] = [];
  let eventName: string;
  let pathname: string;
  let server: Server;

  const listener = (req: IncomingMessage, res: ServerResponse) => {
    if (req.url === pathname) {
      res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
      });

      events.forEach(event => {
        res.write(`event: ${eventName}\ndata: ${event}\n\n`)
      });

      req.on('close', () => {
        res.end();
      });
    } else {
      throw new Error(`unknown path: ${req.url}`);
    }
  };

  return {
    create: () => {
      server = http.createServer(listener).listen(0)
    },
    url: () => {
      const address = server.address() as AddressInfo;
      return `http://localhost:${address.port}`;
    },
    stubEventStream: <T>(path: string, name: string, serverEvents: T[]) => {
      pathname = path;
      eventName = name;
      events = serverEvents.map(event => JSON.stringify(event));
    },
    close: () => server.close(),
  };
}
