import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        punteggi = self._model.getRatings()
        self._view._ddrating1.options.clear()
        self._view._ddrating2.options.clear()
        for punteggio in punteggi :
            self._view._ddrating1.options.append(ft.dropdown.Option(key=punteggio , text=punteggio ))
            self._view._ddrating2.options.append(ft.dropdown.Option(key=punteggio, text=punteggio))

        pass

    def handleCreaGrafo(self, e):
        try:
            avg1 = int(self._view._ddrating1.value)
            avg2 = int(self._view._ddrating2.value)
            val1 = min(avg1,avg2)
            val2 = max(avg1,avg2)
            self._model.buildGrafo(val1,val2)
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"grafo correttamente creato! \nContiene {self._model.getNumNodi()} nodi e {self._model.getNumArchi()} archi. "))

            self._view.update_page()
            self._view.txt_result.controls.append(ft.Text(f"i 5 archi con peso maggiore :  "))
            for arco in self._model.getTop5ArchiPeso():
                self._view.txt_result.controls.append(ft.Text(f" {arco[0]} ---- {arco[1]} , peso : {arco[2]['weight']}"))
            self._view.update_page()

            num,list_comp=self._model.getCompConnessa()
            self._view.txt_result.controls.append(ft.Text(f" il numero di componenti connesse è {num} \n è formata da : {list_comp}  "))
            self._view.update_page()





        except ValueError as e:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"errore {e}"))
            self._view.update_page()
        pass

    def handleCammino(self, e):
        pass