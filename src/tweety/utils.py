def custom_json(self):
    try:
        return self.json()
    except:
        return None
