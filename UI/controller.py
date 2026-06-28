import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._storeValue = None

    def fillDDStore(self):
        allStores = self._model.getAllStores()
        ddoptions = list(map(lambda x: ft.dropdown.Option(data=x, key=x.store_name, on_click=self._choiceStore), allStores))
        self._view._ddStore.options = ddoptions
        self._view.update_page()

    def _choiceStore(self,e):
        self._storeValue = e.control.data



    def handleCreaGrafo(self, e):
        k = self._view._txtIntK.value
        kint = int(k)
        self._model.buildGraph(self._storeValue, kint)
        allNodes = self._model.getAllNodes()
        self.fillDD(allNodes)
        self._view._ddNode.disabled = False
        self._view._btnCerca.disabled = False
        self._view._btnRicorsione.disabled = False
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        Nnodes, Nedges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi:{Nnodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi:{Nedges}"))
        top5 = self._model.getTop5Edges()
        self._view.txt_result.controls.append(ft.Text("Top 5 edges:"))
        for arco in top5:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]} -> {arco[1]} (peso: {arco[2]["weight"]})"))
        self._view.update_page()




    def handleCerca(self, e):
        if self._view._ddNode.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare nodo di partenza."))
            self._view.update_page()
            return
        nodes = self._model.getCammino(self._view._ddNode.value)

        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza : {self._view._ddNode.value}"))
        for n in nodes:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

    def handleRicorsione(self, e):
        bestpath, bestscore = self._model.bestPath(self._view._ddNode.value)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Trovato un cammino che parte da {self._view._ddNode.value} "
                    f"con somma dei pesi uguale a {bestscore}."))

        print(bestpath)
        for v in bestpath:
            self._view.txt_result.controls.append(ft.Text(f"{v}"))
        self._view.update_page()

    def fillDD(self, allNodes):
        self._view._ddNode.options.clear()
        for n in allNodes:
            self._view._ddNode.options.append(
                ft.dropdown.Option(n))