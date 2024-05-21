class CliffDetection:

    picarx = None
    current_state = None

    def __init__(self, _picarx):
        self.picarx = _picarx
        # px = Picarx(grayscale_pins=['A0', 'A1', 'A2'])
        # manual modify reference value
        self.picarx.set_cliff_reference([200, 200, 200])

    def periodic(self):
        try: # Idk why this is here its from the Guide, but if it stops something from breaking, I'm not gonna touch it        
            gm_val_list = self.picarx.get_grayscale_data()
            gm_state = self.picarx.get_cliff_status(gm_val_list)
            self.picarx.cliffDetection(gm_state)
        finally:
            pass