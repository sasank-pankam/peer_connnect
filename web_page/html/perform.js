const socket = new WebSocket('ws://localhost:12345');

socket.addEventListener('open', (event) => {
    console.log('WebSocket connection established.');
});

socket.addEventListener('message', (event) => {
    const message = event.data;
    console.log('Message from server:', message);
    for (let i = 0; i < 100; i++) {
        socket.send('Hello, Server! '+i);
    }
});

socket.addEventListener('close', (event) => {
    if (event.wasClean) {
        console.log(`Closed cleanly, code=${event.code}, reason=${event.reason}`);
    } else {
        console.error('Connection abruptly closed');
    }
});

socket.addEventListener('error', (error) => {
    console.error('WebSocket Error:', error);
});


