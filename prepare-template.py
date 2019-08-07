import os


def main():
    websocket_port = os.environ.get('WEBSOCKET_PORT', '5678')
    with open('/app/server/client.html', 'r') as f:
        text = f.read()
    text = text.replace(r'{{WEBSOCKET_PORT}}', websocket_port)
    with open('/app/server/client.html', 'w') as f:
        f.write(text)


if __name__ == '__main__':
    main()
