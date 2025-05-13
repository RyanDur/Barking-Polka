import {render, screen} from "@testing-library/react";
import {expect} from "vitest";
import App from "../App";
import {createTestServer} from "./testServer";

describe('group chat', () => {
  const server = createTestServer();

  beforeEach(() => {
    server.create();
  });

  afterEach(() => {
    server.close();
  });

  test('when receiving a chat', async () => {
    server.stubEventStream('/api/events', 'chat', [
      {voice: 'friend', message: 'hello,', id: '1'},
      {voice: 'friend', message: ' how are you?', id: '2'}
    ])
    render(<App env={{serverHost: server.url()}}/>)

    expect((await screen.findByLabelText('friend:'))).toHaveValue('hello, how are you?');
  });

  test('when receiving chats from multiple users', async () => {
    server.stubEventStream('/api/events', 'chat', [
      {voice: 'friend 1', message: 'hello,', id: '1'},
      {voice: 'friend 1', message: ' how are you?', id: '2'},
      {voice: 'friend 2', message: 'I am good.', id: '3'}
    ])
    render(<App env={{serverHost: server.url()}}/>)

    expect((await screen.findByLabelText('friend 1:'))).toHaveValue('hello, how are you?');
    expect((await screen.findByLabelText('friend 2:'))).toHaveValue('I am good.');
  });

  test('when receiving data in the wrong format', async () => {
    const badlyFormedMessageEvent = {wrong: 'friend 1', format: 'hello,'};
    server.stubEventStream('/api/events', 'chat', [badlyFormedMessageEvent])

    render(<App env={{serverHost: server.url()}}/>);

    expect((await screen.findByLabelText('server:'))).toHaveValue(`Wrong format from backend: ${JSON.stringify(badlyFormedMessageEvent)}`);
  });
});