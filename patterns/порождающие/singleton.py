class App():
    """
    Возвращает только один экземпляр класса
    """
    __instance = None

    @staticmethod
    def get_instance():
        if App.__instance is None:
            App.__instance = App()
        return App.__instance


print(App.get_instance(), App.get_instance())


