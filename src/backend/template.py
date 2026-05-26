from pathlib import Path
import logging
import re

from .models.params import Params, SideParams

class Template:
    def __init__(self, source: Path):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        self.source = source
        self.content = self.source.read_text("utf-8")
        self.keys = re.findall(r"%[^%]+%", self.content)
        self.inner = self._get_inner()
    
    def build(self):
        # inner = _build_inner(params) 
        # -> _replace_inner(inner)
        # -> _replace_content(params) 
        # -> to file (self.content)
        
        inners = self._build_inner([
            SideParams("Reb", "Rhodesia", "Cool Place", "texture.png", "Template", "template"),
            SideParams("Reb", "Rhodesia", "Cool Place", "texture.png", "Template", "template")
        ])
        self._replace_inner(inners)
        self._replace_content(Params(
            "Rhodesia",
            "Mogrul",
            "https://mogrul.com"
        ))
        
        output_path = Path("out/addons/config.cpp")
        output_path.parent.mkdir(parents = True, exist_ok = True)
        output_path.write_text(self.content)
        
    def _get_inner(self) -> str | None:
        try:
            return re.search(r"#(.*?)#", self.content, re.DOTALL).group(1)
        except AttributeError:
            return None
    
    def _replace_inner(self, replacement: str) -> str:
        self.content = re.sub(r"#.*?#", replacement, self.content, flags = re.DOTALL)
        return self.content
    
    def _replace_content(self, params: Params) -> str:
        self.content = self.content.replace("%MOD_NAME%", params.mod_name)
        self.content = self.content.replace("%AUTHOR_NAME%", params.author_name)
        self.content = self.content.replace("%AUTHOR_URL%", params.author_url)
        
        return self.content
    
    def is_all_replaced(self) -> bool:
        return (
            ("#" not in self.content)
            and ("%" not in self.content)
        )
    
    def _build_inner(self, params: list[SideParams]) -> str:
        built = []
        
        for side_param in params:
            side_dict = {
                "%SIDE%": side_param.side,
                "%SIDE_NAME%": side_param.name,
                "%SIDE_DESCRIPTION%": side_param.description,
                "%SIDE_FLAG_TEXTURE%": side_param.flag_texture,
                "%SIDE_BASE_PATH%": side_param.base_path,
                "%SIDE_TEMPLATE_FILE_NO_EXT%": side_param.file_no_ext
            }
            template = self.inner
            
            for key, value in side_dict.items():
                if key not in self.keys:
                    self.logger.warning(f"Tried to replace key ({key}) in file ({self.source}) but no such key exists!")
                    continue
                
                template = template.replace(key, value)
        
            built.append(template)
        
        return "\n".join(built)