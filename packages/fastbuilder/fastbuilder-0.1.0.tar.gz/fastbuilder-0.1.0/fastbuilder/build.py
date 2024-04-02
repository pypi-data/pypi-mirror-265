import importlib
import os
import pathlib
import sys
from typing import Literal

from colorama import Fore

from .transfer import FrontendBuildProcessor


class Build:
    def __init__(
        self,
        executable_name: str,
        app_path: str,
        console: bool = True,
    ):
        self.app_path = pathlib.Path(app_path)
        self.app_name = self.app_path.stem
        self.workdir = pathlib.Path("out").absolute()
        self.workdir.mkdir(exist_ok=True)
        self.pyinstallercommands = []
        self.uvicorn_packages = [
            "uvicorn.lifespan.off",
            "uvicorn.lifespan.on",
            "uvicorn.lifespan",
            "uvicorn.protocols.websockets.auto",
            "uvicorn.protocols.websockets.wsproto_impl",
            "uvicorn.protocols.websockets.websockets_impl",
            "uvicorn.protocols.http.auto",
            "uvicorn.protocols.http.h11_impl",
            "uvicorn.protocols.http.httptools_impl",
            "uvicorn.protocols.websockets",
            "uvicorn.protocols.http",
            "uvicorn.protocols",
            "uvicorn.loops.auto",
            "uvicorn.loops.asyncio",
            "uvicorn.loops.uvloop",
            "uvicorn.loops",
            "uvicorn.logging",
            "aap.server.log",
        ]
        self.executable = executable_name

        self.console = console
        self.truetype = True

        if self.console == self.truetype:
            self.pyinstallercommands.append("--console")
        else:
            print(
                Fore.RED
                + """\n
                you musst set the console to True (Build(executable_name="server", app_path="main.py", console=True)) or usage\n
                from webbuilder import uvicorn_with_logging_file\n\n\n\n

                from multiprocessing import freeze_support\n
                from pathlib import Path\n
                from webbuilder import uvicorn_with_logging_file\n
                from fastapi import FastAPI, Request, Response\n
                from fastapi.responses import HTMLResponse\n
                from fastapi.staticfiles import StaticFiles\n
                from fastapi.templating import Jinja2Templates\n\n\n\n\n\n


                app = FastAPI()\n\n\n\n

                project_path = Path(__file__).parent\n
                templates = Jinja2Templates(project_path / "templates")\n\n\n\n

                static_files = StaticFiles(
                    directory=(project_path / "static").resolve(),
                    follow_symlink=True,
                )\n\n\n\n
                app.mount("/static", static_files, name="static")\n\n\n\n\n


                @app.get("/", response_class=HTMLResponse)\n
                async def read_item(request: Request):\n
                    prefix = request.headers.get(\n
                        "X-Forwarded-Prefix", request.scope.get("root_path", "")\n
                    )\n
                    return templates.TemplateResponse(\n
                        "index.html", {"request": request, "prefix": prefix}\n
                    )\n\n\n\n\n\n\n

                if __name__ == "__main__":\n\n
                    freeze_support()\n\n
                    uvicorn_with_logging_file(app=app, app_path=project_path)\n\n

                """
            )

    def build_static_files(
        self,
        framework: str,
        document_name: str,
        frontend_folder: str,
        static: str,
        template: str,
    ):
        build = self.app_path.parent / str(frontend_folder) / "build"
        dist = self.app_path.parent / str(frontend_folder) / "dist"
        fastapi_static = self.app_path.parent / str(static)
        fastapi_templates = self.app_path.parent / str(template)

        react_build = FrontendBuildProcessor(
            client_build_path=build,
            fastapi_static_path=fastapi_static,
            fastapi_templates_path=fastapi_templates,
            document_name=document_name,
            frontend_path=frontend_folder,
        )
        vue_build = FrontendBuildProcessor(
            client_build_path=dist,
            fastapi_static_path=fastapi_static,
            fastapi_templates_path=fastapi_templates,
            document_name=document_name,
            frontend_path=frontend_folder,
        )
        solidjs_build = FrontendBuildProcessor(
            client_build_path=dist,
            fastapi_static_path=fastapi_static,
            fastapi_templates_path=fastapi_templates,
            document_name=document_name,
            frontend_path=frontend_folder,
        )

        if framework == "React":
            react_build.transfer(frontend_templates="React")
        if framework == "Vue":
            vue_build.transfer(frontend_templates="Vue")
        if framework == "Solidjs":
            solidjs_build.transfer(frontend_templates="Solidjs")

    def add_hiddenimports(self, package):
        self.pyinstallercommands.append(f"--hidden-import={package}")

    def log_level(self, log_level):
        self.pyinstallercommands.append(f"--log-level={log_level}")

    def add_data(self, folder_name):
        app_dir = self.workdir / str(folder_name)
        self.pyinstallercommands.append(
            f"--add-data={app_dir.parent.parent}\\{folder_name};{folder_name}"
        )

    def add_binary(self, folder_name):
        app_dir = self.workdir / str(folder_name)
        self.pyinstallercommands.append(
            f"--add-binary={app_dir.parent.parent}\\{folder_name};{folder_name}"
        )

    def set_icon(self, icon_name):
        icon_dir = self.workdir / str(icon_name)
        self.pyinstallercommands.append(f"--icon={icon_dir.parent.parent}\\{icon_name}")

    def run_build(
        self,
        document_name: str = "Web Application",
        *,
        frontend_folder: str = None,
        static_folder: str,
        templates_folder: str,
        frontend_framework: Literal["React", "Vue", "Solidjs"] = "React",
        backend_framework: Literal["fastapi", "starlette", "flask", "robyn"] = None,
    ):
        import shutil

        import PyInstaller.__main__

        if frontend_folder is None:
            if not os.path.exists(static_folder):
                return
            if not os.listdir(static_folder):
                main_js_content = "// Your main JavaScript content here"
                with open(os.path.join(static_folder, "main.js"), "w") as main_js_file:
                    main_js_file.write(main_js_content)

            else:
                pass

        if (
            backend_framework is not None
            and backend_framework == "fastapi"
            or backend_framework == "starlette"
        ):
            for package in self.uvicorn_packages:
                self.pyinstallercommands.append(f"--hidden-import={package}")

        if frontend_folder is not None:
            if frontend_framework == "React":
                self.build_static_files(
                    framework="React",
                    document_name=document_name,
                    frontend_folder=frontend_folder,
                    static=static_folder,
                    template=templates_folder,
                )
            elif frontend_framework == "Nextjs":
                self.build_static_files(
                    framework="React",
                    document_name=document_name,
                    frontend_folder=frontend_folder,
                    static=static_folder,
                    template=templates_folder,
                )
            elif frontend_framework == "React":
                self.build_static_files(
                    framework="React",
                    document_name=document_name,
                    frontend_folder=frontend_folder,
                    static=static_folder,
                    template=templates_folder,
                )
            elif frontend_framework == "Vue":
                self.build_static_files(
                    framework="Vue",
                    document_name=document_name,
                    frontend_folder=frontend_folder,
                    static=static_folder,
                    template=templates_folder,
                )
            elif frontend_framework == "Solidjs":
                self.build_static_files(
                    framework="Solidjs",
                    document_name=document_name,
                    frontend_folder=frontend_folder,
                    static=static_folder,
                    template=templates_folder,
                )

        args = [
            str(self.app_path),
            "--distpath",
            str(self.workdir / "dist"),
            f"--name={self.executable}",
            "--onefile",
            "--windowed",
        ]

        sys.path.insert(0, str(self.workdir))
        module_path = ".".join(
            list(reversed([x.stem for x in self.app_path.parents if x.stem]))
            + [self.app_path.stem]
        )
        try:
            importlib.import_module(module_path)
        except ImportError as e:
            print(f"No module found with this name: {e}")
            pass
        if self.executable is not None:
            PyInstaller.__main__.run(args + self.pyinstallercommands)
            shutil.move(f"{self.workdir}/dist", "./")
            spec = self.executable + ".spec"
            if os.path.exists(spec):
                os.remove(spec)
            shutil.rmtree("build")
            shutil.rmtree("out")
            os.rename("dist", "out")
            if os.path.isdir("__pycache__"):
                shutil.rmtree("__pycache__")
