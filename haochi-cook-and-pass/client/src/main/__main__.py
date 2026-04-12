import asyncio
import pygame
import websockets
import threading
from queue import Queue

msg_queue = Queue()

async def websocket_client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("client connected")
        async for message in websocket:
            print(f"received: {message}")
            msg_queue.put(message)

def start_network():
    asyncio.run(websocket_client())

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Haochi Cook and Pass")
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Process messages from the server
        while not msg_queue.empty():
            msg = msg_queue.get()
            # Handle the message (e.g., update game state)
            print(f"Processing message: {msg}")
        pygame.display.flip()
        clock.tick(60) # Limit to 60 FPS
    pygame.quit()

if __name__ == "__main__":
    threading.Thread(target=start_network, daemon=True).start()
    start_game()
