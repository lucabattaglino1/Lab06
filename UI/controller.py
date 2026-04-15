import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_hello(self, e):
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()

    def fillddAnno(self):
        for y in self._model.getYear():
             self._view.ddAnno.options.append(
                 ft.dropdown.Option(y))

    def fillddBrand(self):
        for b in self._model.getBrand():
             self._view.ddBrand.options.append(
                 ft.dropdown.Option(b))


    def fillddRetailer(self):
        self._retailerMap = {}

        for r in self._model.getRetailers():
            self._view.ddRetailer.options.append(ft.dropdown.Option(
                key = r.retailer_code, # stringa che viene visualizzata nel menu
                text=str(r)
            ))
            self._retailerMap[r.retailer_code] = r  # salvo oggetto
        self._view.ddRetailer.on_change = self._choiceDDRetailers

    def _choiceDDRetailers(self, e):
        selected_key = e.control.value
        self._ddRetailersValue = self._retailerMap[selected_key]

        print(self._ddRetailersValue)

    # PUNTO 2
    def handleTopVendite(self, e):

        # leggo i valori dalla view e leggo ciò che ha selezionato l'utente
        year = self._view.ddAnno.value
        brand = self._view.ddBrand.value
        retailer_key = self._view.ddRetailer.value

        # sistemiamo i valori
        if year == "None":
            year = None
        else:
            year = int(year)

        if brand == "None":
            brand = None

        # retailer_key è la chiave del dropdown
        # perciò con la mappa recupero l'oggetto e poi prendo il codice
        retailer = None
        if retailer_key != "None":
            retailer = self._retailerMap[retailer_key].retailer_code

        # chiamo il model
        risultati = self._model.getTopVendite(year, brand, retailer)

        # pulisco
        self._view.txt_result.controls.clear()

        # stampo i risultati
        for r in risultati:
            self._view.txt_result.controls.append(
                ft.Text(f"{r['date']} - {r['product_brand']} - {r['retailer_name']} - {r['ricavo']}")
            )

        self._view.update_page()

    # PUNTO 3
    def handleAnalizzaVendite(self, e):

        # leggo i valori dalla view e leggo ciò che ha selezionato l'utente
        year = self._view.ddAnno.value
        brand = self._view.ddBrand.value
        retailer_key = self._view.ddRetailer.value

        # sistemiamo i valori
        if year == "None":
            year = None
        else:
            year = int(year) #converto perché arriva come stringa

        if brand == "None":
            brand = None

        retailer = None
        if retailer_key != "None":
            retailer = self._retailerMap[retailer_key].retailer_code

        # chiamata model
        res = self._model.getAnalisiVendite(year, brand, retailer)

        # pulisco
        self._view.txt_result.controls.clear()

        # stampa risultati ovvero ogni statistica
        self._view.txt_result.controls.append(ft.Text("Statistiche vendite:\n"))

        self._view.txt_result.controls.append(
            ft.Text(f"Giro d'affari: {res['totale']}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero vendite: {res['num_vendite']}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero retailers coinvolti: {res['num_retailer']}")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Numero prodotti coinvolti: {res['num_prodotti']}")
        )

        self._view.update_page()