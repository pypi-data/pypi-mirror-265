import os.path
import random
import json
import pprint

class ScriptToFile:
    def __init__(self, steps_data, path=None):
        self.context_frame = 'ROOT'
        self.nombre_archivo = 'LoginPrueba'
        self.steps_data = steps_data
        self.output_folder = os.path.abspath(os.path.join(os.getcwd(), "output"))
        self.scripts_folder = os.path.abspath(os.path.join(os.getcwd(), "output/scripts"))
        self.evidence_folder = os.path.abspath(os.path.join(os.getcwd(), "output/screenshots"))

    def main(self):
        self.create_output_folder()
        self.create_scripts_folder()
        self.generate_script()

    ############################################# OUTPUT FOLDER ########################################################
    def create_output_folder(self):
        """
            Returns:
                Crea la carpeta donde se guardara el archivo .py (SERA DEPRECADO)
        """
        try:
            if os.path.exists(self.output_folder) is False:
                os.mkdir(self.output_folder)
        except Exception as error:
            print(f"Exception: {error}, ha ocurrido")

    ############################################# SCRIPTS FOLDER #######################################################
    def create_scripts_folder(self):
        """
            Returns:
                Crea la carpeta donde se guardara el archivo .py (SERA DEPRECADO)
        """
        try:
            if os.path.exists(self.scripts_folder) is False:
                os.mkdir(self.scripts_folder)
        except Exception as error:
            print(f"Exception: {error}, ha ocurrido")

    ############################################ STEPS #################################################################
    def generate_script(self):
        """
            Returns:
                Genera un archivo .py con el script de la automatización.
        """
        json_objects = self.build_json_objects()
        formatted_json = json.dumps(json_objects, indent=4)
        steps_list = ["from Andreani_QA_Selenium.Selenium import Selenium", "",
                                  f"Selenium.json_strings ={formatted_json}"]
        for step in self.steps_data:
            if step["event"] == "url log":
                steps_list += self.build_step_open_browser(step)
            if step["event"] == "click":
                steps_list += self.build_step_click_element(step, json_objects)
            if step["event"] == "input":
                steps_list += self.build_step_write_in_element(step, json_objects)
            if step["event"] == "screenshot":
                steps_list += self.build_step_screenshot(step)
        file_path = rf'{self.scripts_folder}\{self.nombre_archivo}.py' # escritura del archivo
        with open(file_path, 'w', encoding="UTF-8") as script_file:
            for step_line in steps_list:
                script_file.write(step_line + '\n')
            script_file.close()
        print(f"Script generado en... '{file_path}'")

    def build_step_open_browser(self, step: dict):
        """
            Args:
                step (dict): Metadatos del step capturado.
            Returns:
                Procesa las acciones de apertura de navegador en una lista.
        """
        return [f"Selenium.open_browser(Selenium, \"{step['target']}\")"]

    def build_step_click_element(self, step: dict, json_objects: dict):
        """
            Args:
                step (dict): Metadatos del step capturado.
                json_objects (dict): Repositorio de objetos.

            Returns:
                Procesa las acciones de click en una lista.
        """
        actions = []
        if step["target"]["FRAME"] != self.context_frame and step["target"]["FRAME"] == "ROOT":
            self.context_frame = "ROOT"
            actions = [f"Selenium.switch_to_default_frame(Selenium)"]
        if step["target"]["FRAME"] != self.context_frame and step["target"]["FRAME"] != "ROOT":
            self.context_frame = step["target"]["FRAME"]
            name_object = self.get_name_object(step["target"]["FRAME"], json_objects)
            actions = [f"Selenium.switch_to_iframe(Selenium, \"{name_object}\")"]
        name_object = self.get_name_object(step["target"]["XPATH"], json_objects)
        actions.append(f"Selenium.get_element(Selenium, \"{name_object}\").click()")
        return actions

    def build_step_write_in_element(self, step, json_objects):
        """
            Args:
                step (dict): Metadatos del step capturado.
                json_objects (dict): Repositorio de objetos.

            Returns:
                Procesa las acciones de escritura en una lista.
        """
        actions = []
        if step["target"]["FRAME"] != self.context_frame and step["target"]["FRAME"] == "ROOT":
            self.context_frame = "ROOT"
            actions = [f"Selenium.switch_to_default_frame(Selenium)"]
        if step["target"]["FRAME"] != self.context_frame:
            self.context_frame = step["target"]["FRAME"]
            name_object = self.get_name_object(step["target"]["FRAME"], json_objects)
            actions = [f"Selenium.switch_to_iframe(Selenium, \"{name_object}\")"]
        name_object = self.get_name_object(step["target"]["XPATH"], json_objects)
        actions.append(f"Selenium.get_element(Selenium, \"{name_object}\").send_keys(\"{step['value']}\")")
        return actions

    def build_step_screenshot(self, step):
        """
            Returns:
                Procesa las acciones screenshot en una lista.
        """
        return [f"Selenium.screenshot(Selenium, '{step['value']}')"]

    def build_json_objects(self):
        """
            Returns:
                Archivo json que funciona como repositorio de objetos a partir de los steps recibidos.
        """
        json_objects = {}
        for step in self.steps_data:
            if not step["event"] in ["url log", "screenshot"]:
                if json_objects == {}:
                    json_objects.update(self.build_object(step["target"]["TAGNAME"],
                                                          step["target"]["XPATH"],
                                                          step["target"]["FRAME"]))
                    if step["target"]["FRAME"] != 'ROOT':
                        json_objects.update(self.build_object("<iframe>",
                                                              step["target"]["FRAME"],
                                                              "ROOT"))
                else:
                    object_in_json = False
                    for key, value in json_objects.items():
                        if (value["ValueToFind"] == step["target"]["XPATH"]
                                and value["Frame"] == step['target']['FRAME']):
                            object_in_json = True
                            break
                    if object_in_json is False:
                        json_objects.update(self.build_object(step["target"]["TAGNAME"],
                                                              step["target"]["XPATH"],
                                                              step["target"]["FRAME"]))

        return json_objects

    def get_name_object(self, xpath_object: str, json_objects: dict):
        """
            Args:
                xpath_object (str): xpath del objeto objetivo.
                json_objects (dict): Repositorio de objetos.

            Returns:
                Nombre de un objeto obtenido a patir de la lista de objetos.
        """
        for key, value in json_objects.items():
            if value["ValueToFind"] == xpath_object:
                return key

    @staticmethod
    def build_object(tag_name, xpath, frame):
        """
            Args:
                tag_name (str): tag name del objeto.
                xpath (str): xpath del objeto objetivo.
                frame (str): xpath del frame contenedor del objeto objetivo.

            Returns:
                un objeto json con formato pybot.".
        """
        object_element = {}
        object_name = f"{tag_name}_{random.randint(1, 5000)}"  # mejorar esto
        object_element[object_name] = {
            "GetFieldBy": "Xpath",
            "ValueToFind": f"{xpath}",
            "Frame": f"{frame}"
        }
        return object_element

if __name__ == "__main__":
    my_json =   [
                  {
                    "event": "url log",
                    "target": "https://www.google.com/",
                    "value": "https://www.google.com/",
                    "frame": None,
                    "order": 1
                  },
                  {
                    "event": "click",
                    "target": {
                      "TAGNAME": "<button>",
                      "XPATH": "//button[contains(text(),\"NO, GRACIAS\")]",
                      "FRAME": "//iframe[@name=\"callout\"]",
                      "QUALITY": 2
                    },
                    "value": None,
                    "frame": "//iframe[@name=\"callout\"]",
                    "order": 2
                  },
                  {
                    "event": "click",
                    "target": {
                      "TAGNAME": "<textarea>",
                      "XPATH": "//textarea[@id=\"APjFqb\"]",
                      "FRAME": "ROOT",
                      "QUALITY": 3
                    },
                    "value": None,
                    "frame": "ROOT",
                    "order": 3
                  },
                  {
                    "event": "input",
                    "target": {
                      "TAGNAME": "<textarea>",
                      "XPATH": "//textarea[@id=\"APjFqb\"]",
                      "FRAME": "ROOT",
                      "QUALITY": 3
                    },
                    "value": "testing",
                    "frame": "ROOT",
                    "order": 4
                  },
                  {
                    "event": "click",
                    "target": {
                      "TAGNAME": "<input>",
                      "XPATH": "//div[@class=\"FPdoLc lJ9FBc\"]//input[@name=\"btnK\"]",
                      "FRAME": "ROOT",
                      "QUALITY": 1
                    },
                    "value": None,
                    "frame": "ROOT",
                    "order": 5
                  }
                ]
    ScriptToFile(my_json).main()