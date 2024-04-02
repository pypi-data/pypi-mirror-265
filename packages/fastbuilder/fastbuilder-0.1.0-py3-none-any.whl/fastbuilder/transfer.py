import os
import shutil
import subprocess

from bs4 import BeautifulSoup
from colorama import Fore

from .frontend_template import react_template, solidjs_template, vue_template


class FrontendBuildProcessor:
    def __init__(
        self,
        client_build_path,
        fastapi_static_path,
        fastapi_templates_path,
        document_name,
        frontend_path,
    ):
        self.client_build_path = client_build_path
        self.fastapi_static_path = fastapi_static_path
        self.fastapi_templates_path = fastapi_templates_path
        self.document_name = document_name
        self.frontend_path = frontend_path

    def is_node_installed(self):
        try:
            # Versuche, die Node.js Version abzurufen
            result = subprocess.run(
                ["node", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            # Wenn der Befehl erfolgreich war, überprüfe, ob die Ausgabe eine Version enthält
            if result.returncode == 0 and result.stdout.startswith("v"):
                print(
                    Fore.BLUE
                    + f"Node.js is installed. version: {result.stdout.strip()}"
                )
                return True
            else:
                print(Fore.RED + "Node.js is not installed. you need to install nodejs")
                return False
        except Exception as e:
            print(Fore.RED + f"An error has occurred: {e}")
            return False

    def run_build_command(self):
        node_modules_path = os.path.join(self.frontend_path, "node_modules")
        if not os.path.exists(node_modules_path) or not os.path.isdir(
            node_modules_path
        ):
            subprocess.run(["npm", "i"], cwd=self.frontend_path, check=True, shell=True)
            subprocess.run(
                ["npm", "run", "build"], cwd=self.frontend_path, check=True, shell=True
            )
            return True
        else:
            subprocess.run(
                ["npm", "run", "build"], cwd=self.frontend_path, check=True, shell=True
            )

    def transfer(self, frontend_templates):
        if self.is_node_installed():
            if os.path.isdir(self.frontend_path):
                pass
            else:
                if frontend_templates == "React":
                    subprocess.run(
                        ["npx", "create-react-app", str(self.frontend_path)],
                        check=True,
                        shell=True,
                    )

                if frontend_templates == "Solidjs":
                    subprocess.run(
                        [
                            "npx",
                            "degit",
                            "solidjs/templates/js",
                            str(self.frontend_path),
                        ],
                        check=True,
                        shell=True,
                    )

                if frontend_templates == "Vue":
                    subprocess.run(
                        ["npm", "create", "vue@latest", str(self.frontend_path)],
                        check=True,
                        shell=True,
                    )

            if not os.path.exists(self.client_build_path):
                self.run_build_command()

            if not os.path.exists(self.fastapi_static_path):
                os.makedirs(self.fastapi_static_path)

            if not os.path.exists(self.fastapi_templates_path):
                os.makedirs(self.fastapi_templates_path)

            if frontend_templates == "React":
                static_dir = os.path.join(self.client_build_path, "static")
                if os.path.exists(static_dir) and os.path.isdir(static_dir):
                    for item in os.listdir(static_dir):
                        source_item = os.path.join(static_dir, item)
                        destination_item = os.path.join(self.client_build_path, item)
                        shutil.move(source_item, destination_item)
                        print(
                            Fore.GREEN
                            + f" {item} erfolgreich verschoben und static folder gelöscht wurden"
                        )
                shutil.rmtree(static_dir)

            if frontend_templates == "Vue" or frontend_templates == "Solidjs":
                static_dir = os.path.join(self.client_build_path, "assets")
                if os.path.exists(static_dir) and os.path.isdir(static_dir):
                    for item in os.listdir(static_dir):
                        source_item = os.path.join(static_dir, item)
                        destination_item = os.path.join(self.client_build_path, item)
                        shutil.move(source_item, destination_item)
                        print(
                            Fore.GREEN
                            + f"{item} erfolgreich verschoben und static folder gelöscht wurden"
                        )
                shutil.rmtree(static_dir)

            for item in os.listdir(self.client_build_path):
                source_item = os.path.join(self.client_build_path, item)
                destination_item = os.path.join(self.fastapi_static_path, item)

                if os.path.isdir(source_item):
                    shutil.copytree(source_item, destination_item)
                    print(Fore.GREEN + f"{item} erfolgreich verschoben.")
                elif item == "index.html":
                    with open(source_item, "r") as file:
                        content = file.read()

                    soup_template = BeautifulSoup(content, "html.parser")
                    css_link = soup_template.find("link", rel="stylesheet")
                    js_script = soup_template.find("script", src=True)
                    favicon_link = soup_template.find("link", rel="icon")

                    if css_link and js_script and favicon_link:
                        css_file_name = os.path.basename(css_link["href"])
                        js_file_name = os.path.basename(js_script["src"])
                        favicon_file_name = os.path.basename(favicon_link["href"])

                        if frontend_templates == "React":
                            formatted_content = react_template.format(
                                document_name=self.document_name,
                                js_file_name=js_file_name,
                                css_file_name=css_file_name,
                                favicon_file_name=favicon_file_name,
                            )
                        elif frontend_templates == "Vue":
                            formatted_content = vue_template.format(
                                document_name=self.document_name,
                                js_file_name=js_file_name,
                                css_file_name=css_file_name,
                                favicon_file_name=favicon_file_name,
                            )
                        elif frontend_templates == "Solidjs":
                            formatted_content = solidjs_template.format(
                                document_name=self.document_name,
                                js_file_name=js_file_name,
                                css_file_name=css_file_name,
                                favicon_file_name=favicon_file_name,
                            )
                        index_file_path = os.path.join(
                            self.fastapi_templates_path, "index.html"
                        )
                        with open(index_file_path, "w") as index_file:
                            index_file.write(formatted_content)
                            print(f"{index_file_path} erfolgreich erstellt.")
                    else:
                        print(
                            Fore.RED + "CSS-Link oder Javascript-Skript nicht gefunden."
                        )
                elif os.path.isfile(source_item):  # Check if it's a file before copying
                    shutil.copy(source_item, destination_item)
                    print(Fore.GREEN + f"{item} erfolgreich verschoben.")
                else:
                    print(
                        Fore.RED + f"{item} ist weder ein Verzeichnis noch eine Datei."
                    )

            return shutil.rmtree(self.client_build_path)
