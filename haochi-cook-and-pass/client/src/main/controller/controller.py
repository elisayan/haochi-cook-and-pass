
class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        running = True
        while running:
            #Si prendono dalla view gli eventi che sono stati effettuati dall'utente
            events = self.view.get_events()

            for event in events:
                if event["type"] == "QUIT":
                    running = False
                elif event["type"] == "CLICK":
                    self.model.gestisci_pressione(event["pos"])
                elif event["type"] == "RELEASE":
                    self.model.gestisci_rilascio()

            #Aggiornamento del model in base alla posizione del mouse  
            # cambio posizione e se sto spostando l'elemento sul piatto
            mouse_pos = self.view.get_mouse_pos()
            self.model.update(mouse_pos, self.view.width, self.view.height)

             # Rendering
            self.view.draw_game(self.model.plate, self.model.ingredients, self.model.current_recipe)#, self.model.list_recipe)

