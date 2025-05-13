import {type FC, useContext, useEffect, useState} from "react";
import {AppContext} from '../../AppContext';
import {type MessageEvent, messageEventSchema} from "./MessageEvent";

export const Chat: FC = () => {
  const {env} = useContext(AppContext);
  const [messageEvents, updateMessageEvents] = useState<MessageEvent[]>([]);

  useEffect(() => {
    const chatEventSource = new EventSource(`${env?.serverHost}/api/events`);

    chatEventSource.addEventListener('chat', event => {
      const messageEvent = messageEventSchema.decode(JSON.parse(event.data));

      if (messageEvent) {
        const {id, voice, message} = messageEvent;

        updateMessageEvents((current: MessageEvent[]) => {
          const lastMessageEvent: MessageEvent = current[current.length - 1];
          if (lastMessageEvent?.voice === voice) {
            return [...current.slice(0, -1), {id, voice, message: lastMessageEvent.message + message}];
          } else return [...current, {id, voice, message}];
        });

      } else {
        updateMessageEvents([{id: '-1', voice: 'server', message: `Wrong format from backend: ${event.data}`}]);
      }
    });
  }, [env?.serverHost])

  return <ul>
    {messageEvents.map(({id, voice, message}) =>
      <li key={id}>
        <label>{voice}:<input type="text" readOnly={true} value={message}/></label>
      </li>)}
  </ul>
}