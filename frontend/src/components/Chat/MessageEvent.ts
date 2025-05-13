import type {Decoder} from "schemawax";
import * as schema from 'schemawax';

export type MessageEvent = {
  voice: string,
  message: string,
  id: string,
}

export const messageEventSchema: Decoder<MessageEvent> = schema.object({
  required: {
    voice: schema.string,
    message: schema.string,
    id: schema.string,
  }
})
