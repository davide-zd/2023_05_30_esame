import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._retailer_selezionato = None

    # popolo i due dropdown
    def fillDD_year(self):
        lista_anni = self._model.fillDD_Anni()
        self._view.ddyear.options.clear()

        for a in lista_anni:
            self._view.ddyear.options.append(ft.dropdown.Option(
                text=a))
        self._view.update_page()

    def fillDD_country(self):
        lista_paesi = self._model.fillDD_Nazioni()
        self._view.ddcountry.options.clear()

        for a in lista_paesi:
            self._view.ddcountry.options.append(ft.dropdown.Option(
                text=a))
        self._view.update_page()

    #creo il grafo
    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        numero = self._view.txtNumero.value
        anno = self._view.ddyear.value
        nazione = self._view.ddcountry.value

        # se è un dropdown --> is None, altrimenti ""
        if (anno is None):
            self._view.txt_result.controls.append(ft.Text("Devi selezionare un anno dal menù."))
            self._view.update_page()
            return
        if (nazione is None):
            self._view.txt_result.controls.append(ft.Text("Devi selezionare una nazione dal menù."))
            self._view.update_page()
            return
        if (numero == ""):
            self._view.txt_result.controls.append(ft.Text("Devi scrivere un numero nella casella di testo."))
            self._view.update_page()
            return
        try:
            numero = int(numero)
        except:
            self._view.txt_result.controls.append(ft.Text("Deve essere un numero intero."))
            self._view.update_page()
            return
        if (numero < 0):
            self._view.txt_result.controls.append(ft.Text("Deve essere un numero positivo."))
            self._view.update_page()
            return

        # creo il grafo e i dettagli
        self._model.creaGrafo(nazione, numero, anno)
        n, e = self._model.graphDetails()

        self.fillDD_rivenditori()

        # stampo i nodi e gli archi
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {n} nodi e {e} archi."))
        self._view.update_page()

        lista_nodi = self._model._grafo.nodes
        for n in lista_nodi:
            self._view._txtOut.controls.append(ft.Text(f"{n.nome}"))
        self._view.update_page()

        lista_archi_ordinata = self._model.getArchiOrdinati()
        for a in lista_archi_ordinata:
            self._view._txtOut2.controls.append(ft.Text(f"Peso: {a[2]['weight']} - {a[0]} <-> {a[1]}"))
        self._view.update_page()

    def fillDD_rivenditori(self):
        lista_retailer = self._model.fillDD_Retailer()
        self._view.dd_riventitori.options.clear()

        for a in lista_retailer:
            self._view.dd_riventitori.options.append(ft.dropdown.Option(
                text=a.nome,
                data=a,
                on_click=self.read_DD_retailer
            ))
        self._view.update_page()

    def read_DD_retailer(self, e):
        if e.control.data is None:
            self._retailer_selezionato = None
        else:
            self._retailer_selezionato = e.control.data


    def handle_analizza(self, e):
        dimensione, somma_peso = self._model.getCompConnessa(self._retailer_selezionato)
        self._view.txt_result.controls.append(ft.Text(f"La componenete connessa di {self._retailer_selezionato} ha dimensione: {dimensione}"))
        self._view.txt_result.controls.append(ft.Text(f"Il peso totale degli archi della componente connessa è {somma_peso}"))
        self._view.update_page()

    def handle_path(self, e):
        pass
