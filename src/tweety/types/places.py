from .twDataTypes import Place


class Places(dict):
    def __init__(self, client, lat, long, search_term):
        super().__init__()
        self.lat = lat
        self.client = client
        self.long = long
        self.search_term = search_term
        self.results = []
        self.get_page()

    def get_page(self):
        if all(value is None for value in [self.lat, self.long, self.search_term]):
            raise ValueError("Either 'lat' and 'long' OR 'search_term' is Required")

        _results = []
        response = self.client.http.search_place(self.lat, self.long, self.search_term)

        for place in response.get('places', []):
            _results.append(Place(self.client, place))

        self.results = _results

    def __repr__(self):
        return "Places(results={})".format(len(self.results))

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.results[index]

    def __iter__(self):
        for i in self.results:
            yield i

    def __len__(self):
        return len(self.results)



